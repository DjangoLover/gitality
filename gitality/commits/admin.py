from django.contrib import admin

from .models import Commit, CommitAuthor


class CommitAdmin(admin.ModelAdmin):

    pass


class CommitAuthorAdmin(admin.ModelAdmin):

    pass


admin.site.register(Commit, CommitAdmin)
admin.site.register(CommitAuthor, CommitAuthorAdmin)
