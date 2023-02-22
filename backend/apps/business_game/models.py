from django.db import models


class GameManager(models.Manager):
    """Менеджер работы с моделью Game."""

    def create_game(self, name, coordinator_id):
        """Создает запись в Game."""
        game = self.model(name=name, coordinator_id_id=coordinator_id)
        game.save()
        return game


class GameAttributesManager(models.Manager):
    """Менеджер работы с моделью GameAttributes."""

    def set_attributes(self, game_id, required_attributes):
        """Заносит в GameAttributes атрибуты связывая их с экземпляром Game."""
        game_attributes = self.model(game_id_id=game_id)
        game_attributes.save()
        for attribute in required_attributes:
            game_attributes.attributes.add(attribute)
        return game_attributes


class Game(models.Model):
    """Модель игры."""

    name = models.CharField(max_length=55)
    # created_at = models.DateTimeField()
    coordinator_id = models.ForeignKey("users.Coordinator", on_delete=models.CASCADE)
    objects = GameManager()


class GameAttributes(models.Model):
    """Модель атрибутов игры."""

    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    attributes = models.ManyToManyField("users.Attribute")
    objects = GameAttributesManager()
