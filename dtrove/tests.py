
from django.test import TestCase
from mock import patch

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


class DtroveTest(TestCase):
    pass


class InstanceModelTests(DtroveTest):

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


class ClusterModelTests(DtroveTest):

    def setUp(self):
        self.cluster = create_cluster()

    def test_unicode(self):
        self.assertEqual(u'test_cluster', unicode(self.cluster))

    def test_status(self):
        self.assertEqual(u'spawning', self.cluster.status)


class DatastoreModelTests(DtroveTest):

    def setUp(self):
        self.datastore = create_datastore()

    def test_unicode(self):
        self.assertEqual(u'mysql-1.0', unicode(self.datastore))


class KeyModelTests(DtroveTest):

    def setUp(self):
        self.key = create_key()

    def test_unicode(self):
        self.assertEqual(u'testkey', unicode(self.key))


class TaskTests(DtroveTest):

    def setUp(self):
        self.ds = create_datastore()
        self.ds.save()
        self.cluster = create_cluster(datastore=self.ds)
        self.cluster.save()
        self.key = create_key()
        self.key.save()
        self.instance = create_instance(cluster=self.cluster, key=self.key)
        self.instance.save()

    def test_debug(self):
        from dtrove.celery import debug_task
        output = debug_task()
        self.assertEqual('Request: <Context: {}>', output)

    def test_perform(self):
        from dtrove.tasks import preform
        from fabric.api import env
        with patch('dtrove.tasks.run') as fake_run:
            cmd = '%(key)s %(password)s %(host_string)s'
            expected = 'sec none root@127.0.0.1'
            output = preform(self.instance.pk, '', cmd)
            fake_run.assert_called_with('sec none root@127.0.0.1')
