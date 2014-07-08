
from django.db import models
from django.utils.module_loading import import_string

from dtrove import config


class Cluster(models.Model):
    name = models.CharField(max_length=255)
    datastore = models.ForeignKey('Datastore')
    size = models.IntegerField(default=2)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class Datastore(models.Model):
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
        return import_string(self.manager_class)(self)

    @property
    def name(self):
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
