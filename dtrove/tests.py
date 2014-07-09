
from django.test import TestCase

from dtrove import models


# Helper methods
def create_datastore(manager=None):
    if manager is None:
        manager = 'dtrove.datastores.mysql.MySQLManager'
    return models.Datastore(manager_class=manager, version='1.0', image='none')


def create_cluster(name='test_cluster', datastore=None):
    if datastore is None:
        datastore = create_datastore()
    return models.Cluster(name=name, datastore=datastore)


def create_key(name='testkey', passphrase='none', private='sec', public='pub'):
    return models.Key(name=name,
                      passphrase=passphrase,
                      private=private,
                      public=public)


def create_instance(name='test_instance', cluster=None, key=None,
                    addr='127.0.0.1', user='root', server='test_server'):
    if cluster is None:
        cluster = create_cluster()

    if key is None:
        key = create_key()

    return models.Instance(name=name, cluster=cluster, key=key,
                           addr=addr, user=user, server=server)


class InstanceModelTests(TestCase):

    def setUp(self):
        self.instance = create_instance()

    def test_connection_info(self):
        expected = {
            'key': 'sec',
            'password': 'none',
            'host_string': 'root@127.0.0.1'
        }
        self.assertEqual(expected, self.instance.connection_info)

    def test_unicode(self):
        self.assertEqual(u'test_instance', unicode(self.instance))


class ClusterModelTests(TestCase):

    def setUp(self):
        self.cluster = create_cluster()

    def test_unicode(self):
        self.assertEqual(u'test_cluster', unicode(self.cluster))


class DatastoreModelTests(TestCase):

    def setUp(self):
        self.datastore = create_datastore()

    def test_unicode(self):
        self.assertEqual(u'mysql - 1.0', unicode(self.datastore))


class KeyModelTests(TestCase):

    def setUp(self):
        self.key = create_key()

    def test_unicode(self):
        self.assertEqual(u'testkey', unicode(self.key))
