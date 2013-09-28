from django.contrib import admin

from .models import AuthorProgress, ProjectProgress


class AuthorProgressAdmin(admin.ModelAdmin):

    list_select_related = True


class ProjectProgressAdmin(admin.ModelAdmin):

    list_select_related = True


admin.site.register(AuthorProgress, AuthorProgressAdmin)
admin.site.register(ProjectProgress, ProjectProgressAdmin)
