dtrove
======

[![Build Status](https://travis-ci.org/rmyers/dtrove.svg?branch=master)](https://travis-ci.org/rmyers/dtrove)

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

Then do stuff
