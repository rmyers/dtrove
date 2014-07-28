
from .base import *


class BaseDatastoreTests(DtroveTest):

    def setUp(self):
        from dtrove.datastores.base import BaseManager
        self.datastore = create_datastore()
        self.manager = BaseManager(self.datastore)

    def test_backup(self):
        self.assertRaises(NotImplementedError, self.manager.backup, None)

    def test_prepare(self):
        self.assertRaises(NotImplementedError, self.manager.prepare, None)
