"""
Configuration Options
=====================

This extends the normal django settings module so we can simply call::

    from dtrove import config
    NOVA_USER = config.NOVA_USERNAME

This allows us to have a consistent place to define possible settings
and document them as well as provide some defaults and warnings.
To modify any of these values simply edit your django settings file.

"""
from __future__ import absolute_import

import logging

from django.conf import settings

# The celery app must be loaded here to make the @shared_task decorator work.
from .celery import app as celery_app


def _get(name, default=None, warn=False):
    """Get an attribute from django settings or a default."""
    if warn and not hasattr(settings, name):
        logging.warn("Unable to find setting: %s", name)
    return getattr(settings, name, default)


# Default set of datastore managers used in choice field
_MANAGERS = [
    ('dtrove.datastores.mysql.MySQLManager', 'mysql'),
    ('dtrove.datastores.redis.RedisManager', 'redis'),
    ('dtrove.datastores.pgsql.PostgresManager', 'postgres')
]


class config():
    """
    This defines the available options to configure dtrove.

    These are set or overridden in the django settings file.
    """

    #: The nova management username
    NOVA_USERNAME = _get('NOVA_USERNAME', warn=True)

    #: The nova management user's password
    NOVA_PASSWORD = _get('NOVA_PASSWORD', warn=True)

    #: OS_TENANT_ID or OS_PROJECT_ID of the nova user.
    NOVA_PROJECT_ID = _get('NOVA_PROJECT_ID', warn=True)

    #: The url of the identity service for nova.
    NOVA_URL = _get('NOVA_URL', 'http://0.0.0.0:5000/v2.0')

    #: Actual url to use instead of the endpoint from the catalog.
    NOVA_BYPASS_URL = _get('NOVA_BYPASS_URL')

    #: Type of the nova endpoint.
    NOVA_ENDPOINT_TYPE = _get('NOVA_ENDPOINT_TYPE', 'publicURL')

    #: List of available datastores. This should be a list of tuples::
    #:
    #:     [('path.to.Manager', 'manager_name'), ...]
    #:
    DTROVE_DATASTORE_MANAGERS = _get('DTROVE_DATASTORE_MANAGERS', _MANAGERS)
