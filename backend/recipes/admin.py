from django.contrib import admin
from django.contrib.auth.models import Group

from foodgram import const
from recipes.models import (
    AmountOfIngredient, Cart, Favorite, Ingredient, Recipe, Tag
)


admin.site.unregister(Group)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('measurement_unit',)
    empty_value_display = const.EMPTY


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color',)
    search_fields = ('name', 'slug',)
    ordering = ('color',)
    empty_value_display = const.EMPTY


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author',)
    list_filter = ('name', 'author', 'tags',)
    empty_value_display = const.EMPTY


@admin.register(AmountOfIngredient)
class AmountOfIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ingredient',
        'amount',
    )
    list_filter = ('ingredient',)
    ordering = ('ingredient',)
    empty_value_display = const.EMPTY


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
    empty_value_display = const.EMPTY


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'date_added',)
    list_filter = ('user', 'recipe', 'date_added',)
    empty_value_display = const.EMPTY
