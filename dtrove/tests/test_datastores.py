
from django.template import TemplateDoesNotExist

from dtrove.datastores.base import BaseManager
from dtrove.datastores.mysql import MySQLManager
from .base import *


class BaseDatastoreTests(DtroveTest):

    def setUp(self):
        self.datastore = create_datastore()
        self.instance = create_instance()
        self.manager = BaseManager(self.datastore)
        patcher = patch('dtrove.datastores.base.run')
        self.mock_run = patcher.start()
        self.addCleanup(patcher.stop)

    def test_backup(self):
        self.assertRaises(NotImplementedError, self.manager.backup, None)

    def test_prepare(self):
        self.assertRaises(NotImplementedError, self.manager.prepare, None)

    def test_render_config_file(self):
        template = self.manager.render_config_file(self.instance)
        self.assertTemplateUsed(template, 'mysql/config')

    def test_config_not_found(self):
        ds = create_datastore(manager='dtrove.datastores.base.BaseManager')
        manager = BaseManager(ds)
        self.assertRaises(TemplateDoesNotExist,
                          manager.render_config_file,
                          self.instance)

    def test_start(self):
        self.manager.start()
        self.mock_run.assert_called_with('service None start')

    def test_restart(self):
        self.manager.restart()
        self.mock_run.assert_called_with('service None restart')

    def test_stop(self):
        self.manager.stop()
        self.mock_run.assert_called_with('service None stop')

    def test_packages_blanks(self):
        ds_spacey = create_datastore(packages='  \n  curl  \n  ssh')
        manager = BaseManager(ds_spacey)
        self.assertEqual(['curl', 'ssh'], manager.packages)

    def test_packages_empty(self):
        ds_spacey = create_datastore(packages='        \n')
        manager = BaseManager(ds_spacey)
        self.assertEqual([], manager.packages)


class TestMySQLManager(DtroveTest):

    def setUp(self):
        m_run = patch('dtrove.datastores.mysql.run')
        m_put = patch('dtrove.datastores.mysql.put')
        b_run = patch('dtrove.datastores.base.run')
        self.mock_run = m_run.start()
        self.addCleanup(m_run.stop)
        self.mock_put = m_put.start()
        self.addCleanup(m_put.stop)
        self.mock_base_run = b_run.start()
        self.addCleanup(b_run.stop)
        self.datastore = create_datastore(packages='mysql-server')
        self.instance = create_instance()
        self.manager = MySQLManager(self.datastore)

    def test_prepare(self):
        self.manager.prepare(self.instance)
        apt = 'DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server'
        self.mock_run.assert_has_calls([
            call('apt-get update'),
            call(apt)
        ])
        self.mock_put.assert_called_with(ANY, '/etc/mysql/my.cnf')
        self.mock_base_run.assert_called_with('service mysql restart')
