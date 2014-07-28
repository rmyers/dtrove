
from .base import *


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
            task.delay.assert_called_with(instance.pk)


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
