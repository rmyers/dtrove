"""
DTrove Models
=============

These objects persist infomation about the clusters, datastores and other
information to the Dtrove database. Creating instances of these are pretty
straight forward if you know anything about Django. When a user adds a
Cluster from the API or the web front end the underlining servers are created.
Celery workers are spawn to create the nodes and then report back the status.
For example::

    >>> from dtrove.models import *
    >>> ds = Datastore.objects.get(version='5.5')
    >>> ds
    <Datastore: mysql - 5.5>
    >>> c = Cluster.objects.create(name='my_cluster', datastore=ds, size=10)
    >>> c
    <Cluster: my_cluster>
    >>> c.datastore.name
    u'mysql - 5.5'
    >>> c.datastore.status
    u'spawning'

Once the cluster is in an 'active' state further operations can be done.

Available models
----------------

"""

from django.db import models

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

    The posibilities are endless!
    """

    name = models.CharField(max_length=255)
    datastore = models.ForeignKey('Datastore')
    size = models.IntegerField(default=2)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    @property
    def status(self):
        """Status of the cluster"""
        # TODO (rmyers): implement this
        return u'spawning'


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
        from django.utils.module_loading import import_string
        return import_string(self.manager_class)(self)

    @property
    def name(self):
        """The display name of the datastore (manager.name - version)"""
        return '%s - %s' % (self.manager.name, self.version)


class Key(models.Model):
    """SSH Key Pair

    This holds the public and private keys for connecting to a remote host.

    .. note:: This should have encrypted fields. Don't put anything really
              secure in here. This is just a proof of concept.

    :param str name: Name of the key
    :param str passphrase: Passphrase for the key
    :param str private: Text of the private key
    :param str public: Text of the public key

    These keys are attached to an instance, the idea is that each cluster
    would have it's own ssh key assigned to it. That way there isn't a single
    master key that own's your entire network.

    You should also use a passphrase for each key even though it is not a
    required field.

    You can access the information in this key in the
    :py:data:`dtrove.models.Instance.connection_info` property on the
    instance(s) the key is attached to.
    """
    name = models.CharField(max_length=50)
    passphrase = models.CharField(max_length=512, blank=True)
    private = models.TextField(blank=True)
    public = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class Instance(models.Model):
    """Instance

    This contains the information about the actual server instance that runs
    the datastore in the cluster.

    :param str name: Name of the instance
    :param cluster: Cluster that this instance is a part of
    :type cluster: :py:class:`dtrove.models.Cluster`
    :param key: SSH Key pair object for this instance
    :type key: :py:class:`dtrove.models.Key`
    :param str user: The user which the SSH Key is connected to
    :param ipaddr addr: IP Address of this server
    :param str server: UUID of the nova server instance

    .. note:: This model is internal only, all interactions are handled
              thought the cluster model and or the manager class on the
              cluster

    Remote operations can be preformed on this instance by using the
    connection_info property like so::

        from fabric.api import sudo, settings
        from fabric.network import disconnect_all
        from dtrove.models import Instance

        instance = Instance.objects.first()

        with settings(**instance.connection_info):
            sudo('rm -rf /etc/trove/*')

        # Always remember to disconnect ssh sessions
        disconnect_all()

    See the :py:class:`dtrove.datastores.base.BaseManager` class for more
    examples.
    """
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
        """Provides the connection info from the key stored for this server"""
        kwargs = {
            'key': self.key.private,
            'password': self.key.passphrase,
            'host_string': '%s@%s' % (self.user, self.addr),
        }
        return kwargs
