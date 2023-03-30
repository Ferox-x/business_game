from django.urls import path

from apps.users.views import CoordinatorViewSet, PlayerViewSet

urlpatterns = [
    path(
        "api/coordinator/list",
        CoordinatorViewSet.as_view(
            {
                "get": "list",
            }
        ),
    ),
    path(
        "api/coordinator/players/<int:page>",
        CoordinatorViewSet.as_view(
            {
                "get": "get_coordinator_players",
            }
        ),
    ),
    path(
        "api/coordinator/games/<int:page>",
        CoordinatorViewSet.as_view(
            {
                "get": "get_coordinator_games",
            }
        ),
    ),
    path(
        "api/coordinator/retrieve",
        CoordinatorViewSet.as_view(
            {
                "get": "retrieve",
                "post": "partial_update",
            }
        ),
    ),
    path(
        "api/coordinator/attributes",
        CoordinatorViewSet.as_view(
            {
                "get": "get_attributes",
                "post": "add_new_attribute",
                "put": "set_attributes",
            }
        ),
    ),
    path(
        "api/coordinator/all-attributes",
        CoordinatorViewSet.as_view(
            {
                "get": "get_all_attributes",
            }
        ),
    ),
    path(
        "api/coordinator/invite-code",
        CoordinatorViewSet.as_view(
            {
                "put": "update_invite_code",
                "get": "get_invite_code",
            }
        ),
    ),
    path(
        "api/player/retrieve",
        PlayerViewSet.as_view(
            {
                "get": "retrieve",
                "post": "partial_update",
            }
        ),
    ),
    path(
        "api/player/games/<int:page>",
        PlayerViewSet.as_view(
            {
                "get": "get_player_games",
            }
        ),
    ),
    path(
        "api/player/attributes",
        PlayerViewSet.as_view(
            {
                "get": "get_attributes",
                "post": "set_value_to_attribute",
            }
        ),
    ),
    path(
        "api/player/attributes/value",
        PlayerViewSet.as_view(
            {
                "get": "get_attribute_and_value",
            }
        ),
    ),
]
