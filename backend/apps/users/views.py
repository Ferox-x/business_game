import logging

from django.db import IntegrityError
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from services.auth_services.auth_services import InviteCodeMethods
from services.permissions import IsCoordinator, IsPlayer
from services.to_json import attributes_to_json

from apps.users.models import AttributeAndValue, Coordinator, Player
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

    @action(detail=True, methods=["post"])
    def set_attributes(self, request: Request):
        """Метод для установки атрибутов координатором."""
        try:
            attributes = request.data["attributes"]
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

    @action(detail=False, methods=["get"])
    def get_attributes(self, request: Request):
        """Метод для получения атрибутов координатора."""
        queryset = request.user.attributes.all()
        attributes = attributes_to_json(queryset)
        return Response(attributes, status=status.HTTP_200_OK)

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

    @action(detail=False, methods=["get"])
    def get_coordinator_players(self, request: Request):
        """Получение координатором списка приглашенных игроков."""
        user = self.get_object()
        players = (
            Player.objects.filter(coordinator_id=user.id)
            .prefetch_related("attributes")
            .select_related("coordinator_id")
        )
        data = list()
        for player in players:
            data.append(
                {
                    "email": player.email,
                    "created_at": player.created_at,
                    "first_name": player.first_name,
                    "second_name": player.second_name,
                }
            )
        return Response({"players": data}, status=status.HTTP_200_OK)

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
            "get_invite_code": [IsAuthenticated, IsCoordinator],
            "update_invite_code": [IsAuthenticated, IsCoordinator],
            "get_coordinator_players": [IsAuthenticated, IsCoordinator],
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
            {"attribute": data_object.attribute.attribute, "value": data_object.value}
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
            "partial_update": [IsAuthenticated, IsPlayer],
            "set_value_to_attribute": [IsAuthenticated, IsPlayer],
            "get_attribute_and_value": [IsAuthenticated, IsPlayer],
        }
        permission_classes = actions[self.action]

        return [permission() for permission in permission_classes]
