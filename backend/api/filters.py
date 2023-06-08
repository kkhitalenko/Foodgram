from rest_framework.filters import SearchFilter


class IngredientSearch(SearchFilter):
    """Filter for ingredients."""

    search_param = 'name'
