from django.db import IntegrityError
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import IngredientSearch, RecipeFilter
from api.pagination import Paginator
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.serializers import (
    CartSerializer, FavoriteSerializer, IngredientSerializer,
    RecipeReadSerializer, RecipeWriteSerializer, TagSerializer,
    UserWithRecipesSerializer, SubscriptionWriteSerializer
)
from recipes.models import (
    AmountOfIngredient, Cart, Favorite, Ingredient, Recipe, Tag
)
from users.models import Subscription, User


class UserViewSet(DjoserUserViewSet):
    pagination_class = Paginator
    http_method_names = ('get', 'post', 'delete')

    @action(
        # http_method_names=('post', 'delete'),
        methods=('POST',),
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        data = {
            'user': request.user.id,
            'author': author.id
        }
        serializer = SubscriptionWriteSerializer(
            data=data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscription(self, request, id=id):
        author = get_object_or_404(self.queryset, id=id)
        get_object_or_404(
            Subscription, author=author, user=self.request.user
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(subscribing__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = UserWithRecipesSerializer(
            page,
            context={'request': request},
            many=True
        )
        return self.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearch,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = Paginator
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ('get', 'post', 'patch', 'delete',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return RecipeWriteSerializer

    @staticmethod
    def add_to_list(serializer, pk, request):
        recipe = get_object_or_404(Recipe, pk=pk)
        context = {'request': request}
        data = {
            'user': request.user.id,
            'recipe': recipe.id
        }
        serializer = serializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_from_list(model, user, pk=None):
        get_object_or_404(
            model, user=user, pk=pk
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def shopping_list(request, ingredients):
        shopping_cart = [f'Список покупок {request.user}.\n']
        for ingredient in ingredients:
            shopping_cart.append(
                f'{ingredient["ingredient__name"]} - '
                f'{ingredient["amount"]} '
                f'{ingredient["ingredient__measurement_unit"]}\n'
            )
        file = f'{request.user}_shopping_cart.txt'
        response = HttpResponse(shopping_cart, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={file}'
        return response

    @action(
        methods=['POST'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        return self.add_to_list(FavoriteSerializer, pk, request)

    @favorite.mapping.delete
    def delete_from_favorite(self, request, pk=None):
        return self.delete_from_list(Favorite, request.user, pk)

    @action(
        methods=['POST'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        return self.add_to_list(CartSerializer, pk, request)

    @shopping_cart.mapping.delete
    def delete_from_shopping_cart(self, request, pk=None):
        return self.delete_from_list(Cart, request.user, pk)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        ingredients = (
            AmountOfIngredient.objects
            .filter(recipe__shopping__user=request.user)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(amount=Sum('amount'))
            .order_by('ingredient__name')
        )
        return self.shopping_list(request, ingredients)
