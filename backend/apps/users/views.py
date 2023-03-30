import logging

from django.core.paginator import EmptyPage, Paginator
from django.db import IntegrityError
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from services.invite_code import InviteCodeMethods
from services.permissions import IsCoordinator, IsPlayer
from services.to_json import attributes_to_json

from apps.business_game.models import Game
from apps.users.models import Attribute, AttributeAndValue, Coordinator, Player
from apps.users.serializers import CoordinatorSerializer, PlayerSerializer

logger = logging.getLogger()


class CoordinatorViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Набор отображения для личного кабинета Координатора.

    Methods: POST, GET
    """

    queryset = Coordinator.objects.all()
    serializer_class = CoordinatorSerializer

    @action(detail=True, methods=["put"])
    def set_attributes(self, request: Request):
        """Метод для установки атрибутов координатором."""
        try:
            attributes = request.data["attributes"]
            attributes = [
                int(attribute)
                for attribute, value in attributes.items()
                if value is True
            ]
        except KeyError:
            detail = "Key attribute not found"
            raise ValidationError(detail)

        coordinator: Coordinator = request.user

        try:
            coordinator.attributes.set(attributes)
        except (IntegrityError, ValueError):
            detail = "Invalidate attributes"
            raise ValidationError(detail)

        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def add_new_attribute(self, request):

        try:
            attribute = request.data["attribute"]
        except KeyError:
            detail = "Key attribute not found"
            raise ValidationError(detail)

        Attribute.objects.create(attribute=attribute)

        return self.get_all_attributes(request)

    @action(detail=False, methods=["get"])
    def get_attributes(self, request: Request):
        """Метод для получения атрибутов координатора."""
        queryset = request.user.attributes.all()
        attributes = attributes_to_json(queryset)
        return Response(attributes, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_all_attributes(self, request: Request):
        """Метод для получения атрибутов координатора."""
        all_attributes = Attribute.objects.all()
        coordinator_attributes = request.user.attributes.all()
        union = [
            [attribute.id, attribute.attribute, True]
            if attribute in coordinator_attributes
            else [attribute.id, attribute.attribute, False]
            for attribute in all_attributes
        ]
        return Response(union, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_coordinator_games(self, request: Request, page: int = 1):
        """Метод для получения игроков приглашенным координатором."""
        games = Game.objects.filter(coordinator_id=request.user.id)

        paginator = Paginator(games, 5)
        try:
            page_games = paginator.page(page)
        except EmptyPage:
            paginator_json = {
                "next": False,
                "prev": page - 1 if paginator.num_pages + 1 == page else False,
                "total_pages": paginator.num_pages,
                "current_page": page,
                "data": [],
            }
            return Response(paginator_json, status=status.HTTP_200_OK)

        games_json = [
            {
                "game_id": game.id,
                "name": game.name if game.name else "Не указанно",
                "number_players": "Не указанно",
                "year": "Не указанно",
                "end_date": "Не указанно",
                "status": "Не указанно",
            }
            for game in page_games
        ]

        paginator_json = {
            "next": page_games.has_next(),
            "prev": page_games.has_previous(),
            "total_pages": paginator.num_pages,
            "current_page": page,
            "data": games_json,
        }

        return Response(paginator_json, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_coordinator_players(self, request: Request, page: int = 1):
        """Метод для получения игроков приглашенным координатором."""
        players = Player.objects.filter(coordinator_id=request.user.id)

        paginator = Paginator(players, 5)
        try:
            page_players = paginator.page(page)
        except EmptyPage:
            paginator_json = {
                "next": False,
                "prev": page - 1 if paginator.num_pages + 1 == page else False,
                "total_pages": paginator.num_pages,
                "current_page": page,
                "data": [],
            }
            return Response(paginator_json, status=status.HTTP_200_OK)

        players_json = [
            {
                "user_id": player.id,
                "email": player.email,
                "first_name": player.first_name if player.first_name else "Не указанно",
                "last_name": player.last_name if player.first_name else "Не указанно",
                "games": 0,
                "register_date": player.created_at,
            }
            for player in page_players
        ]

        paginator_json = {
            "next": page_players.has_next(),
            "prev": page_players.has_previous(),
            "total_pages": paginator.num_pages,
            "current_page": page,
            "data": players_json,
        }

        return Response(paginator_json, status=status.HTTP_200_OK)

    @action(detail=True, methods=["put"])
    def update_invite_code(self, request: Request):
        """Метод обновления invite-code."""
        user = self.get_object()
        new_invite_code = InviteCodeMethods.generate_invite_code(user.id)
        user.invite_code = new_invite_code
        user.save()
        return Response({"invite_code": new_invite_code}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def get_invite_code(self, request: Request):
        """Получение инвайт кода и ссылки."""
        user = self.get_object()
        invite_code = user.invite_code
        return Response({"invite_code": invite_code}, status=status.HTTP_200_OK)

    def get_object(self):
        """Переопределение метода получения объекта."""
        obj_id = self.request.user.id
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=obj_id)
        return obj

    def get_permissions(self):
        """Метод проверяющий права доступа."""
        actions = {
            "list": [IsAdminUser],
            "retrieve": [IsAuthenticated, IsCoordinator],
            "partial_update": [IsAuthenticated, IsCoordinator],
            "set_attributes": [IsAuthenticated, IsCoordinator],
            "get_attributes": [IsAuthenticated, IsCoordinator],
            "add_new_attribute": [IsAuthenticated, IsCoordinator],
            "get_all_attributes": [IsAuthenticated, IsCoordinator],
            "get_coordinator_players": [IsAuthenticated, IsCoordinator],
            "get_coordinator_games": [IsAuthenticated, IsCoordinator],
            "get_invite_code": [IsAuthenticated, IsCoordinator],
            "update_invite_code": [IsAuthenticated, IsCoordinator],
        }
        permission_classes = actions[self.action]

        return [permission() for permission in permission_classes]


class PlayerViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Набор отображения для личного кабинета Игрока.

    Methods: POST, GET
    """

    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    @action(detail=False, methods=["get"])
    def get_player_games(self, request: Request, page: int = 1):
        """Метод для получения игроков приглашенным координатором."""
        # Переделать в будущем на личные игры.
        games = Game.objects.all()

        paginator = Paginator(games, 5)
        try:
            page_games = paginator.page(page)
        except EmptyPage:
            paginator_json = {
                "next": False,
                "prev": page - 1 if paginator.num_pages + 1 == page else False,
                "total_pages": paginator.num_pages,
                "current_page": page,
                "data": [],
            }
            return Response(paginator_json, status=status.HTTP_200_OK)

        games_json = [
            {
                "game_id": game.id,
                "name": game.name if game.name else "Не указанно",
                "role": "Не указанно",
                "number_players": "Не указанно",
                "year": "Не указанно",
                "end_date": "Не указанно",
            }
            for game in page_games
        ]

        paginator_json = {
            "next": page_games.has_next(),
            "prev": page_games.has_previous(),
            "total_pages": paginator.num_pages,
            "current_page": page,
            "data": games_json,
        }

        return Response(paginator_json, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_attributes(self, request: Request):
        """Метод для получения атрибутов координатора игроком."""
        user: Player = request.user
        queryset = user.coordinator_id.attributes.all()
        attributes = attributes_to_json(queryset)
        return Response(attributes, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def set_value_to_attribute(self, request: Request):
        """Метод для заполнения атрибутов координатора игроком."""
        attributes_and_value = request.data["attributes"]
        player: Player = request.user
        coordinator_attrs = player.coordinator_id.attributes.all()

        if attributes_and_value:
            Player.attribute_manger.set(
                attributes_and_value, player.id, coordinator_attrs
            )
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def get_attribute_and_value(self, request):
        """Метод для получения атрибутов игроком."""
        player: Player = request.user
        queryset = AttributeAndValue.objects.select_related("attribute").filter(
            player_id=player.id
        )
        data = [
            {
                "attribute": data_object.attribute.attribute,
                "value": data_object.value,
                "id": data_object.id,
            }
            for data_object in queryset
        ]
        return Response(data, status=status.HTTP_200_OK)

    def get_object(self):
        """Переопределение метода получения объекта."""
        obj_id = self.request.user.id
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=obj_id)
        return obj

    def get_permissions(self):
        """Метод проверяющий права доступа."""
        actions = {
            "retrieve": [IsAuthenticated, IsPlayer],
            "get_attributes": [IsAuthenticated, IsPlayer],
            "get_player_games": [IsAuthenticated, IsPlayer],
            "partial_update": [IsAuthenticated, IsPlayer],
            "set_value_to_attribute": [IsAuthenticated, IsPlayer],
            "get_attribute_and_value": [IsAuthenticated, IsPlayer],
        }
        permission_classes = actions[self.action]

        return [permission() for permission in permission_classes]
