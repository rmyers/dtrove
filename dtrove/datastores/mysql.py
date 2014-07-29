"""
Oracle MySQL Manager
--------------------

"""

from cStringIO import StringIO

from fabric.api import run, env, put

from dtrove.datastores import base


class MySQLManager(base.BaseManager):
    """Oracle MySQL Manager"""
    service_name = 'mysql'

    def prepare(self, instance):
        run('apt-get update')
        for pkg in self.packages:
            run('DEBIAN_FRONTEND=noninteractive apt-get install -y %s' % pkg)

        config = StringIO(self.render_config_file(instance))
        put(config, '/etc/mysql/my.cnf')

        self.restart()
