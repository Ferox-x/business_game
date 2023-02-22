from django.urls import path

from apps.business_game.views import GameVieSet, TestView

urlpatterns = [
    # path(
    #     "api/game/",
    # ),
    # path("api/game/<str:invite_code>", name="invite-url"),
    path(
        "api/game/start",
        GameVieSet.as_view(
            {
                "post": "create_game_and_set_attributes",
            }
        ),
    ),
    path("api/game/test", TestView.as_view()),
]
