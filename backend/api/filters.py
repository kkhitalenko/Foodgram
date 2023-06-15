from django_filters import rest_framework
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag


class IngredientSearch(SearchFilter):
    """Filter for ingredients."""

    search_param = 'name'


class RecipeFilter(rest_framework.FilterSet):
    """Filter for recipes."""

    author = rest_framework.CharFilter()
    tags = rest_framework.ModelMultipleChoiceFilter(
        field_name='tags__slug', queryset=Tag.objects.all(),
        to_field_name='slug'
    )
    is_favorited = rest_framework.BooleanFilter()
    is_in_shopping_cart = rest_framework.BooleanFilter()

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorite(self, queryset, name, value):
        if value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset
