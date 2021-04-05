import datetime as dt

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


def now_year():
    return dt.datetime.now().year


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    email = models.EmailField(
        _('email адрес'),
        unique=True
    )
    confirmation_code = models.CharField(
        _('код доступа к токену'),
        max_length=40,
        blank=True,
        null=True
    )
    bio = models.CharField(
        _('о себе'),
        max_length=400,
        blank=True,
        null=True
    )
    role = models.CharField(
        _('Права'),
        max_length=9,
        choices=Roles.choices,
        default=Roles.USER
    )

    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')

    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.Roles.ADMIN

    @property
    def is_moderator(self):
        return self.is_admin or self.role == self.Roles.MODERATOR


class Category(models.Model):
    name = models.CharField(max_length=30,
                            verbose_name=_('Название категории'))
    slug = models.SlugField(unique=True,
                            verbose_name=_('URL адрес категории'))

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

    def __str__(self):
        return self.slug[:20]


class Genre(models.Model):
    name = models.CharField(max_length=40,
                            verbose_name=_('Название жанра'))
    slug = models.SlugField(unique=True,
                            max_length=30,
                            verbose_name=_('URL адрес жанра'))

    class Meta:
        verbose_name = _('Жанр')
        verbose_name_plural = _('Жанры')

    def __str__(self):
        return self.slug[:20]


class Title(models.Model):
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 blank=True,
                                 null=True,
                                 related_name='titles',
                                 verbose_name=_('Категория произведения')
                                 )
    genre = models.ManyToManyField(Genre,
                                   blank=True,
                                   related_name='titles',
                                   related_query_name='genres',
                                   verbose_name=_('Жанр произведения')
                                   )
    name = models.CharField(max_length=50,
                            verbose_name=_('Название произведения'))
    year = models.PositiveIntegerField(blank=True,
                                       null=True,
                                       db_index=True,
                                       verbose_name=_(
                                           'Год выпуска произведения'),
                                       validators=[
                                           MaxValueValidator(
                                               now_year)
                                       ])
    description = models.TextField(blank=True,
                                   null=True,
                                   verbose_name=_('Описание произведения')
                                   )

    class Meta:
        verbose_name = _('Произведение')
        verbose_name_plural = _('Произведения')

    def __str__(self):
        return self.name[:20]


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField(
        verbose_name=_('Содержание отзыва')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('Автор отзыва')
    )
    score = models.PositiveSmallIntegerField(
        verbose_name=_('Оценка от 1 до 10'),
        validators=[MinValueValidator(1, 'Не может быть меньше 1'),
                    MaxValueValidator(10, 'Не может быть больше 10')
                    ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата отзыва')
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = _('отзыв')
        verbose_name_plural = _('отзывы')
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='onereviewpertitle'
            )
        ]

    def __str__(self):
        return self.text[:20]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата комментария'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return self.text[:20]
