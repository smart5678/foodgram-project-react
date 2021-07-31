from django.contrib import admin

from social.models import Follow


@admin.register(Follow)
class FollowingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    empty_value_display = '-пусто-'