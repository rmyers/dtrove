
from django.core.exceptions import ValidationError
from django.test import TestCase
from mock import patch, MagicMock

from dtrove import models


# Helper methods
def create_datastore(manager=None, save=False):
    if manager is None:
        manager = 'dtrove.datastores.mysql.MySQLManager'
    ds = models.Datastore(manager_class=manager, version='1.0', image='none')
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
        patcher = patch('dtrove.models.Instance.provision')
        self.MockClass = patcher.start()
        self.addCleanup(patcher.stop)
        self.cluster = create_cluster(size=2, save=True)

    def test_unicode(self):
        self.assertEqual(u'test_cluster', unicode(self.cluster))

    def test_max_cluster(self):
        kwargs = {
            'name': 'foo',
            'size': 10,
            'datastore': self.cluster.datastore,
        }
        self.assertRaises(
            ValidationError, models.Cluster.objects.create, **kwargs)

    def test_instance_creation_on_save(self):
        self.cluster.save()
        self.assertEqual(2, self.cluster.instance_set.count())

    def test_multiple_saves(self):
        self.cluster.save()
        self.assertEqual(2, self.cluster.instance_set.count())
        self.cluster.save()
        self.assertEqual(2, self.cluster.instance_set.count())

    def test_add_node(self):
        self.cluster.save()
        self.assertEqual(2, self.cluster.instance_set.count())
        self.cluster.add_node()
        self.assertEqual(3, self.cluster.instance_set.count())
        self.assertEqual(3, self.cluster.size)


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
        self.cluster = create_cluster(size=0, save=True)
        self.key = create_key(save=True)
        self.instance = create_instance(cluster=self.cluster,
                                        key=self.key,
                                        save=True)

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
