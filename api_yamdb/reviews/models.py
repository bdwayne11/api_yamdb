from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

from .validators import validate_year

ROLE_CHOICES = [
    ('user', 'user'),
    ('admin', 'admin'),
    ('moderator', 'moderator')
]


class User(AbstractUser):
    username = models.CharField(
        max_length=120,
        unique=True,
        blank=False,
        null=False,
    )
    password = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        max_length=50,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        'Роль',
        max_length=25,
        choices=ROLE_CHOICES,
        default='user',
        blank=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=50,
        blank=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=70,
        blank=True,
    )
    biography = models.TextField(
        'Биография',
        blank=True,
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=255,
        null=True,
        blank=False,
        default='****',
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Genre(models.Model):
    name = models.CharField(
        'Жанр',
        max_length=120,
        blank=False,
        null=False,
    )
    slug = models.SlugField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=120,
        blank=False,
        null=False,
    )
    slug = models.SlugField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=120,
        blank=False,
        null=False,
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        help_text='Введите категорию произведения',
        null=True,
        blank=True,
        related_name='titles'
    )
    description = models.TextField(null=True, verbose_name='Описание')
    year = models.TimeField(
        'Год выпуска',
        help_text='Введите год релиза',
        validators=(validate_year,)
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True,
    )
    text = models.TextField()
    rating = models.IntegerField(
        'Рейтинг',
        default=0,
        validators=[
            MinValueValidator(1, message='Оценка не может быть ниже 1'),
            MaxValueValidator(10, message='Оценка не может быть выше 10')
        ]
    )

    class Meta:
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_rev'
            )
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    text = models.TextField()

    def __str__(self):
        return self.text[:20]
