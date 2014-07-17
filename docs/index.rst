
Welcome to DTrove's documentation!
==================================

Fork of `openstack trove`_ written in Django

The main difference is that the this project does not use a guest agent on the
host machines. Instead all the commands to manage the instances are done either
thru ssh or the console on the compute hosts.

If you like the project `fork it on github`_.

.. _openstack trove: http://wiki.openstack.org/wiki/Trove
.. _fork it on github: https://github.com/rmyers/dtrove

Quickstart Guide
---------------------

The main way to run dtrove is in single superuser. Basically using the same
account to create all database clusters. The plan is to make the api honor
the same access controls as the :ref:`providers` you have chosen.

Install
~~~~~~~

You have to go bleeding edge on a project like this, so break out your
trusty `git` tool and prepare to get dirty

1. Clone this repository::

    $ git clone https://github.com/rmyers/dtrove.git
    $ cd dtrove
    $ mkvirtualenv dtrove -r requirements.txt
    $ pip install -e .

2. Now you are ready to add this to your django settings file::

    INSTALLED_APPS = (
        ...
        'dtrove',
        'rest_framework',
    )

3. For the default Openstack Provider set the following::

    OS_USERNAME=your_nova_user.
    OS_PASSWORD=your_password
    OS_PROJECT_ID=your_project_id
    OS_NOVA_URL=http://localhost:5000

  .. note:: See the :ref:`config` for details about all the options available.

4. First run the migrations::

    $ python manage.py migrate


Creating Clusters
~~~~~~~~~~~~~~~~~

First

Further Reading
---------------

See the following sections for more details on the setup of dtrove.

.. toctree::
   datastores
   providers
   tasks
   models
   config
   :maxdepth: 1


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
