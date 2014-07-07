# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Datastore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('manager_class', models.CharField(max_length=255, choices=[(b'mysql', b'dtrove.datatores.mysql.MySQLManager'), (b'redis', b'dtrove.datatores.redis.RedisManager'), (b'postgres', b'dtrove.datatores.pgsql.PostgresManager')])),
                ('version', models.CharField(max_length=255)),
                ('image', models.CharField(max_length=255)),
                ('packages', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='cluster',
            name='datastore',
            field=models.ForeignKey(to='dtrove.Datastore'),
            preserve_default=True,
        ),
    ]
