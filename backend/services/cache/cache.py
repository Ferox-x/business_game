from django.core.cache import cache


class RedisCacheMethods:
    """Методы для работы с Redis."""

    INVITE_CODE_TIME = 7200
    RESET_PASSWORD_TOKEN_TIME = 86400
    RESET_PASSWORD_KEY_TEMPLATE = "reset_token_"
    INVITE_CODE_KEY_TEMPLATE = "invite_code_"

    @classmethod
    def set_reset_password_token(cls, key: int, value: str):
        """Метод инициализации нового ключа для токена смены пароля."""
        cache.set(
            "".join((cls.RESET_PASSWORD_KEY_TEMPLATE, str(key))),
            value,
            cls.RESET_PASSWORD_TOKEN_TIME,
        )

    @classmethod
    def get_reset_password_token(cls, key: int):
        """Методы для получения значения ключа токена смены пароля."""
        return cache.get("".join((cls.RESET_PASSWORD_KEY_TEMPLATE, str(key))))

    @classmethod
    def set_invite_code(cls, value: str):
        """Метод инициализации ключа для инвайт кода."""
        cache.set(
            "".join((cls.INVITE_CODE_KEY_TEMPLATE, value)), value, cls.INVITE_CODE_TIME
        )

    @classmethod
    def get_invite_code(cls, key: str):
        """Метод для получения значения ключа инвайт кода."""
        return cache.get("".join((cls.INVITE_CODE_KEY_TEMPLATE, key)))
