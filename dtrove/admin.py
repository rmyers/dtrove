
from django.contrib import admin
from .models import Datastore, Cluster


@admin.register(Datastore, Cluster)
class DtroveAdmin(admin.ModelAdmin):
    pass
