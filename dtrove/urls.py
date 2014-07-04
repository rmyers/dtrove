from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = patterns(
    '',
    url(r'^$', 'dtrove.views.home', name='home'),
    url(r'^signin/$', auth_views.login, name="signin"),
    url(r'^admin/', include(admin.site.urls)),
)
