from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from foodgram import const
from users.models import User


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
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient_unit'
            )
        ]

    def __str__(self) -> str:
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=const.STANDARD_LENGTH,
        unique=True
    )
    color = ColorField(
        'Цвет в HEX',
        max_length=const.HEX_LENGTH,
        unique=True
    )
    slug = models.SlugField(
        'Слаг',
        max_length=const.STANDARD_LENGTH,
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
        related_name='recipes',
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
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления (в минутах)',
        validators=(
            MinValueValidator(
                1,
                'Время приготовления не может быть меньше одной минуты!'
            ), (MaxValueValidator(
                const.MAX_VALUE,
                'Время приготовления не может быть больше недели!'
            ))
        )
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
        related_name='ingredientinrecipe',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=(
            MinValueValidator(
                1, message='Количество не может быть меньше единицы!'
            ), (MaxValueValidator(
                const.MAX_VALUE, message='Никто столько не съест!'
            ))
        )
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return f'{self.ingredient}-{self.recipe}'


class UserRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='%(app_label)s_%(class)s_unique'
            )
        ]

    def __str__(self) -> str:
        return f'{self.user} -> {self.recipe}'


class Favorite(UserRecipe):
    class Meta(UserRecipe.Meta):
        default_related_name = 'favorites'
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'


class Cart(UserRecipe):
    date_added = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        editable=False
    )

    class Meta(UserRecipe.Meta):
        default_related_name = 'shopping'
        verbose_name = 'Рецепт в списке покупок'
        verbose_name_plural = 'Рецепты в списке покупок'
