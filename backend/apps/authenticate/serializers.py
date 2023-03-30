import logging

import jwt
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from services.auth_services.auth_services import AuthRoles
from services.auth_services.generate_tokens import AccessToken, RefreshToken
from services.invite_code import InviteCodeMethods
from services.validators.custom_validators import CustomValidatorsMethods
from utils.serialize_errors import ErrorsSerializer

from apps.authenticate.models import AuthUser
from apps.users.models import Coordinator, Player

logger = logging.getLogger(__name__)


class RegistrationPlayerSerializer(serializers.ModelSerializer, ErrorsSerializer):
    """Сериализация регистрации игрока и создания нового."""

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    invite_code = serializers.CharField(max_length=15)

    class Meta:
        """Мета класс."""

        model = Player
        fields = ["email", "password", "invite_code"]
        validators = []

    def create(self, validated_data):
        """Метод создания новых пользователей(игроков)."""
        return self.Meta.model.objects.create_user(**validated_data)

    def validate(self, data):
        """Метод валидации данных."""
        email = data.get("email")
        password = data.get("password")
        invite_code = data.get("invite_code")
        errors = list()
        errors.extend(CustomValidatorsMethods.is_email_validate(email))
        errors.extend(CustomValidatorsMethods.is_password_validate(password))
        coordinator_id = InviteCodeMethods.get_coordinator_id_by_invite_code(
            invite_code
        )

        if not coordinator_id:
            errors.append("Invite-код недействителен.")

        try:
            AuthUser.objects.get(email=data.get("email"))
            errors.append("Пользователь с таким email уже зарегистрирован")
        except ObjectDoesNotExist:
            pass

        if errors:
            raise serializers.ValidationError(errors)

        return {
            "email": email,
            "password": password,
            "coordinator_id": coordinator_id,
        }


class RegistrationCoordinatorSerializer(serializers.ModelSerializer, ErrorsSerializer):
    """Сериализация регистрации координатора и создания нового."""

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        """Мета класс."""

        model = Coordinator
        fields = ["email", "password"]

    def create(self, validated_data):
        """Метод создания новых пользователей(координаторов)."""
        return self.Meta.model.objects.create_coordinator(**validated_data)

    def validate(self, data):
        """Метод проверки валидности пароля и email."""
        errors = list()

        password = data.get("password")
        email = data.get("email")
        errors.extend(CustomValidatorsMethods.is_password_validate(password))
        errors.extend(CustomValidatorsMethods.is_email_validate(email))
        try:
            AuthUser.objects.get(email=data.get("email"))
            errors.append("Пользователь с таким email уже зарегистрирован")
        except ObjectDoesNotExist:
            pass
        if errors:
            raise serializers.ValidationError(errors)

        return data


class LoginSerializer(serializers.Serializer, ErrorsSerializer):
    """Сериализатор входа в систему."""

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        """Метод валидации.

        Метод проверяет пришедшие данные запроса, аутентифицирует пользователя,
        возвращает токены.
        :param data:
        :return: {
            'email': ...,
            'access_token': ...,
            'refresh_token': ...,
        }.
        """
        email = data.get("email", None)
        password = data.get("password", None)

        errors = list()

        user = authenticate(username=email, password=password)

        if user is None:
            errors.append("Пользователь с такими email и паролем не найден.")
            raise serializers.ValidationError(errors)
        if not user.is_active:
            errors.append("Данный пользователь был деактивирован.")
            raise serializers.ValidationError(errors)

        self.refresh_token = RefreshToken().generate_token(user_id=user.id)

        return {
            "email": user.email,
            "access_token": user.access_token,
            "refresh_token": self.refresh_token,
            "role": AuthRoles().get_role_name(user.role_id),
        }


class RefreshSerializer(serializers.Serializer):
    """Сериализатор для обновления токена."""

    refreshToken = serializers.CharField(max_length=255)

    def validate(self, data):
        """Метод валидации рефреш токена."""
        refresh_token = data.get("refreshToken")
        user_model = get_user_model()
        errors = list()

        try:
            payload = RefreshToken().decode_token(refresh_token)
        except jwt.ExpiredSignatureError:
            errors.append(
                "timeline действия токена обновления истек,"
                " пожалуйста, войдите снова."
            )
            raise serializers.ValidationError(errors)

        if not RefreshToken().check_token_type(payload):
            errors.append("Неверный тип токена.")
            raise serializers.ValidationError(errors)

        try:
            user = user_model.objects.get(pk=payload.get("id"))
        except ObjectDoesNotExist:
            errors.append("Пользователь не найден")
            raise serializers.ValidationError(errors)
        if not user.is_active:
            errors.append("Пользователь неактивен")
            raise serializers.ValidationError(errors)
        access_token = AccessToken().generate_token(
            user_id=user.id, user_role_id=user.role_id
        )

        return {
            "access_token": access_token,
        }


class PasswordResetSerializer(serializers.Serializer):
    """Сериализатор отправки сообщения на почту."""

    email = serializers.CharField()

    def validate(self, data):
        """Метод  проверки заполненности поля email.

        :param data:
        :return:{
            email: ...
            }.
        """
        errors = list()
        try:
            AuthUser.objects.get(email=data.get("email"))
        except ObjectDoesNotExist:
            errors.append("Пользователь с таким  email не найден")
            raise serializers.ValidationError(errors)
        return data


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Сериализатор смены пароля."""

    password1 = serializers.CharField(allow_null=True)
    password2 = serializers.CharField(allow_null=True)

    def validate(self, data):
        """Проверка паролей на соответствие.

        :param data:
        :return:
        """
        password1 = data.get("password1", None)
        password2 = data.get("password2", None)
        errors = list()
        if password1 is None or password2 is None:
            errors.append("Все поля должны быть заполнены")
            raise serializers.ValidationError(errors)

        if password1 != password2:
            errors.append("Пароли не совпадают.")
            raise serializers.ValidationError(errors)

        errors.extend(CustomValidatorsMethods.is_password_validate(password1))

        if errors:
            raise serializers.ValidationError(detail=errors)

        return data


class PasswordChangeSerializer(serializers.Serializer):
    """Класс сериализации изменения пароля."""

    old_password = serializers.CharField(allow_null=True)
    new_password = serializers.CharField(allow_null=True)
    new_password2 = serializers.CharField(allow_null=True)

    def validate(self, data):
        """Метод валидации данных при изменении пароля."""
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        new_password2 = data.get("new_password2")
        errors = list()

        if old_password is None or new_password is None or new_password2 is None:
            raise serializers.ValidationError("Все поля должны быть заполнены")
        user = self.context["request"].user
        is_password_correct = user.check_password(old_password)
        if not is_password_correct:
            raise serializers.ValidationError("Старый пароль указан неверно")

        if new_password != new_password2:
            raise serializers.ValidationError("Пароли не совпадают")

        errors.extend(CustomValidatorsMethods.is_password_validate(new_password))

        if errors:
            raise serializers.ValidationError(errors)

        return data
