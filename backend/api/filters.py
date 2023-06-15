from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from recipes.models import Ingredient, Recipe, Tag


class IngredientSearch(SearchFilter):
    search_param = 'name'

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favourited = filters.BooleanFilter(
        method='filter_is_favourited',
        label='В избранном'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart',
        label='В списке покупок'
    )

    class Meta:
        model = Recipe
        fields = (
            'is_favourited',
            'is_in_shopping_cart',
            'author',
            'tags'
        )

    def filter_is_favourited(self, queryset, name, value):
        user = self.request.user.pk
        if value and user:
            return queryset.filter(favourite__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user.pk
        if value and user:
            return queryset.filter(shopping__user=user)
        return queryset
