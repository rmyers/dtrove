
from .base import *


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
        with patch('dtrove.tasks.PROVIDER') as prov:
            with patch('dtrove.tasks.prepare') as prepare:
                create(self.instance.pk)
                prov.create.assert_called_with(self.instance)
                prepare.assert_called_with(self.instance.id)
