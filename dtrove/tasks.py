"""
Tasks
============

These handle all the remote operations that happen. Such as building a new
cluster, or run a scheduled backup. We are using celery as our worker
daemon, giving us a powerful system to schedule or chain tasks together.

Execution Tasks
---------------

We can use the `perform` task to run any command on the remote systems.

.. py:function:: dtrove.tasks.perform(instance_id, name, *cmds)

    Execute a remote task

    :param int instance_id: ID of the instance to connect to
    :param str name: Identifier of this task
    :param str cmds: The actual commands to run

    For example (To ruin someones day)::

         perform.delay(1, 'destory', 'rm -rf /', 'echo everything gone')

         Will produce
         [root@10.0.0.1] run: rm -rf /
         out:
         [root@10.0.0.1] run: echo everything gone
         out: everything gone
         Disconnecting from 127.0.0.1...
         done.

Build Tasks
-----------

These tasks handle creating and managing the servers themselves.

.. py:function:: dtrove.tasks.create_server(instance_id, volume_id=None)

    Create a nova server instance

    :param int instance_id: ID of the instance to build
    :param str volume_id: Optional volume id to attach


.. py:function:: dtrove.tasks.create_volume(instance_id)

    Create a volume for the instance

    :param int instance_id: ID of the instance


.. py:function:: dtrove.tasks.attach_volume(instance_id, volume_id)

    Attach a volume to a nova server instance

    :param int instance_id: ID of the instance to build
    :param str volume_id: Optional volume id to attach

"""

from __future__ import absolute_import

from celery import shared_task
from fabric.api import run, env, settings, prefix
from fabric.network import disconnect_all

from dtrove import config
from dtrove.models import Instance


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
    """Connects to the instance and preforms the commands"""
    instance = Instance.objects.get(pk=instance_id)

    with settings(**instance.connection_info):
        map(run, cmds)

    # Always remember to disconnect ssh sessions
    disconnect_all()
