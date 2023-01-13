from django.urls import include, path
from rest_framework import routers

from src.ingredients.views import IngredientViewSet
from src.recipes.views import RecipeViewSet
from src.tags.views import TagViewSet
from src.users.views import UsersViewSet

router = routers.SimpleRouter()

router.register('users', UsersViewSet, basename='users')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
