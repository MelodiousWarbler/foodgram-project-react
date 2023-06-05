from django.contrib.auth.models import AbstractUser
from django.db import models

from foodgram import const
from foodgram.validators import validate_username


class MyUser(AbstractUser):
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=const.EMAIL_LENGTH,
        unique=True,
    )
    username = models.CharField(
        'Уникальный юзернейм',
        max_length=const.USER_STANDARD_FIELD_LENGTH,
        validators=(validate_username,),
        unique=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=const.USER_STANDARD_FIELD_LENGTH,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=const.USER_STANDARD_FIELD_LENGTH,
    )
    password = models.CharField(
        'Пароль',
        max_length=const.USER_STANDARD_FIELD_LENGTH,
    )
    # is_active = models.BooleanField(
    #     'Активен',
    #     default=True,
    # )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self) -> str:
        return f'{self.username}: {self.email}'


class Subscription(models.Model):
    author = models.ForeignKey(
        MyUser,
        verbose_name='Автор рецепта',
        related_name='subscribers',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        MyUser,
        verbose_name='Подписчики',
        related_name='subscriptions',
        on_delete=models.CASCADE,
    )
    date_added = models.DateTimeField(
        'Дата создания подписки',
        auto_now_add=True,
        editable=False
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self) -> str:
        return f'{self.user.username} -> {self.author.username}'
