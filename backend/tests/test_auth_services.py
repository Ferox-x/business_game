from datetime import datetime, timedelta
from unittest import TestCase

import jwt
from apps.users.models import Coordinator, Player
from django.conf import settings
from services.auth_services.auth_services import AuthRoles
from services.auth_services.generate_tokens import JWTTokens


class AuthRolesTests(TestCase):
    """Класс тестирования AuthRoles."""

    @classmethod
    def setUpClass(cls) -> None:
        """Данные тестирования."""
        cls.auth_roles = AuthRoles()
        cls.true_coordinator_role_id = 2
        cls.true_player_role_id = 3

    def test_get_roles(self):
        """Тестирование метода get_roles."""
        roles = self.auth_roles.get_roles()

        roles_dict_error = "Метод get_roles должен возвращать словарь ролей."

        self.assertIsInstance(roles, dict, roles_dict_error)

    def test_init(self):
        """Тестирование метода __init__."""
        roles = self.auth_roles.get_roles()

        model_coordinator = roles.get(self.true_coordinator_role_id)
        model_player = roles.get(self.true_player_role_id)

        coordinator_error = "ID 2 роли должен принадлежать модели координатора."
        player_error = "ID 3 роли должен принадлежать модели игрока."

        self.assertEqual(model_coordinator, Coordinator, coordinator_error)
        self.assertEqual(model_player, Player, player_error)

    def test_coordinator_role_id(self):
        """Тестирование метода get_coordinator_role_id."""
        testing_coordinator_role_id = self.auth_roles.get_coordinator_role_id()

        coordinator_id_error = "ID роли координатора должен быть 2"

        self.assertEqual(
            self.true_coordinator_role_id,
            testing_coordinator_role_id,
            coordinator_id_error,
        )

    def test_player_role_id(self):
        """Тестирование метода get_player_role_id."""
        testing_player_role_id = self.auth_roles.get_player_role_id()

        player_id_error = "ID роли игрока должен быть 3"

        self.assertEqual(
            self.true_player_role_id, testing_player_role_id, player_id_error
        )


class JWTTokensTests(TestCase):
    """Класс тестирования JWTTokens."""

    @classmethod
    def setUpClass(cls) -> None:
        """Данные тестирования."""
        cls.jwt_tokens = JWTTokens
        cls.SECRET_KEY = settings.SECRET_KEY
        cls.ACCESS_LIFE_TIME = 1
        cls.REFRESH_LIFE_TIME = 30

    @classmethod
    def setUp(cls) -> None:
        """Данные тестирования."""
        cls.user_id = 1
        cls.user_role_id = 2

    def test_generate_access_token(self):
        """Тестирование метода generate_access_token."""
        access_token = self.jwt_tokens().generate_access_token(
            self.user_id, self.user_role_id
        )
        payload = jwt.decode(access_token, self.SECRET_KEY, algorithms=["HS256"])

        testing_user_id = payload.get("id")
        testing_user_role_id = payload.get("role")

        user_id_error = "Ошибка генерации access токена. (Неверный id пользователя)"
        user_role_id_error = "Ошибка генерации access токена. (Неверный id роли)"

        self.assertEqual(testing_user_id, self.user_id, user_id_error)
        self.assertEqual(testing_user_role_id, self.user_role_id, user_role_id_error)

    def test_generate_refresh_token(self):
        """Тестирование метода generate_refresh_token."""
        refresh_token = self.jwt_tokens().generate_refresh_token(self.user_id)
        payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=["HS256"])

        testing_refresh_key = payload.get("refresh")

        refresh_key_error = "Ошибка генерации refresh токена. (Неверный refresh key)"

        self.assertTrue(testing_refresh_key, refresh_key_error)

    def test_decode_token(self):
        """Тестирование метода decode_token."""
        payload = {"id": self.user_id, "role": self.user_role_id}
        dt = datetime.now() + timedelta(days=self.ACCESS_LIFE_TIME)

        payload["exp"] = dt
        testing_token = jwt.encode(payload, self.SECRET_KEY, algorithm="HS256")

        testing_payload = self.jwt_tokens().decode_token(testing_token)

        testing_user_id = testing_payload.get("id")
        testing_user_role_id = testing_payload.get("role")

        user_id_error = "Ошибка декодирования токена токена. (Неверный id пользователя)"
        user_role_id_error = "Ошибка декодирования токена токена. (Неверный id роли)"

        self.assertEqual(testing_user_id, self.user_id, user_id_error)
        self.assertEqual(testing_user_role_id, self.user_role_id, user_role_id_error)

    def test_get_payload_for_access_token(self):
        """Тестирование метода _get_payload_for_access_token."""
        payload = {"id": self.user_id, "role": self.user_role_id}

        testing_payload = self.jwt_tokens()._get_payload_for_access_token(
            self.user_id, self.user_role_id
        )

        payload_auth_user_error = (
            "Неверная полезная загрузка для генерации access_token"
        )

        self.assertEqual(payload, testing_payload, payload_auth_user_error)

    def test_get_payload_for_refresh_token(self):
        """Тестирование метода _get_payload_for_refresh_token."""
        payload = {"id": self.user_id, "refresh": "True"}

        testing_payload = self.jwt_tokens()._get_payload_for_refresh_token(self.user_id)

        payload_refresh_error = "Неверная полезная загрузка для генерации refresh_token"

        self.assertEqual(payload, testing_payload, payload_refresh_error)
