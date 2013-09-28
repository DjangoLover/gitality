from django.contrib import admin

from .models import Project


class ProjectAdmin(admin.ModelAdmin):

    list_select_related = True


admin.site.register(Project, ProjectAdmin)
