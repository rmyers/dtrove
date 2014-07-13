from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from dtrove.forms import KeystoneForm


urlpatterns = patterns(
    'dtrove.views',
    url(r'^api/', include('dtrove.api.urls')),
)
