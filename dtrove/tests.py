
from collections import namedtuple

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

# Openstack mock response classes
OSServer = namedtuple('OpenstackServer',
                      ['accessIPv4', 'id', 'status', 'progress', 'fault'])


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

    def test_status(self):
        with patch('dtrove.models.PROVIDER') as prov:
            prov.update_status.return_value = ('building', 10)
            self.assertEqual('building', self.instance.server_status)
            prov.update_status.assert_called_with(self.instance)

    def test_set_status(self):
        instance = create_instance(server='status_setter')
        instance.server_status = 'building'
        self.assertEqual('building', instance.server_status)

    def test_progress(self):
        with patch('dtrove.models.PROVIDER') as prov:
            prov.update_status.return_value = ('building', 10)
            self.assertEqual(10, self.instance.progress)
            prov.update_status.assert_called_with(self.instance)

    def test_set_progress(self):
        instance = create_instance(server='progress_setter')
        instance.progress = 24
        self.assertEqual(24, instance.progress)

    def test_message(self):
        instance = create_instance(server='message_getter')
        self.assertEqual('', instance.message)
        instance.message = 'I am a message'
        self.assertEqual('I am a message', instance.message)

    def test_provision(self):
        with patch('dtrove.tasks.create') as task:
            instance = create_instance(server='', save=True)
            task.delay.assert_called_with(instance)


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

    def test_add_too_large(self):
        self.cluster.save()
        self.assertRaises(ValidationError, self.cluster.add_node, 5)


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
        patcher = patch('dtrove.models.Instance.provision')
        self.MockClass = patcher.start()
        self.addCleanup(patcher.stop)
        self.cluster = create_cluster(size=2, save=True)
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

    def test_create(self):
        from dtrove.tasks import create
        instance_id = create(self.instance.pk)
        self.assertEqual(self.instance.pk, instance_id)


class BaseProviderTests(DtroveTest):

    def setUp(self):
        from dtrove.providers.base import BaseProvider
        self.provider = BaseProvider()

    def test_base_create(self):
        self.assertRaises(NotImplementedError, self.provider.create, '')

    def test_base_destroy(self):
        self.assertRaises(NotImplementedError, self.provider.destroy, '')

    def test_base_snapshot(self):
        self.assertRaises(NotImplementedError, self.provider.snapshot, '')

    def test_base_attach_volume(self):
        self.assertRaises(NotImplementedError, self.provider.attach_volume, '')

    def test_base_flavors(self):
        self.assertRaises(NotImplementedError, self.provider.flavors, '')

    def test_get_provider(self):
        from dtrove.providers.openstack import Provider
        from dtrove.providers import get_provider
        p = get_provider()
        self.assertTrue(isinstance(p, Provider))


class OpenStackProviderTests(DtroveTest):

    def setUp(self):
        from dtrove.providers.openstack import Provider
        self.provider = Provider()
        mock_nova = patch('dtrove.providers.openstack.nova_client')
        self.MockNova = mock_nova.start()
        self.addCleanup(mock_nova.stop)
        mock_cinder = patch('dtrove.providers.openstack.cinder_client')
        self.MockCinder = mock_cinder.start()
        self.addCleanup(mock_cinder.stop)
        mock_key = patch('dtrove.providers.openstack.keystone_client')
        self.MockKeystone = mock_key.start()
        self.addCleanup(mock_key.stop)
        patcher = patch('dtrove.models.Instance.provision')
        self.MockInstance = patcher.start()
        self.addCleanup(patcher.stop)
        self.instance = create_instance(server='', save=True)
        self.MockNova.Client = MagicMock()
        self.MockNova.Client().servers = MagicMock()

    def test_nova_client(self):
        self.assertEqual(self.MockNova.Client(), self.provider.nova)
        self.MockNova.Client.assert_called_with(
            username='test_user',
            project_id='12345',
            region_name='IAD',
            bypass_url=None,
            auth_token=self.MockKeystone.Client().auth_ref.auth_token,
            auth_url='http://localhost:5000/v2.0',
            api_key='test_pass'
        )

    def test_create(self):
        server = OSServer('127.0.0.1', 'uuid', 'active', 90, {})
        self.MockNova.Client().servers.get.return_value = server
        self.provider.create(self.instance)
        self.assertEqual('active', self.instance.server_status)
        self.assertEqual(100, self.instance.progress)

    def test_create_error(self):
        server = OSServer('127.0.0.1', 'id', 'error', 10, {'message': 'fail'})
        self.MockNova.Client().servers.get.return_value = server
        self.assertRaises(Exception, self.provider.create, self.instance)
        self.assertEqual('error', self.instance.server_status)
        self.assertEqual(10, self.instance.progress)
        self.assertEqual('fail', self.instance.message)
