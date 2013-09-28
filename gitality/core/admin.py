from django.contrib import admin

from .models import KVS


class KVSAdmin(admin.ModelAdmin):

    pass


admin.site.register(KVS, KVSAdmin)
