from django.db import models
from django.urls import reverse

# Project
from app_users.models import UserModel


def image_directory_path(instance, filename):
    return f'covers/{instance.title} {filename}'


# Create your models here.
class GameModel(models.Model):
    author = models.ForeignKey(to=UserModel, on_delete=models.SET_NULL, null=True, related_name='user', verbose_name='Автор')
    image = models.ImageField(upload_to=image_directory_path, verbose_name='Обложка')
    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=200, verbose_name='URL')
    description = models.TextField(default='Coming Soon', verbose_name='Описание')
    release_date = models.DateField(null=True, blank=True, verbose_name='Дата выхода')
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name='Скидка в %')

    def total_price(self) -> float:
        return self.price - (self.price * self.discount / 100)

    class Meta:
        db_table = 'games'
        verbose_name = 'Игру'
        verbose_name_plural = 'Игры'
        ordering = ('title',)

    def get_absolute_url(self):
        return reverse('games:game_detail', kwargs={'author': self.author.username, 'game_slug': self.slug})

    def __repr__(self) -> str:
        return f'Game(id:{self.pk}, title:{self.title}, author:{self.author})'

    def __str__(self):
        return f'{self.title} ({self.author})'
    

class WishListModel(models.Model):
    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name='wishlist_user', verbose_name='Пользователь')
    game = models.ForeignKey(to=GameModel, on_delete=models.CASCADE, related_name='wishlist_game', verbose_name='Игра')

    class Meta:
        db_table = 'wishlist'
        verbose_name = 'Списку Желаемоего'
        verbose_name_plural = 'Списки Желаемого'
        ordering = ('id',)

    def __repr__(self) -> str:
        return f'Withlist(id:{self.pk}, user:{self.user.username}, game:{self.game.title})'

    def __str__(self):
        return f'{self.user.username} добавил {self.game.title} в список желаемого'