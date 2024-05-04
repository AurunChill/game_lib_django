from django.contrib import admin
from django.utils.safestring import mark_safe

# Project
from app_games import models


@admin.register(models.GameModel)
class GameModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('show_cover', 'title', 'author', 'release_date', 'price', 'discount',)
    list_editable = ['discount',]
    search_fields = ['title', 'author', 'price', 'discount']
    list_filter = ['discount']
    readonly_fields=['show_cover_big']
    fields = ('author', 'image', 'show_cover_big', 'title', 'slug', 'description', 'release_date', 'price', 'discount',)
    save_on_top = True

    @admin.display(description='Обложка')
    def show_cover(self, game: models.GameModel):
        if game.image:
            return mark_safe(f'<img src="{game.image.url}" style="border-radius: 10px" width=50>')
        return 'Нет обложки'

    @admin.display(description='Обложка (Фото)')
    def show_cover_big(self, game: models.GameModel):
        if game.image:
            return mark_safe(f'<img src="{game.image.url}" style="border-radius: 10px" width=250>')
        return 'Нет обложки'
