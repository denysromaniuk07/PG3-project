from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Permission for users to modify their own profile"""
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsAuthor(permissions.BasePermission):
    """Permission for post authors"""
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Permission for post authors or read-only access"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsMentor(permissions.BasePermission):
    """Permission for mentor-only actions"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_mentor


class IsResumeOwner(permissions.BasePermission):
    """Permission for resume owners"""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsJobApplicationOwner(permissions.BasePermission):
    """Permission for job application owners"""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
