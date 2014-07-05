
import logging

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from keystoneclient import exceptions as keystone_exceptions

from openstack_auth.backend import KeystoneBackend
from openstack_auth import exceptions
from openstack_auth import user as auth_user
from openstack_auth import utils


LOG = logging.getLogger(__name__)

KEYSTONE_CLIENT_ATTR = "_keystoneclient"


class RaxBackend(KeystoneBackend):
    """Django authentication backend class for rackspace.

    This is based off of the ``openstack_auth.backend.KeystoneBackend``.
    The main difference is that the Rackspace catalog is slightly different
    than the keystone one. So this accounts for that and also cuts out a bunch
    of logic for stuff I don't care for.
    """

    def authenticate(self, request=None, username=None, password=None):
        """Authenticates a user via the Keystone Identity API. """
        LOG.debug('Beginning user authentication for user "%s".' % username)

        insecure = getattr(settings, 'OPENSTACK_SSL_NO_VERIFY', False)
        ca_cert = getattr(settings, "OPENSTACK_SSL_CACERT", None)
        endpoint_type = getattr(
            settings, 'OPENSTACK_ENDPOINT_TYPE', 'publicURL')
        auth_url = getattr(
            settings, "OPENSTACK_KEYSTONE_URL", "http://0.0.0.0:5000/v2.0")

        keystone_client = utils.get_keystone_client()
        try:
            client = keystone_client.Client(
                username=username,
                password=password,
                auth_url=auth_url,
                insecure=insecure,
                cacert=ca_cert,
                debug=settings.DEBUG)

            unscoped_auth_ref = client.auth_ref
            unscoped_token = auth_user.Token(auth_ref=unscoped_auth_ref)
        except (keystone_exceptions.Unauthorized,
                keystone_exceptions.Forbidden,
                keystone_exceptions.NotFound) as exc:
            msg = _('Invalid user name or password.')
            LOG.debug(str(exc))
            return None
        except (keystone_exceptions.ClientException,
                keystone_exceptions.AuthorizationFailure) as exc:
            msg = _("An error occurred authenticating. "
                    "Please try again later.")
            LOG.debug(str(exc))
            return None

        # Check expiry for our unscoped auth ref.
        self.check_auth_expiry(unscoped_auth_ref)

        # Check if token is automatically scoped to default_project
        if unscoped_auth_ref.project_scoped:
            auth_ref = unscoped_auth_ref
        else:
            return None

        # Check expiry for our new scoped token.
        self.check_auth_expiry(auth_ref)

        # If we made it here we succeeded. Create our User!
        user = auth_user.create_user_from_token(
            request,
            auth_user.Token(auth_ref),
            auth_url)

        if request is not None:
            auth_user.set_session_from_user(request, user)

            # Support client caching to save on auth calls.
            setattr(request, KEYSTONE_CLIENT_ATTR, client)

        logging.error('Authentication completed for user "%s".' % username)
        return user
