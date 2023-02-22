import random
import string

from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist

from services.cache.cache import RedisCacheMethods


class InviteCodeMethods:
    """Класс методов для инвайт кода."""

    @staticmethod
    def get_coordinator_id_by_invite_code(invite_code: str):
        """Метод для получения ID координатора по инвайт коду."""
        is_invite_code_valid = RedisCacheMethods.get_invite_code(invite_code)
        if not is_invite_code_valid:
            try:
                coordinator = apps.get_model("users.Coordinator")
                coordinator.objects.get(invite_code=invite_code)
                RedisCacheMethods.set_invite_code(invite_code)
            except ObjectDoesNotExist:
                return None
        coordinator_id = int(invite_code.split("-")[0])
        return coordinator_id

    @staticmethod
    def generate_invite_code(coordinator_id: int) -> str:
        """Метод генерации инвайт кодаю.

        :param coordinator_id:
        :return:
        """
        id_string = str(coordinator_id)
        id_string_len = len(id_string)
        random_part = "".join(
            [random.choice(string.ascii_letters) for _ in range(9 - id_string_len)]
        )
        invite_code = "-".join((id_string, random_part))
        return invite_code


class AuthRoles:
    """Класс для взаимодействия с ролями."""

    _coordinator_id = 2
    _player_id = 3

    def __init__(self):
        """Созадет инстанс класса AuthRoles, со словарем моделей."""
        self._roles = {
            self._coordinator_id: apps.get_model("users.Coordinator"),
            self._player_id: apps.get_model("users.Player"),
        }

    def get_roles(self):
        """Возвращает словарь ролей."""
        return self._roles

    def get_coordinator_role_id(self):
        """Возвращает ид роли координатора."""
        return self._coordinator_id

    def get_player_role_id(self):
        """Возвращает ид роли игрока."""
        return self._player_id

    def get_role_name(self, role_id):
        """Возвращает название роли."""
        name_roles = {
            self._coordinator_id: "Coordinator",
            self._player_id: "Player",
        }

        return name_roles.get(role_id)
