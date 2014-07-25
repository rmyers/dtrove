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

from cStringIO import StringIO


class BaseManager(object):
    """Manager Base

    :param datastore: The actual datastore version that is being managed.
                      The datastores have the image and package information to
                      install on the guest vm's.
    """

    def __init__(self, datastore):
        """Creates a Manager"""
        self.datastore = datastore
        self.image = datastore.image
        self.packages = datastore.packages

    @property
    def name(self):
        """Returns the name of the manager ex: MySQLManager = mysql"""
        return self.__class__.__name__.replace('Manager', '').lower()

    def backup():
        """Preform a backup on the remote instance."""
        raise NotImplementedError()

    def prepare():
        """Install and configure the datastore on the instance."""
        raise NotImplementedError()
