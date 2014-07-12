"""
Serializers
===========

Turn our models into objects that are consumed by the api routes.
"""

from rest_framework import serializers

from dtrove.models import Cluster, Instance, Datastore


class DatastoreSerializer(serializers.ModelSerializer):
    name = serializers.Field(source='name')

    class Meta:
        model = Datastore
        fields = ['id', 'name', 'version']


class ClusterSerializer(serializers.ModelSerializer):
    datastore = DatastoreSerializer()

    class Meta:
        model = Cluster
        fields = ['id', 'name', 'size', 'datastore', 'created']
