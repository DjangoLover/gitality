from django.contrib import admin

from .models import Commit, CommitAuthor


class CommitAdmin(admin.ModelAdmin):

    list_select_related = True


class CommitAuthorAdmin(admin.ModelAdmin):

    pass


admin.site.register(Commit, CommitAdmin)
admin.site.register(CommitAuthor, CommitAuthorAdmin)
