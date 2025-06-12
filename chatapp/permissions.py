# permissions.py
from rest_framework.permissions import BasePermission

class IsAdminUserOnly(BasePermission):
    """
    Allows access only to authenticated admin users (is_staff=True or is_superuser=True).
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff
