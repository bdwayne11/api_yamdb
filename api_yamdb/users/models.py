from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_CHOICES = [
    (USER, 'user'),
    (ADMIN, 'admin'),
    (MODERATOR, 'moderator')
]


class User(AbstractUser):
    email = models. EmailField(
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    is_moderator = models.BooleanField(
        verbose_name='Статус модератора',
        default=False
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(choices=ROLE_CHOICES, max_length=20,
                            default=USER, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
