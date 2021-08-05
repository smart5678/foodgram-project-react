from django.contrib import admin

from cart.models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'user')
    list_filter = ('recipe', 'user')
    fields = (('recipe', 'user'),)
    list_editable = ('recipe', 'user', )
    empty_value_display = '-пусто-'
