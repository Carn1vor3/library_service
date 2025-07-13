from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class PaymentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS and request.user and request.user.is_authenticated:
            return True
        if request.user and request.user.is_staff:
            return True
        return False