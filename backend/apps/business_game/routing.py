from django.urls import re_path

from apps.business_game.consumers import GameWebsocketAPI

websocket_urlpatterns = [
    re_path(r"ws/game/(?P<game_id>\w+)/$", GameWebsocketAPI.as_asgi()),
]
