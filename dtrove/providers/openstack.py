
import time

from novaclient.v1_1 import client as nova_client
from cinderclient.v2 import client as cinder_client
from keystoneclient.v2_0 import client as keystone_client

from dtrove import config
from .base import BaseProvider


class Provider(BaseProvider):

    def __init__(self):
        self.username = config.OS_USERNAME
        self.password = config.OS_PASSWORD
        self.project_id = config.OS_PROJECT_ID
        self.auth_url = config.OS_AUTH_URL
        self.region_name = 'IAD'
        self.endpoints = None
        self.auth_token = None

    def _auth(self):
        self.ks = keystone_client.Client(username=self.username,
                                         password=self.password,
                                         project_id=self.project_id,
                                         auth_url=self.auth_url)
        auth_ref = self.ks.auth_ref
        self.auth_token = auth_ref.auth_token
        self.endpoints = auth_ref.service_catalog.get_endpoints()

    def _poll(self, instance):
        while True:
            status, progress = self.update_status(instance)

            if status in ['active']:
                instance.progress = 100
                break
            elif status == "error":
                raise Exception(instance.message)

            time.sleep(5)

    def url(self, service):
        if self.endpoints is None:
            self._auth()

        service_endpoints = self.endpoints.get('service', [])
        for endpoint in service_endpoints:
            if endpoint.get('region', '') == self.region_name:
                return endpoint.get('publicURL')

    @property
    def nova(self):
        if self.auth_token is None:
            self._auth()
        return nova_client.Client(username=self.username,
                                  api_key=self.password,
                                  project_id=self.project_id,
                                  auth_token=self.auth_token,
                                  region_name=self.region_name,
                                  auth_url=self.auth_url,
                                  bypass_url=self.url('compute'))

    def update_status(self, instance):
        if not instance.server:
            return 'NA', 0
        obj = self.nova.servers.get(instance.server)

        status = getattr(obj, 'status', 'none').lower()
        progress = getattr(obj, 'progress', None) or 0

        if status == "error":
            instance.message = obj.fault['message']

        instance.server_status = status
        instance.progress = progress

        return status, progress

    def create_key(self, key):
        try:
            existing = self.nova.keypairs.get(key.name)
        except:
            self.nova.keypairs.create(name=key.name, public_key=key.public)

    def create(self, instance):
        cluster = instance.cluster
        datastore = cluster.datastore
        image = datastore.image
        key = instance.key
        # TODO: don't hard code this
        flavor = '2'
        # First create a keypair to log in with
        self.create_key(key)
        server = self.nova.servers.create(name=instance.name,
                                          image=image,
                                          flavor=flavor,
                                          key_name=key.name)
        time.sleep(3)
        server = self.nova.servers.get(server.id)
        instance.server = server.id
        instance.addr = server.accessIPv4
        instance.save()
        self._poll(instance)
