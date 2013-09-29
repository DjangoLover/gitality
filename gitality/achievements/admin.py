from django.contrib import admin

from .models import Achievement


class RequirementsInline(admin.TabularInline):

    model = Achievement.requirements.through
    raw_id_fields = ('kvs',)


class AchievementAdmin(admin.ModelAdmin):

    exclude = ('requirements',)
    inlines = (RequirementsInline,)


admin.site.register(Achievement, AchievementAdmin)
