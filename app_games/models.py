from django.db import models


def image_directory_path(instance, filename):
    return f'covers/{instance.title} {filename}'


# Create your models here.
class GameModel(models.Model):
    author = models.CharField(max_length=50, unique=True, verbose_name='Автор')
    image = models.ImageField(upload_to=image_directory_path, verbose_name='Обложка')
    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=200, verbose_name='URL')
    description = models.TextField(default='Coming Soon', verbose_name='Описание')
    release_date = models.DateField(null=True, blank=True, verbose_name='Дата выхода')
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name='Скидка в %')

    class Meta:
        db_table = 'games'
        verbose_name = 'Игру'
        verbose_name_plural = 'Игры'
        ordering = ('title',)

    # def get_absolute_url(self):
    #     return reverse("", kwargs={"": self.slug})

    def __repr__(self) -> str:
        return f'Game(id:{self.pk}, title:{self.title}, author:{self.author})'

    def __str__(self):
        return f'{self.title} ({self.author})'