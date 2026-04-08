import logging

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(getattr(obj, 'author', None) and obj.author.user_id == request.user.id)


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            getattr(obj, 'author', None) is not None
            and obj.author.user_id == request.user.id
        )

