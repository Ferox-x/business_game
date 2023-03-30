from apps.authenticate.models import AuthUser
from channels.db import database_sync_to_async
from channels.exceptions import DenyConnection
from django.contrib.auth.models import AnonymousUser, User
from services.auth_services.auth_services import AuthRoles
from services.auth_services.generate_tokens import AccessToken


class TokenAuthMiddleware:
    """JWT валидация пользователя для вебсокета."""

    @classmethod
    def _header_token(cls, headers):
        """Метод достающий токен из заголовка."""
        for header in headers:
            if header[0].decode("utf8") == "authorization":
                return header[1].decode("utf8").split()[1]

    @classmethod
    @database_sync_to_async
    def _get_user(cls, model, payload):
        """Метод, получающий пользователя по полезной нагрузке из токена."""
        try:
            return model.objects.get(pk=payload["id"])
        except User.DoesNotExist:
            return AnonymousUser()

    def __init__(self, app):
        """Метод инициализации."""
        self.app = app

    async def __call__(self, scope, receive, send):
        """Метод вызова."""
        token = scope["query_string"][6:].decode("UTF-8")

        try:
            payload = AccessToken().decode_token(token)
        except Exception:
            msg = "Ошибка аутентификации. Невозможно декодировать токен."
            raise DenyConnection(msg)

        roles = AuthRoles().get_roles()

        model = roles.get(payload.get("role"), AuthUser)

        try:
            user = await self._get_user(model, payload)

        except AuthUser.DoesNotExist:
            msg = "Пользователь соответствующий данному токену не найден."
            raise DenyConnection(msg)

        scope["user"] = user

        return await self.app(scope, receive, send)
