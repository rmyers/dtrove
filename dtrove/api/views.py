"""
API Views
=========

Mapping models and serialisers to Views.
"""

from rest_framework import generics, permissions

from dtrove.models import Datastore, Cluster
from .serializers import DatastoreSerializer, ClusterSerializer


class DatastoreList(generics.ListAPIView):
    model = Datastore
    serializer_class = DatastoreSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class DatastoreDetail(generics.RetrieveAPIView):
    model = Datastore
    serializer_class = DatastoreSerializer


class ClusterList(generics.ListCreateAPIView):
    model = Cluster
    serializer_class = ClusterSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class ClusterDetail(generics.RetrieveAPIView):
    model = Cluster
    serializer_class = ClusterSerializer
