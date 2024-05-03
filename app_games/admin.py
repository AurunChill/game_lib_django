from django.contrib import admin

# Project
from app_games import models


@admin.register(models.GameModel)
class GameModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'author', 'release_date', 'price', 'discount',)
    list_editable = ['discount',]
    search_fields = ['title', 'author', 'price', 'discount']
    list_filter = ['discount']
    fields = ('author', 'image', 'title', 'slug', 'description', 'release_date', 'price', 'discount',)
