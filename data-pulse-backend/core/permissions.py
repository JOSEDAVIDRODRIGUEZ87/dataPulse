from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    """Permiso exclusivo para Administradores."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == "ADMIN"


class IsAnalistaRole(permissions.BasePermission):
    """Permiso para Analistas y Administradores (Jerarquía)."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol in [
            "ADMIN",
            "ANALISTA",
        ]


class IsViewerRole(permissions.BasePermission):
    """Permiso para todos los roles (lectura)."""

    def has_permission(self, request, view):
        return request.user.is_authenticated  # VIEWER es el default
