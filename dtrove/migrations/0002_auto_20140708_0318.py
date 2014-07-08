# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dtrove', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('user', models.CharField(default=b'root', max_length=25)),
                ('addr', models.GenericIPAddressField(null=True, blank=True)),
                ('server', models.CharField(help_text=b'Nova server UUID', max_length=36, blank=True)),
                ('cluster', models.ForeignKey(to='dtrove.Cluster')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Key',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('passphase', models.CharField(max_length=512, blank=True)),
                ('private', models.TextField(blank=True)),
                ('public', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='instance',
            name='key',
            field=models.ForeignKey(blank=True, to='dtrove.Key', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cluster',
            name='size',
            field=models.IntegerField(default=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='datastore',
            name='manager_class',
            field=models.CharField(max_length=255, choices=[(b'dtrove.datastores.mysql.MySQLManager', b'mysql'), (b'dtrove.datastores.redis.RedisManager', b'redis'), (b'dtrove.datastores.pgsql.PostgresManager', b'postgres')]),
        ),
    ]
