from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from dtrove.forms import KeystoneForm


urlpatterns = patterns(
    'dtrove.views',
    url(r'^$', 'home', name='home'),
    # create a new cluster
    url(r'^cluster/$', 'cluster', name='cluster'),
    # cluster details
    url(r'^cluster/(?P<cluster_id>\d+)/', 'details', name='details'),
    url(r'^signout/$', auth_views.logout),
    url(r'^signin/$', auth_views.login,
        {'authentication_form': KeystoneForm},
        name="signin"),
    url(r'^admin/', include(admin.site.urls)),
)
