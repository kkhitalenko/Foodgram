from api.views import CustomUserViewSet, IngredientViewSet, TagViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

v1_router = DefaultRouter()

v1_router.register(r'ingredients', IngredientViewSet, basename='ingredients')
v1_router.register(r'tags', TagViewSet, basename='tags')
v1_router.register(r'users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(v1_router.urls)),
    path('', include('djoser.urls')),
]
