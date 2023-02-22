from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsCoordinator(BasePermission):
    """Доступ только для координатора."""

    def has_permission(self, request, view):
        """Метод проверки пользователя на координатора."""
        return bool(request.user and request.user.is_coordinator)


class IsPlayer(BasePermission):
    """Доступ только для игрока."""

    def has_permission(self, request, view):
        """Метод проверки пользователя на игрока."""
        return bool(request.user and request.user.is_player)


class GamePlayer(BasePermission):
    """Доступ только для игрока определённой игры."""

    def has_permission(self, request: Request, view):
        """."""
        pass
