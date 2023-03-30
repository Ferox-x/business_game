from abc import ABC, abstractmethod
from datetime import datetime, timedelta

import jwt
from django.conf import settings


class JWTTokensBase(ABC):
    """Абстрактный класс для создания JWT токенов.

    Для использования необходимо переопределить метод _get_payload_token,
    который должен возвращать dict.

    Так же необходимо переопределить life_time,
    время жизни указывается в минутах.
    """

    _SECRET_KEY = settings.SECRET_KEY
    life_time = 0
    token_type = ""

    def decode_token(self, token):
        """Метод декодирования токена."""
        payload = jwt.decode(token, self._SECRET_KEY, algorithms=["HS256"])
        return payload

    def generate_token(self, **kwargs):
        """Генерирует токен."""
        payload = self._get_payload_token(kwargs)
        token = self._generate_jwt_token(payload=payload)

        return token

    def _generate_jwt_token(self, payload):
        """Генерирует JWT токен исходя из переданного payload.

        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена зависит от параметра life_time.
        """
        if self.life_time == 0:
            raise ValueError("life_time не может быть равен 0.")

        dt = datetime.now() + timedelta(minutes=self.life_time)

        payload["exp"] = dt
        token = jwt.encode(payload, self._SECRET_KEY, algorithm="HS256")

        return token

    @classmethod
    @abstractmethod
    def _get_payload_token(cls, kwargs) -> dict:
        """Переопределить, получение payload для нового токен.

        Так же необходимо сделать проверку на правильность переданных ключей,
        в kwargs.
        """

    def check_token_type(self, payload: dict):
        """Метод проверяющий тип токена, на вход принимает нагрузку токена."""
        token_type = payload.get("type", False)

        if token_type and token_type == self.token_type:
            return True
        return False


class AccessToken(JWTTokensBase):
    """Класс access токена."""

    life_time = 1000
    token_type = "access"

    def generate_token(self, user_id, user_role_id):
        """Генерирует токен."""
        return super().generate_token(user_id=user_id, user_role_id=user_role_id)

    @classmethod
    def _get_payload_token(cls, kwargs) -> dict:
        """Переопределить, получение payload для нового токен."""
        user_id = kwargs.get("user_id")
        user_role_id = kwargs.get("user_role_id")

        return {"id": user_id, "role": user_role_id, "type": cls.token_type}


class RefreshToken(JWTTokensBase):
    """Класс refresh токена."""

    life_time = 60 * 24
    token_type = "refresh"

    def generate_token(self, user_id):
        """Генерирует токен."""
        return super().generate_token(user_id=user_id)

    @classmethod
    def _get_payload_token(cls, kwargs) -> dict:
        """Переопределить, получение payload для нового токен."""
        user_id = kwargs.get("user_id")

        return {"id": user_id, "type": cls.token_type}


class PasswordResetToken(JWTTokensBase):
    """Класс password reset токена."""

    life_time = 25
    token_type = "password_reset"

    def generate_token(self, user_id):
        """Генерирует токен."""
        return super().generate_token(user_id=user_id)

    @classmethod
    def _get_payload_token(cls, kwargs) -> dict:
        user_id = kwargs.get("user_id")

        return {"id": user_id, "type": cls.token_type}
