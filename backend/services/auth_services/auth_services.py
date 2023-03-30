from django.apps import apps


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
