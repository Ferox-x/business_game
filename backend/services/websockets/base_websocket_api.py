import json
from abc import ABC

from channels.generic.websocket import JsonWebsocketConsumer


class BaseWebsocketInit(JsonWebsocketConsumer, ABC):
    """Базовый класс с инициализацией."""

    def __init__(self, *args, **kwargs):
        """Инициализация."""
        super().__init__(args, kwargs)
        self.user = None
        self.action = None
        self.data = None


class BaseWebsocketAPI(BaseWebsocketInit, ABC):
    """Базовый класс для вебсокетов, вызывающий action."""

    def connect(self):
        """Подключение к вебсокету."""
        self.accept()

    def disconnect(self, close_code):
        """Отключение от вебсокета."""
        self.close()


class BaseWebsocketPermissions(BaseWebsocketInit, ABC):
    """Базовый класс для прав доступа."""

    action_and_permissions = {}

    def check_permission(self):
        """Проверка прав доступа."""
        for result_check in self._get_permissions():
            if not result_check:
                return self.send_json({"message": "access denied"})

        return True

    def _get_permissions(self):
        """Метод проверяющий права доступа."""
        permissions = self.action_and_permissions[self.action]

        access = [permission(self.user) for permission in permissions]

        return access

    def receive(self, text_data):
        """Получение сообщения."""
        text_data = json.loads(text_data)
        self.data = text_data.get("data")
        self.action = text_data.get("action")

        try:
            if self.check_permission():
                method = getattr(self, f"action_{self.action}")
                method()
        except AttributeError:
            pass


class WebsocketActionAPI(BaseWebsocketAPI, BaseWebsocketPermissions):
    """Класс для взаимодействия с вебсокетами."""

    pass
