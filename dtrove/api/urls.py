from django.conf.urls import patterns, url, include

from .views import DatastoreDetail, DatastoreList
from .views import ClusterDetail, ClusterList


datastore_urls = patterns(
    '',
    url(r'/(?P<pk>\d+)$', DatastoreDetail.as_view(), name='datastore-detail'),
    url(r'', DatastoreList.as_view(), name='datastore-list')
)

cluster_urls = patterns(
    '',
    url(r'^/(?P<pk>\d+)$', ClusterDetail.as_view(), name='cluster-detail'),
    url(r'^$', ClusterList.as_view(), name='cluster-list')
)

urlpatterns = patterns(
    '',
    url(r'^datastores', include(datastore_urls)),
    url(r'^clusters', include(cluster_urls)),
)
