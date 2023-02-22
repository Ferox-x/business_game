from asgiref.sync import async_to_sync
from services.bussines_games.bussines_games import Game, GamesContainer, Player
from services.websockets.base_websocket_api import WebsocketActionAPI
from services.websockets.permissions import access_true, is_coordinator, is_player


class GameWebsocketAPI(WebsocketActionAPI):
    """Вебсокет для игры."""

    action_and_permissions = {
        "game_chat_send_message": [access_true],
        "start_game": [is_coordinator],
        "create_trade": [is_player],
    }

    def connect(self):
        """Метод подключения к сокету игры."""
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.user = self.scope["user"]
        self.game_group_id = "game_%s" % self.game_id

        game: Game = GamesContainer().get_game_by_game_id(self.game_id)
        game.add_player(self.user.id, self.channel_name)

        player = game.get_player(self.user.id)
        player.add_role("32131")

        async_to_sync(self.channel_layer.group_add)(
            self.game_group_id, self.channel_name
        )

        self.accept()

    def action_game_chat_send_message(self):
        """Метод отправки сообщения в группу."""
        message = self.data.get("message")
        async_to_sync(self.channel_layer.group_send)(
            self.game_group_id,
            {
                "type": "chat.message",
                "json": {"user": self.user.email, "message": message},
            },
        )

    def action_private_chat_send_message(self):
        """Метод отправки личного сообщения."""
        message = self.data.get("message")
        channel_name = self.data.get("channel_name")
        async_to_sync(self.channel_layer.send)(
            channel_name,
            {
                "type": "chat.message",
                "json": {"user": self.user.email, "message": message},
            },
        )

    def chat_message(self, event):
        """Метод отправки сообщения в чат."""
        self.send_json(content=event["json"])

    def action_start_game(self):
        """Метод начала игры."""
        game = GamesContainer().get_game_by_game_id(self.game_id)
        game.set_game_status_in_process()

    def action_create_trade(self):
        """."""
        data = self.data

        game = GamesContainer().get_game_by_game_id(self.game_id)
        buyer: Player = game.get_player(self.user.id)
        seller: Player = game.get_player(data.get("seller_id"))
        buyer.game_role.send_offer_to_player(
            seller_id=data.get("seller_id"),
            resource=data.get("resource"),
            quantity=data.get("quantity"),
            price_per_one=data.get("price_per_one"),
        )
        json_trades = buyer.game_role.get_all_trades()
        async_to_sync(self.channel_layer.send)(
            seller.channel,
            {
                "type": "chat.message",
                "json": {"trades": json_trades},
            },
        )
