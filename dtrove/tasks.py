"""
Tasks
============

These handle all the remote operations that happen. Such as building a new
cluster, or run a scheduled backup. We are using celery as our worker
daemon, giving us a powerful system to schedule or chain tasks together.

By chaining tasks together, we can have a simple workflow pattern and can
trigger a roll back if needed.
"""

from __future__ import absolute_import

from celery import shared_task
from fabric.api import run, env, settings, prefix

from dtrove import config


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def preform(instance_id, name, *cmds):
    """Connects to the instance and preforms the commands

    :param int instance_id: ID of the instance to connect to
    :param str name: Identifier of this task
    :param cmds: The actual commands to run

    For example::

         perform.delay(1, 'destory', 'rm -rf /', 'echo everything gone')

         Will produce
         [root@10.0.0.1] output: rm -rf /
         [root@10.0.0.1] output: everything gone
    """
