from apps.authenticate.models import AuthUser
from django.core.exceptions import ObjectDoesNotExist

from services.auth_services.generate_tokens import PasswordResetToken
from services.cache.cache import RedisCacheMethods


class ResetPassword:
    """Класс восстановлнеия пароля."""

    @staticmethod
    def generate_content_for_reset_password(email: str) -> tuple:
        """Функция отправки сообщения на восстановление пароля.

        :param email:
        :return: tuple.
        """
        content = {}

        try:
            user = AuthUser.objects.get(email__exact=email)

        except ObjectDoesNotExist:
            return False, content
        token = PasswordResetToken().generate_token(user_id=user.id)
        RedisCacheMethods.set_reset_password_token(user.pk, token)

        content["token"] = token

        return True, content

    @staticmethod
    def reset_password_confirm(data: dict, token) -> tuple:
        """Функция смены пароля по ссылке.

        :param data:
        :param token:
        :return: bool.
        """
        payload = PasswordResetToken().decode_token(token)

        if not PasswordResetToken().check_token_type(payload):
            message = "Неверный тип токена."
            return False, message

        pk = payload.get("id")
        token_redis = RedisCacheMethods.get_reset_password_token(pk)
        if token_redis and (token_redis != token):
            return False, "Не валидный токен"
        try:
            user = AuthUser.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return False, "Данный пользователь не зарегистрирован"

        password = data.get("password1")
        user.set_password(password)
        user.save()
        return True, "Password has been changed"
