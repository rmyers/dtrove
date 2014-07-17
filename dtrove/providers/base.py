"""

This is the interface that the provisioning system uses to create new
nodes/volumes/backups for the clusters.

These classes are meant to be used in the task system as they are usually
long running operations. During the execution of a long running process
the status should be updated on the base objects, usually a
:py:class:`dtrove.models.Instance`.

Here is a example::

    from celery import shared_task
    from dtrove.models import Instance
    from dtrove.provider import get_provider

    provider = get_provider()

    @shared_task
    def create(instance_id):
        instance = Instance.objects.get(pk=instance_id)
        provider.create(instance)

"""

from dtrove import config


def get_provider():
    "Return the current provider class"
    from django.utils.module_loading import import_string
    return import_string(config.DTROVE_PROVIDER)()


class ProviderError(Exception):
    """An exception during a provisoner action."""


class BaseProvider(object):
    """Base Provider Interface"""

    #: Whether or not this provider supports creating and attaching volumes
    supports_volumes = True

    #: Whether of not this provider supports snapshots
    supports_snapshots = True

    def create(self, instance, **kwargs):
        """Creates a new instance

        :param instance: An instance object to create
        :type instance: :py:class:`dtrove.models.Instance`
        :raises: :py:class:`dtrove.providers.base.ProviderError`
            If the create failed

        Typically the provider should respond with a 202 message and work
        in the background to create the instance. So during creation of the
        instance on the provider this should update the progress field of the
        instance.

        The provider should update instance with the following info:

          * `server`: Reference to the actual server id on the provider
          * `addr`: The public facing ip address to this server
          * `user`: The inital user that was created

        The task, status and progress are properties that are cached on the
        :py:class:`dtrove.models.Instance` Instance object.
        """
        raise NotImplementedError()

    def destroy(self, instance):
        """Destroys an instance

        :param instance: An instance object to delete
        :type instance: :py:class:`dtrove.models.Instance`
        :raises: :py:class:`dtrove.providers.base.ProviderError`
            If the delete failed

        This should delete the instance and poll until the instance is deleted.
        """
        raise NotImplementedError()

    def snapshot(self, instance):
        """Creates a snapshot of an instance

        :param instance: An instance object to delete
        :type instance: :py:class:`dtrove.models.Instance`
        :raises: :py:class:`dtrove.providers.base.ProviderError`
            If the snapshot failed
        """
        raise NotImplementedError()

    def attach_volume(self, instance):
        """Creates and mounts a volume on an instance

        :param instance: An instance object to delete
        :type instance: :py:class:`dtrove.models.Instance`
        :raises: :py:class:`dtrove.providers.base.ProviderError`
            If the volume create and mount failed

        The provider should update instance with the following info:

          * `volume`: Reference to the actual volume id on the provider

        """
        raise NotImplementedError()

    def flavors(self, datastore=None):
        """Return a list of flavors available

        :param str datastore: (optional) datastore to filter flavors by
        """
        raise NotImplementedError()
