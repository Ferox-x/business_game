from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from apps.users.models import Coordinator, Player


class CoordinatorSerializer(serializers.ModelSerializer):
    """Сериализатор модели Координатора."""

    phone_number = PhoneNumberField()

    class Meta:
        """Мета класс."""

        model = Coordinator
        fields = [
            "email",
            "first_name",
            "last_name",
            "patronymic",
            "birthday",
            "invite_code",
            "phone_number",
            "company",
            "job_title",
        ]
        read_only_fields = ["email", "invite_code"]


class PlayerSerializer(serializers.ModelSerializer):
    """Сериализатор модели Игрока."""

    class Meta:
        """Мета класс."""

        model = Player
        fields = [
            "email",
            "first_name",
            "last_name",
            "patronymic",
        ]
        read_only_fields = ["email"]
