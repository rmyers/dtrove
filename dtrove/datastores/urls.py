from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^v1$', 'dtrove.database.home', name='home'),
)
