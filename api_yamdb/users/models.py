from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_moderator = models.BooleanField(
        verbose_name='Статус модератора',
        default=False
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
