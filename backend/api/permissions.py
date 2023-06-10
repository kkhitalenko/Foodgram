from rest_framework import permissions


class RecipePermission(permissions.BasePermission):
    """Permission for RecipeViewSet."""

    def has_object_permission(self, request, view, obj):
        return (request.method == 'GET' or
                request.method == 'POST' and request.user.is_authenticated or
                request.user == obj.author or
                request.user.is_admin)
