from django.contrib import admin

from .models import Achievement


class AchievementAdmin(admin.ModelAdmin):

    pass


admin.site.register(Achievement, AchievementAdmin)
