from django.contrib import admin

from social.models import Favorite, Follow


@admin.register(Follow)
class FollowingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'favorite_recipe')
    empty_value_display = '-пусто-'
