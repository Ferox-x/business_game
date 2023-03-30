import json
from abc import ABC

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from services.bussines_games.utils.game_utils import GameStates
from services.bussines_games.validators.action_validator import BaseAction


class BaseWebsocketInit(JsonWebsocketConsumer, ABC):
    """Базовый класс с инициализацией."""

    def __init__(self, *args, **kwargs):
        """Инициализация."""
        super().__init__(args, kwargs)
        self.user = None
        self.action = None
        self.data = None
        self.validated_data = None


class BaseWebsocketAPI(BaseWebsocketInit, ABC):
    """Базовый класс для вебсокетов, вызывающий action."""

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.game_group_id = None

    def connect(self):
        """Подключение к вебсокету."""
        self.accept()

    def disconnect(self, close_code):
        """Отключение от вебсокета."""
        self.close(code=close_code)

    def send_to_channel(
        self, channel_name, player=None, action=None, data=None, notice=None
    ):
        """Отправляет сообщение на конкретный канал."""
        if action:
            data_json = {"action": action}
        else:
            data_json = {"action": self.action}

        if data:
            data_json["data"] = data
        if notice:
            data_json["notice"] = notice
        if player and self.game.game_status != GameStates.lobby:
            data_json[
                "resources"
            ] = player.game_role.resources.to_json_trade_resources()

            try:
                possibilities = player.game_role.resources.get_possibilities()
                data_json["possibilities"] = possibilities
            except AttributeError:
                pass

        async_to_sync(self.channel_layer.send)(
            channel_name,
            {"type": "chat.message", "json": data_json},
        )

    def send_to_the_group(self, action=None, data=None, notice=None):
        """Отправляет сообщение в конкретную группу."""
        if action:
            data_json = {"action": action}
        else:
            data_json = {"action": self.action}

        if data:
            data_json["data"] = data
        if notice:
            data_json["notice"] = notice
        async_to_sync(self.channel_layer.group_send)(
            self.game_group_id,
            {
                "type": "chat.message",
                "json": data_json,
            },
        )

    def send_to_current_user(self, data):
        self.send_to_channel(self.channel_name, data)


class BaseWebsocketPermissions(BaseWebsocketInit, ABC):
    """Базовый класс для прав доступа."""

    action_and_permissions = {}

    def check_permission(self):
        """Проверка прав доступа."""
        for result_check in self._get_permissions():
            if not result_check:
                return self.send_json({"message": "access denied"})

        return True

    @classmethod
    def get_action_and_permissions(cls):
        attributes = dir(cls)

        attributes = [
            attribute
            for attribute in attributes
            if (
                attribute.endswith("action_and_permissions")
                and not attribute.endswith("get_action_and_permissions")
            )
        ]

        attributes = [getattr(cls, attribute) for attribute in attributes]

        action_and_permissions = {}

        for class_actions_and_permission in attributes:
            for action, permissions in class_actions_and_permission.items():
                action_and_permissions[action] = permissions

        return action_and_permissions

    def _get_permissions(self):
        """Метод проверяющий права доступа."""
        action_and_permissions = self.get_action_and_permissions()

        permissions = action_and_permissions[self.action]

        access = [permission(self) for permission in permissions]

        return access


class WebsocketActionAPI(BaseWebsocketAPI, BaseWebsocketPermissions):
    """Класс для взаимодействия с вебсокетами."""

    def _validate(self, validator, data):
        try:
            return validator.parse_obj(data)
        except ValueError:
            error = {"error": "Неверная data"}
            self.send_to_channel(self.channel_name, error)

    def receive(self, text_data):
        """Получение сообщения."""
        text_data = json.loads(text_data)
        self.data = text_data.get("data")
        self.action = text_data.get("action")

        try:
            BaseAction(action=f"action_{self.action}")
        except ValueError as ex:
            error = {"error": str(ex)}
            self.send_to_channel(self.channel_name, error)
        else:
            if self.check_permission():
                method = getattr(self, f"action_{self.action}")
                method()

    def chat_message(self, event):
        """Метод отправки сообщения в чат."""
        self.send_json(content=event["json"])
