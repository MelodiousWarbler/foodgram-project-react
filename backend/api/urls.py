from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet


router = DefaultRouter()

router.register(r'tags', TagViewSet, 'tag')
router.register(r'ingredients', IngredientViewSet, 'ingredient')
router.register(r'recipes', RecipeViewSet, 'recipe')
router.register(r'users', UserViewSet, 'user')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
