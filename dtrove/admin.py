
from django.contrib import admin
from .models import Datastore, Cluster, Key, Instance


@admin.register(Datastore, Cluster, Key, Instance)
class DtroveAdmin(admin.ModelAdmin):
    pass
