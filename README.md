dtrove
======

[![Build Status](https://travis-ci.org/rmyers/dtrove.svg?branch=master)](https://travis-ci.org/rmyers/dtrove)
[![Coverage Status](https://coveralls.io/repos/rmyers/dtrove/badge.png)](https://coveralls.io/r/rmyers/dtrove)

Fork of [openstack trove](http://wiki.openstack.org/wiki/Trove) written in Django



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
---------------------

The main way to run dtrove is in single superuser. Basically using the same
account to create all database clusters. All actions are handled thru the
management api.

To setup single user mode just add a few settings in your django settings
file. For Nova set the following:

* `NOVA_USERNAME`: OS_USERNAME of the nova user.
* `NOVA_PASSWORD`: OS_PASSWORD for the nova user.
* `NOVA_PROJECT_ID`: OS_TENANT_ID or OS_PROJECT_ID of the nova user.
* `NOVA_URL`: The url of the identity service for nova.
* `NOVA_BYPASS_URL`: Actual url to use instead of the endpoint from the catalog.
* `NOVA_ENDPOINT_TYPE`: (publicURL) Type of the nova endpoint.

If you are missing one and they are required to run you will receive a runtime
error with the appropriate list of settings you are missing.

Management Method
-----------------

There are two ways to manage the hosts in dtrove. There is no guest agent in
dtrove which is by design as the server is the brain of the operation and tells
the guests what to do.

* `SSH`: A special user is added to the hosts with sudo access and public key auth.
* `Console`: If you have access to the compute hosts you can run a remote worker.

For running with ssh you'll need to create a public/private ssh key:

    $ ssh_key_gen my_key.rsa

For running with a console access you need to make sure the celery worker is
running on all compute hosts.
