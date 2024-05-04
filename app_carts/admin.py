from django.contrib import admin
from django.contrib.auth import get_user_model

# Project
from app_carts import models
from app_games.models import GameModel


class UserInline(admin.StackedInline):
    model = get_user_model()
    verbose_name = 'Пользователь'
    can_delete = False


class GameInline(admin.StackedInline):
    model = GameModel
    verbose_name = 'Игра'
    can_delete = False


@admin.register(models.CartItemModel)
class CartItemModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'game')
    search_fields = ['user__username', 'game__name']  # Assuming 'username' in User and 'name' in Game
    list_filter = ['user', 'game']
    fields = ('user', 'game')

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super(CartItemModelAdmin, self).get_inline_instances(request, obj)