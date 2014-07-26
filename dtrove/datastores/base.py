"""
DTrove Datastore Base Classes
=============================

The base classes that define the interface for all datastores.

If you wish to create your own datastore, simply subclass the base and
override the methods you need to for example::

    from dtrove.datastores import base
    from dtrove.commands import run

    class MyBackyardDBManager(base.BaseManager):

        def backup():
            with self.conn as connection:
                run('/bin/bash my_backup.sh')

        @property
        def name():
            return 'ClassNameOverriddenDB'

Templates for the managers live in `dtrove/datastores/<manager_name>` where
manager name by default is the lowercase manager name with the 'Manager'
removed. For example 'MySQLManager' would be 'mysql'.

More on templates later.

"""

from django.template.loader import select_template
from django.template import Context
from fabric.api import run, env, put


class BaseManager(object):
    """Manager Base

    :param datastore: The actual datastore version that is being managed.
                      The datastores have the image and package information to
                      install on the guest vm's.
    """

    #: Name of the service ie 'mysql'
    service_name = None

    def __init__(self, datastore):
        """Creates a Manager"""
        self.datastore = datastore
        self.image = datastore.image
        packages = datastore.packages.split('\n')
        self.packages = map(lambda pkg: pkg.strip(), packages)

    @property
    def name(self):
        """Returns the name of the manager ex: MySQLManager = mysql"""
        return self.__class__.__name__.replace('Manager', '').lower()

    def backup(self, instance):
        """Preform a backup on the remote instance."""
        raise NotImplementedError()

    def prepare(self, instance):
        """Install and configure the datastore on the instance."""
        raise NotImplementedError()

    def render_config_file(self, instance):
        """Load and render a config file for this datastore."""
        context = Context({
            'instance': instance,
            'datastore': self.datastore,
        })
        lookup = {
            'manager': self.name,
            'name': self.datastore.name,
            'version': self.datastore.version,
        }
        template = select_template([
            '%(manager)s/%(name)s/%(version)s/config' % lookup,
            '%(manager)s/%(name)s/config' % lookup,
            '%(manager)s/config' % lookup,
        ])
        return template.render(context)

    def restart(self):
        """Restart the datastore."""
        run('service %s restart' % self.service_name)

    def stop(self):
        """Stop the datastore"""
        run('service %s stop' % self.service_name)

    def start():
        """Start the datastore"""
        run('service %s start' % self.service_name)
