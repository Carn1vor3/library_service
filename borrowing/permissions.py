from rest_framework import permissions


class BorrowingPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ["POST", "GET"] and request.user and request.user.is_authenticated:
            return True
        if request.user and request.user.is_staff:
            return True
        return False
