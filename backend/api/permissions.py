from rest_framework import permissions


class RecipePermission(permissions.BasePermission):
    """Permission for RecipeViewSet."""

    def has_permission(self, request, view):
        return (request.method == 'GET' or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method == 'GET' or obj.author == request.user
                or request.user.is_staff)
