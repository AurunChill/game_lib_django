from django.contrib import admin

# Project
from app_carts import models


@admin.register(models.CartItemModel)
class CartItemModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'game')
    search_fields = ['user__username', 'game__name']  # Assuming 'username' in User and 'name' in Game
    list_filter = ['user', 'game']
    fields = ('user', 'game')
