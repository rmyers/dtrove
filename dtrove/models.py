
from django.db import models
from django.utils.module_loading import import_string

from dtrove import config


class Cluster(models.Model):
    name = models.CharField(max_length=255)
    datastore = models.ForeignKey('Datastore')
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
