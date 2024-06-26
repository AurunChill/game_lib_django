from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


def image_directory_path(instance, filename):
    return f'users/{instance.username} {filename}'


class UserModel(AbstractUser):
    image = models.ImageField(upload_to=image_directory_path, blank=True, null=True, verbose_name='Аватар')

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={"username": self.username})

    def __repr__(self) -> str:
        return f'User(id:{self.pk}, username:{self.username})'

    def __str__(self):
        return self.username