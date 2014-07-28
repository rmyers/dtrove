
from collections import namedtuple

from .base import *

# Openstack mock response classes
OSServer = namedtuple('OpenstackServer',
                      ['accessIPv4', 'id', 'status', 'progress', 'fault'])


class BaseProviderTests(DtroveTest):

    def setUp(self):
        from dtrove.providers.base import BaseProvider
        self.provider = BaseProvider()

    def test_base_create(self):
        self.assertRaises(NotImplementedError, self.provider.create, '')

    def test_base_update(self):
        self.assertRaises(NotImplementedError, self.provider.update_status, '')

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
        # Mocks
        mock_nova = patch('dtrove.providers.openstack.nova_client')
        mock_cinder = patch('dtrove.providers.openstack.cinder_client')
        mock_key = patch('dtrove.providers.openstack.keystone_client')
        mock_provision = patch('dtrove.models.Instance.provision')
        self.MockNova = mock_nova.start()
        self.MockCinder = mock_cinder.start()
        self.MockKeystone = mock_key.start()
        self.MockProvision = mock_provision.start()
        # Add clean ups
        self.addCleanup(mock_nova.stop)
        self.addCleanup(mock_cinder.stop)
        self.addCleanup(mock_key.stop)
        self.addCleanup(mock_provision.stop)
        # An instance to provision
        self.instance = create_instance(server='', save=True)
        # shortcut to mock clients
        self.nova = self.MockNova.Client()
        self.keystone = self.MockKeystone.Client()

    def test_nova_client(self):
        self.assertEqual(self.nova, self.provider.nova)
        self.MockNova.Client.assert_called_with(
            username=settings.OS_USERNAME,
            project_id=settings.OS_PROJECT_ID,
            region_name='IAD',
            bypass_url=None,
            auth_token=self.keystone.auth_ref.auth_token,
            auth_url=settings.OS_AUTH_URL,
            api_key=settings.OS_PASSWORD,
        )

    def test_create(self):
        servers = [
            OSServer('127.0.0.1', 'uuid', 'building', 10, {}),
            OSServer('127.0.0.1', 'uuid', 'building', 50, {}),
            OSServer('127.0.0.1', 'uuid', 'active', 90, {}),
        ]

        def side_effect(*args, **kwargs):
            return servers.pop(0)

        self.nova.servers.get.side_effect = side_effect
        self.provider.create(self.instance)
        self.assertEqual('active', self.instance.server_status)
        self.assertEqual(100, self.instance.progress)

    def test_create_error(self):
        server = OSServer('127.0.0.1', 'id', 'error', 10, {'message': 'fail'})
        self.nova.servers.get.return_value = server
        self.assertRaises(Exception, self.provider.create, self.instance)
        self.assertEqual('error', self.instance.server_status)
        self.assertEqual(10, self.instance.progress)
        self.assertEqual('fail', self.instance.message)

    def test_update_status(self):
        # Test update_status on a new instance with no server
        self.provider.update_status(self.instance)
        self.assertEqual('NA', self.instance.server_status)
        self.assertEqual(0, self.instance.progress)

    def test_url(self):
        SC = {
            'foo': [
                {'region': 'IAD', 'publicURL': 'my_url'}
            ]
        }
        self.keystone.auth_ref.service_catalog.get_endpoints.return_value = SC
        url = self.provider.url('foo')
        self.assertEqual('my_url', url)

    def test_create_missing_key(self):
        self.nova.keypairs.get.side_effect = Exception
        self.provider.create_key(self.instance.key)
        self.nova.keypairs.create.assert_called_with(
            name=self.instance.key.name,
            public_key=self.instance.key.public
        )
