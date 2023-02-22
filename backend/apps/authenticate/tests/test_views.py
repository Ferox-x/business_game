from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from services.auth_services.generate_tokens import RefreshToken
from services.cache.cache import RedisCacheMethods

from apps.authenticate.models import AuthUser
from apps.users.models import Coordinator, Player, UserRole


class AuthenticateTest(APITestCase):
    """Класт тестирования views приложения authenticate."""

    USER_EMAIL = "user@mail.ru"
    COORDINATOR_EMAIL = "user2@mail.ru"
    USER_PASSWORD = "user1213aeqwadsa"
    EMAIL_ERROR = "USER123"
    PASSWORD_ERROR = "qwerty"

    @classmethod
    def setUpTestData(cls):
        """Инициализация стартовой БД необходимой для тестирования."""
        UserRole.objects.create(name="Admin")
        UserRole.objects.create(name="Coordinator")
        UserRole.objects.create(name="Player")
        test_user = AuthUser.objects.create(
            email=cls.USER_EMAIL, password=cls.USER_PASSWORD, role_id=3
        )
        test_user.save()
        test_coordinator = Coordinator.objects.create_coordinator(
            email=cls.COORDINATOR_EMAIL, password=cls.USER_PASSWORD
        )
        test_coordinator.save()

    def test_player_registration(self):
        """Тест регистрации координатора."""
        length = Player.objects.count()
        url = reverse("registrate-player")
        data = {
            "user": {
                "email": "player@mail.ru",
                "password": self.USER_PASSWORD,
                "invite_code": Coordinator.objects.get(
                    email=self.COORDINATOR_EMAIL
                ).invite_code,
            }
        }
        self.client.post(url, data=data, format="json")
        self.assertEqual(Player.objects.count(), length + 1)

    def test_player_registration_with_wrong_data(self):
        """Тест регистрации игрока с невалидными данными."""
        url = reverse("registrate-player")
        data = {
            "user": {
                "email": self.EMAIL_ERROR,
                "password": self.PASSWORD_ERROR,
                "invite_code": "sad",
            }
        }
        errors_list = [
            "Введите правильный адрес электронной почты.",
            "Введённый пароль слишком короткий. Он должен "
            "содержать как минимум 8 символов.",
            "Введённый пароль слишком широко распространён.",
            "Invite-код недействителен.",
        ]
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(errors_list, response.data.get("errors"))

    def test_coordinator_registration(self):
        """Тест регистрации координатора."""
        length = Coordinator.objects.count()
        url = reverse("registrate-coordinator")
        data = {"user": {"email": "coor@mail.ru", "password": self.USER_PASSWORD}}
        self.client.post(url, data=data, format="json")
        self.assertEqual(Coordinator.objects.count(), length + 1)

    def test_coordinator_registration_with_wrong_data(self):
        """Тест регистрации координатора с невалидными данными."""
        url = reverse("registrate-coordinator")
        data = {"user": {"email": self.EMAIL_ERROR, "password": self.PASSWORD_ERROR}}
        errors_list = [
            "Введённый пароль слишком короткий. "
            "Он должен содержать как минимум 8 символов.",
            "Введённый пароль слишком широко распространён.",
            "Введите правильный адрес электронной почты.",
        ]
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(errors_list, response.data.get("errors"))

    def test_login(self):
        """Аутентификация пользователя по email."""
        url = reverse("login")
        data = {
            "user": {"email": self.COORDINATOR_EMAIL, "password": self.USER_PASSWORD}
        }
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_wit_error(self):
        """Тест аутентификации пользователя по email с невалидными данными."""
        url = reverse("login")
        data = {"user": {"email": self.COORDINATOR_EMAIL, "password": "anypassword"}}
        message = ["Пользователь с такими email и паролем не найден."]
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(message, response.data.get("errors"))

    def test_sending_email(self):
        """Тест на проверку отправки сообщения с ссылкой на востановление пароля."""
        url = reverse("password-reset")
        data = {"email": self.USER_EMAIL}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sending_email_with_error(self):
        """Тест на проверку отправки сообщения с ссылкой на востановление пароля."""
        url = reverse("password-reset")
        data = {"email": "user"}
        message = ["Пользователь с таким  email не найден"]
        response = self.client.post(url, data, format="json")
        self.assertEqual(message, response.data.get("errors"))

    def test_reset_password(self):
        """Тест на смену пароля по ссылке."""
        token = RedisCacheMethods.get_reset_password_token(1)
        url = reverse("confirm-password-reset", kwargs={"token": token})
        data_confirm = {"password1": "qsqrwer23dsa", "password2": "qsqrwer23dsa"}

        self.client.put(url, data_confirm, format="json")
        log_in = self.client.login(email=self.USER_EMAIL, password="qsqrwer23dsa")
        self.assertTrue(log_in)

    def test_reset_password_with_wrong_data(self):
        """Тест на смену пароля по ссылке c невалидными данными."""
        token = RedisCacheMethods.get_reset_password_token(1)
        url = reverse("confirm-password-reset", kwargs={"token": token})
        data_confirm = [
            {"password1": "qwerty", "password2": "qwerty"},
            {"password1": None, "password2": "qwerty"},
            {"password1": "qwerty", "password2": None},
            {"password1": "qwerty", "password2": "asdf"},
        ]
        messages_list = [
            [
                "Введённый пароль слишком короткий. "
                "Он должен содержать как минимум 8 символов.",
                "Введённый пароль слишком широко распространён.",
            ],
            ["Все поля должны быть заполнены"],
            ["Все поля должны быть заполнены"],
            ["Пароли не совпадают."],
        ]

        for i in range(len(messages_list)):
            response = self.client.put(url, data_confirm[i], format="json")
            self.assertEqual(messages_list[i], response.data.get("errors"))

    def test_api_refresh(self):
        """Тест на смену access токена."""
        url = reverse("api-refresh")
        refresh_token = RefreshToken().generate_token(1)
        data = {"refreshToken": refresh_token}
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_refresh_with_wrong_data(self):
        """Тест на смену access токена с невалидными данными."""
        url = reverse("api-refresh")

        data = [
            {"refreshToken": None},
            {"refreshToken": RefreshToken().generate_token(25)},
        ]
        errors_list = [
            ["Учетные данные для аутентификации не были предоставлены."],
            ["Пользователь не найден"],
        ]
        for i in range(len(errors_list)):
            response = self.client.post(url, data=data[i], format="json")
            self.assertEqual(errors_list[i], response.data.get("errors"))

    def test_change_password(self):
        """Тест на изменения пароля."""
        user = Coordinator.objects.get(email=self.COORDINATOR_EMAIL)
        self.client.force_authenticate(user)
        url = reverse("password-change")
        data = {
            "old_password": self.USER_PASSWORD,
            "new_password": "qsqrwer23dsa",
            "new_password2": "qsqrwer23dsa",
        }
        response = self.client.post(url, data, format="json")
        log_in = self.client.login(
            username=self.COORDINATOR_EMAIL, password="qsqrwer23dsa"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(log_in)

    def test_change_password_with_wrong_data(self):
        """Тест на изменение пароля с невалидными данными."""
        user = Coordinator.objects.get(email=self.COORDINATOR_EMAIL)
        self.client.force_authenticate(user)
        url = reverse("password-change")
        data = [
            {
                "old_password": "2231",
                "new_password": "qsqrwer23dsa",
                "new_password2": "qsqrwer23dsa",
            },
            {
                "old_password": self.USER_PASSWORD,
                "new_password": "qsqrwer23d",
                "new_password2": "qsqrwer23dsa",
            },
            {
                "old_password": self.USER_PASSWORD,
                "new_password": None,
                "new_password2": "qsqrwer23dsa",
            },
            {
                "old_password": self.USER_PASSWORD,
                "new_password": "qwerty",
                "new_password2": "qwerty",
            },
        ]
        messages = [
            ["Старый пароль указан неверно"],
            ["Пароли не совпадают"],
            ["Все поля должны быть заполнены"],
            [
                "Введённый пароль слишком короткий. "
                "Он должен содержать как минимум 8 символов.",
                "Введённый пароль слишком широко распространён.",
            ],
        ]
        for i in range(len(messages)):
            response = self.client.post(url, data[i], format="json")
            self.assertEqual(messages[i], response.data.get("errors"))
