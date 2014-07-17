dtrove
======

[![Build Status](https://travis-ci.org/rmyers/dtrove.svg?branch=master)](https://travis-ci.org/rmyers/dtrove)
[![Coverage Status](https://coveralls.io/repos/rmyers/dtrove/badge.png)](https://coveralls.io/r/rmyers/dtrove)

Fork of [openstack trove](http://wiki.openstack.org/wiki/Trove) written in Django

The main difference is that the this project does not use a guest agent on the
host machines. Instead all the commands to manage the instances are done either
thru ssh or the console on the compute hosts.

Documentation
-------------

View the documentation on [read the docs](http://dtrove.readthedocs.org/en/latest/index.html)
