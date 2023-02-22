from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from services.bussines_games.bussines_games import GamesContainer
from services.permissions import IsCoordinator

from apps.business_game.models import Game, GameAttributes
from apps.business_game.serializers import GameSerializer


class GameVieSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Класс отображения для Игр."""

    queryset = Game.objects.all()
    serializer_class = GameSerializer

    @action(detail=False, methods=["post"])
    def create_game_and_set_attributes(self, request):
        """Метод создания игры и атрибутов к ней."""
        game_name = request.data.get("game_name")
        # time_start = request.data.get("time_start")
        required_attributes = request.data.get("required_attributes")
        game = Game.objects.create_game(name=game_name, coordinator_id=request.user.id)
        GamesContainer().create_game(game.id)
        GameAttributes.objects.set_attributes(
            game_id=game.id, required_attributes=required_attributes
        )
        return Response({"message": "Игра успешно создана"}, status=status.HTTP_200_OK)

    def get_permissions(self):
        """Метод проверяющий права доступа."""
        actions = {
            "list": [IsAdminUser],
            "create_game_and_set_attributes": [IsAuthenticated, IsCoordinator],
        }
        permission_classes = actions[self.action]

        return [permission() for permission in permission_classes]


class TestView(APIView):
    """."""

    def get(self, request):
        """."""
        GamesContainer().get_game_by_game_id(1)
        GamesContainer().get_game_by_game_id(2)

        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        """."""
        game_1 = GamesContainer().create_game(1)
        game_2 = GamesContainer().create_game(2)
        game_2.add_player(1)
        game_2.add_player(2)
        game_2.add_player(3)
        game_1.add_player(1)
        game_1.add_player(2)
        game_1.add_player(3)

        return Response(status=status.HTTP_200_OK)
