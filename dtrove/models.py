
from django.db import models
from django.utils.module_loading import import_string

from dtrove import config


class Cluster(models.Model):
    """Datastore Cluster

    This is the Main User facing object it defines the datastore type along
    with the size of the cluster and the other user options.

    :param str name: Name of the cluster
    :param datastore: Datastore of the cluster
    :type datastore: :py:class:`dtrove.models.Datastore`
    :param int size: Number of nodes in the cluster

    When a user creates a new Cluster the system handles provisioning the
    underlining instances and checking on the health of them.

    After the cluster is created the user can then use the datastores, or
    perform certain actions:

    * Schedule automated backups
    * Import from a previous datastore export
    * Export the data into a transportable type
    * Change configuration parameters

    More options later
    """

    name = models.CharField(max_length=255)
    datastore = models.ForeignKey('Datastore')
    size = models.IntegerField(default=2)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class Datastore(models.Model):
    """Datastore

    This represents a version of a specific datastore that is available

    :param manager_class: The dotted path to the actual manager object
    :type manager_class: :py:class:`dtrove.config.DTROVE_DATASTORE_MANAGERS`
    :param str version: The version of the datastore ex: 5.6
    :param str image: The id of the VM image to use to create new instances
    :param str packages: Comma separated list of packages to install

    The main purpose of this object is to link the datastore manager to
    a list of packages to install and the base image that is used to create
    instances.

    By creating an datastore that makes it available for users to select and
    install a cluster from it.

    The `manager_class` property should be an importable subclass of the
    :py:class:`dtrove.datastores.base.BaseManager` class.
    """
    manager_class = models.CharField(
        max_length=255,
        choices=config.DTROVE_DATASTORE_MANAGERS)
    version = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    packages = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    @property
    def manager(self):
        """The manager object initialize with this datastores information"""
        return import_string(self.manager_class)(self)

    @property
    def name(self):
        """The display name of the datastore (manager.name - version)"""
        return '%s - %s' % (self.manager.name, self.version)


class Key(models.Model):
    name = models.CharField(max_length=50)
    passphase = models.CharField(max_length=512, blank=True)
    private = models.TextField(blank=True)
    public = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class Instance(models.Model):
    name = models.CharField(max_length=255)
    cluster = models.ForeignKey(Cluster)
    key = models.ForeignKey(Key, null=True, blank=True)
    user = models.CharField(max_length=25, default='root')
    addr = models.GenericIPAddressField(null=True, blank=True)
    server = models.CharField(max_length=36, blank=True,
                              help_text='Nova server UUID')

    def __unicode__(self):
        return self.name

    @property
    def connection_info(self):
        kwargs = {
            'key': self.key.private,
            'password': self.key.passphase,
            'host_string': '%s@%s' % (self.user, self.addr),
        }
        return kwargs
