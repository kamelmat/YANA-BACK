from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Permite el acceso solo a usuarios administradores (is_admin=True).
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin
