from django.db import models

# Project
from app_users.models import UserModel
from app_games.models import GameModel


class CartItemModel(models.Model):
    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name='cart_user', verbose_name='Пользователь')
    game = models.ForeignKey(to=GameModel, on_delete=models.CASCADE, related_name='cart_game', verbose_name='Игра')

    class Meta:
        db_table = 'carts'
        verbose_name = 'Корзину'
        verbose_name_plural = 'Корзины'
        ordering = ('id',)

    def __repr__(self) -> str:
        return f'Cart(id:{self.pk}, user:{self.user.username}, game:{self.game.title})'

    def __str__(self):
        return f'{self.user.username} берет {self.game.title} в корзину'