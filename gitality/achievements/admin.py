from django.contrib import admin

from .models import (
    Achievement,
    CommitAchievement,
    CommitAuthorAchievement,
    ProjectAchievement
)


class RequirementsInline(admin.TabularInline):

    model = Achievement.requirements.through
    raw_id_fields = ('kvs',)


class AchievementAdmin(admin.ModelAdmin):

    exclude = ('requirements',)
    inlines = (RequirementsInline,)


class CommitAchievementAdmin(admin.ModelAdmin):

    list_select_related = True


class CommitAuthorAchievementAdmin(admin.ModelAdmin):

    list_select_related = True


class ProjectAchievementAdmin(admin.ModelAdmin):

    list_select_related = True


admin.site.register(Achievement, AchievementAdmin)
admin.site.register(CommitAchievement, CommitAchievementAdmin)
admin.site.register(CommitAuthorAchievement, CommitAuthorAchievementAdmin)
admin.site.register(ProjectAchievement, ProjectAchievementAdmin)
