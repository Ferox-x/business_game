import logging

from rest_framework import authentication, exceptions
from services.auth_services.auth_services import AuthRoles
from services.auth_services.generate_tokens import AccessToken

from .models import AuthUser

logger = logging.getLogger()


class JWTAuthentication(authentication.BaseAuthentication):
    """Класс для JWT авторизации."""

    authentication_header_prefix = "Token"

    def authenticate(self, request):
        """Метод проверяющий Authorization заголовок.

        Метод authenticate вызывается каждый раз, независимо от того, требует
        ли того эндпоинт аутентификации. 'authenticate' имеет два возможных
        возвращаемых значения:
            1) None - мы возвращаем None если не хотим аутентифицироваться.
            Обычно это означает, что мы знаем, что аутентификация не удастся.
            Примером этого является, например, случай, когда токен не включен в
            заголовок.
            2) (user, token) - мы возвращаем комбинацию пользователь/токен
            тогда, когда аутентификация пройдена успешно. Если ни один из
            случаев не соблюден, это означает, что произошла ошибка, и мы
            ничего не возвращаем. В таком случае мы просто вызовем исключение
            AuthenticationFailed и позволим DRF сделать все остальное.
        """
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            return None

        elif len(auth_header) > 2:
            return None
        prefix = auth_header[0].decode("utf-8")
        token = auth_header[1].decode("utf-8")

        if prefix.lower() != auth_header_prefix:
            return None

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        """Метод авторизации.

        Попытка аутентификации с предоставленными данными. Если успешно -
        вернуть пользователя и токен, иначе - сгенерировать исключение.
        """
        try:
            payload = AccessToken().decode_token(token)
        except Exception:
            msg = "Ошибка аутентификации. Невозможно декодировать токен."
            raise exceptions.AuthenticationFailed(msg)

        if not AccessToken().check_token_type(payload):
            msg = "Ошибка аутентификации. Неверный тип токена."
            raise exceptions.AuthenticationFailed(msg)

        roles = AuthRoles().get_roles()

        model = roles.get(payload.get("role"), None)

        if not model:
            msg = "Пользователь соответствующий данной роле не найден."
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = model.objects.get(pk=payload["id"])
        except AuthUser.DoesNotExist:
            msg = "Пользователь соответствующий данному токену не найден."
            raise exceptions.AuthenticationFailed(msg)

        if not user:
            msg = "Пользователь не найден."
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = "Данный пользователь деактивирован."
            raise exceptions.AuthenticationFailed(msg)

        return user, token
