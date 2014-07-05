dtrove
======

[![Build Status](https://travis-ci.org/rmyers/dtrove.svg?branch=master)](https://travis-ci.org/rmyers/dtrove)
[![Coverage Status](https://coveralls.io/repos/rmyers/dtrove/badge.png)](https://coveralls.io/r/rmyers/dtrove)

Fork of openstack trove written in Django

API
---

The v1 api is mostly consistent with the trove api. You can see the api here:

   [trove api](http://wiki.openstack.org/wiki/Trove)

Differences
-----------

The main difference is that the this project does not use a guest agent on the
host machines. Instead all the commands to manage the instances are done either
thru ssh or the console on the compute hosts.

Hacking
-------

First setup the environment to use dtrove:

    $ mkvirtualenv dtrove -r requirements.txt

Then setup the initial data and databases:

    $ fab install

Setup Management API
-------------------

The main way to run dtrove is in single superuser. Basically using the same
account to create all database clusters. All actions are handled thru the
management api.

To setup single user mode just add a .supernova conf in the home directory of
the user that runs the server. Using supernova allows you to use multiple
accounts or services easily. Here is a example config:

    [nova]
    OS_USERNAME = {my_username}
    OS_API_KEY = {my_api_key}
    OS_TENANT_NAME = {my_tenant}
    OS_PROJECT_ID = {my_project}
    NOVA_URL='https://identity.api.rackspacecloud.com/v2.0'

    [cinder]
    OS_EXECUTABLE = cinder
    OS_USERNAME = {my_username}
    OS_API_KEY = {my_api_key}
    OS_TENANT_NAME = {my_tenant}
    OS_PROJECT_ID = {my_project}
    CINDER_URL='https://identity.api.rackspacecloud.com/v2.0'

Management Method
-----------------

There are two ways to manage the hosts in dtrove. There is no guest agent in
dtrove which is by design as the server is the brain of the operation and tells
the guests what to do.

* SSH: A special user is added to the hosts with sudo access and public key auth.
* Console: If you have access to the compute hosts you can run a remote worker.

For running with ssh you'll need to create a public/private ssh key:

    $ ssh_key_gen my_key.rsa

For running with a console access you need to make sure the celery worker is
running on all compute hosts.
