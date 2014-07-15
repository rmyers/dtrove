"""
Serializers
===========

Turn our models into objects that are consumed by the api routes.
"""

from rest_framework import serializers

from dtrove.models import Cluster, Instance, Datastore


class DatastoreSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.Field(source='name')

    class Meta:
        model = Datastore
        fields = ['id', 'name', 'version', 'url']


class ClusterSerializer(serializers.ModelSerializer):
    datastore = DatastoreSerializer(read_only=True)
    datastore_id = serializers.PrimaryKeyRelatedField(source='datastore',
                                                      write_only=True)

    class Meta:
        model = Cluster
        fields = ['id', 'name', 'size', 'datastore', 'datastore_id', 'created']
