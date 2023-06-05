from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from foodgram import const
from foodgram.validators import validate_slug


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        'Название',
        max_length=const.STANDARD_LENGTH,
        db_index=True
    )
    measurement_unit = models.CharField(
        'Единицы измерения',
        max_length=const.STANDARD_LENGTH
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self) -> str:
        return f'{self.name}'


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=const.STANDARD_LENGTH,
        unique=True
    )
    color = models.CharField(
        'Цвет в HEX',
        max_length=const.HEX_LENGTH,
        unique=True
    )
    slug = models.CharField(
        'Слаг',
        max_length=const.STANDARD_LENGTH,
        validators=(validate_slug,),
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self) -> str:
        return f'{self.name}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор'
    )
    name = models.CharField('Название', max_length=const.STANDARD_LENGTH)
    image = models.ImageField('Картинка, закодированная в Base64')
    text = models.TextField('Описание', help_text='Заполните описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='AmountOfIngredient',
        verbose_name='Список ингредиентов'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Список id тегов'
    )
    cooking_time = models.PositiveIntegerField(
        'Время приготовления (в минутах)',
        validators=(MinValueValidator(
            1,
            message='Время приготовления не может быть меньше одной минуты!'
        ),)
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('name',)

    def __str__(self) -> str:
        return f'{self.name}. Автор: {self.author.username}'


class AmountOfIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    amount = models.PositiveIntegerField(
        'Количество',
        validators=(MinValueValidator(
            1,
            message='Количество не может быть меньше единицы!'
        ),)
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return (
            f'{self.ingredient.name} - {self.amount}'
            f' ({self.ingredient.measurement_unit})'
        )


class Favourite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    date_added = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        editable=False
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self) -> str:
        return f'{self.user} -> {self.recipe}'


class Cart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепты в списке покупок',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        verbose_name='Владелец списка',
        on_delete=models.CASCADE,
    )
    date_added = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        editable=False
    )

    class Meta:
        verbose_name = 'Рецепт в списке покупок'
        verbose_name_plural = 'Рецепты в списке покупок'

    def __str__(self) -> str:
        return f'{self.user} -> {self.recipe}'
