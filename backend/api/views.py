from api.pagination import StandardResultsSetPagination
from djoser.views import UserViewSet


class CustomUserViewSet(UserViewSet):
    pagination_class = StandardResultsSetPagination
