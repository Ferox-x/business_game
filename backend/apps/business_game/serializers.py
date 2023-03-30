from rest_framework import serializers

from apps.business_game.models import Game


class GameSerializer(serializers.ModelSerializer):
    """Сериализатор модели Game."""

    class Meta:
        """Мета класс сериализатора."""

        model = Game
        fields = ["name", "time_start", "coordinator_id"]
