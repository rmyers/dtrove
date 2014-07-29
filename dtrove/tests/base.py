
import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase
from mock import patch, MagicMock, ANY, call

from dtrove import models

level = logging.INFO
if settings.DEBUG:
    level = logging.DEBUG

logging.basicConfig(filename='test.log', level=level)


def create_datastore(manager=None, packages='', save=False):
    if manager is None:
        manager = 'dtrove.datastores.mysql.MySQLManager'
    ds = models.Datastore(manager_class=manager,
                          packages=packages,
                          version='1.0',
                          image='none')
    if save:
        ds.save()
    return ds


def create_cluster(name='test_cluster', datastore=None, size=0, save=False):
    if datastore is None:
        datastore = create_datastore(save=save)
    cluster = models.Cluster(name=name, datastore=datastore, size=size)
    if save:
        cluster.save()
    return cluster


def create_key(name='testkey', passphrase='none', private='sec',
               public='pub', save=False):
    key = models.Key(name=name,
                     passphrase=passphrase,
                     private=private,
                     public=public)
    if save:
        key.save()
    return key


def create_instance(name='test_instance', save=False, cluster=None, key=None,
                    addr='127.0.0.1', user='root', server='test_server'):
    if cluster is None:
        cluster = create_cluster(save=save)

    if key is None:
        key = create_key(save=save)

    instance = models.Instance(name=name, cluster=cluster, key=key,
                               addr=addr, user=user, server=server)
    if save:
        instance.save()
    return instance


class DtroveTest(TestCase):
    pass
