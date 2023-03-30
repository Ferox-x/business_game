import random

from utils.counter import Counter
from utils.singleton import Singleton

from services.bussines_games.resources.resources import ResourcesGame
from services.bussines_games.roles.roles import Banks, BaseGameRole, Ministers
from services.bussines_games.roles.roles_dict import RolesDict
from services.bussines_games.trades.container import ItemStatus
from services.bussines_games.utils.game_utils import GameStates


class Coordinator:
    def __init__(self, coordinator, game, channel=None):
        self.coordinator_id = coordinator.id
        self.name = coordinator.get_full_name() or coordinator.email
        self.game = game
        self.channel = channel

    def connect(self, game, channel):
        self.game = game
        self.channel = channel


class PlayerGame:
    """Класс игрока."""

    def __init__(self, player_id, name, channel, game):
        """Метод инициализации игрока."""
        self.player_id: int = player_id
        self.name = name
        self.game: "Game" = game
        self.game_role: "BaseGameRole" = None
        self.channel = channel

    def add_role(self, name, alias, description, role):
        """Метод добавления роли игроку."""
        self.game_role = role(
            game=self.game,
            player=self,
            game_role_name=name,
            description=description,
            alias=alias,
        )

    def update_channel(self, channel_name):
        """Метод обновления канала."""
        self.channel = channel_name

    def player_data_for_coordinator(self):
        dict_to_return = {
            "id": self.player_id,
            "name": self.name,
            "role": self.game_role.game_role_name,
            "resources": self.game_role.resources.to_json_trade_resources(),
        }
        return dict_to_return

    def player_data_for_player(self):
        players = dict()
        smi_dict = dict()
        for key, value in self.game.players.items():
            players[str(key)] = value.name

        for smi in self.game.ministers.get_smi():
            if smi is not None:
                smi_dict[str(smi.player.player_id)] = smi.player.name

        dict_to_return = {
            "data": {
                "role": self.game_role.alias,
                "diploma_and_license": (
                    self.game_role.resources.get_license_and_diploma()
                ),
                "trades": self.game_role.trades.incoming_trades(self),
                "credits": self.game_role.credits.get_all_items().get(
                    ItemStatus.accepted
                ),
                "input_data": {
                    "players": players,
                    "SMI": smi_dict,
                    "banks": self.game.banks.get_all_banks_name(),
                },
                "game_status": GameStates.in_process,
                "role_data": self.game_role.to_json_role_data(),
            },
            "resources": self.game_role.resources.to_json_trade_resources(),
        }
        return dict_to_return


class Game:
    """Класс игры."""

    ROLE_DICT = RolesDict.roles_dict

    def __init__(self, game_id, coordinator, start_time) -> None:
        """Инициализация игры."""
        self.game_id: int = game_id
        self.game_start_time = start_time
        self.game_status: str = GameStates.lobby

        self.coordinator: Coordinator = Coordinator(coordinator, self)
        self.players: {int: "PlayerGame"} = {}
        self.ministers: Ministers = None
        self.banks: Banks = None

        self.resources: ResourcesGame = ResourcesGame()
        self.year: int = 0
        self.counter_ids = Counter()

    def on_change_year(self):
        self.set_game_status_changing_year()
        players = self.players.values()

        for player in players:
            player.game_role.on_change_year()

        self.resources.on_change_year()
        self.resources.pay_paycheck(self.ministers.get_all_ministers())

        self.year += 1

    def add_player(self, player_id, name, channel) -> PlayerGame | bool:
        """Добавить игрока."""
        if self.allow_to_connect_player():
            player = PlayerGame(player_id, name, channel, self)
            self.players[player_id] = player
            return player
        return False

    def get_player(self, player_id):
        """Получить игрока."""
        player = self.players.get(player_id)
        return player

    def set_role_for_users(self) -> None:
        """Функция распределения ролей игрокам."""
        ministers = []
        banks = []

        players_amount = len(self.players)
        players_instance = list(self.players.values())
        roles = list(self.ROLE_DICT.values())[:players_amount]
        random.shuffle(players_instance)

        for index, player in enumerate(players_instance):
            if index in (1, 2, 3, 4, 5, 16, 25):
                ministers.append(player)
            elif index in (6, 19, 24, 28):
                banks.append(player)

            role = roles[index]
            player.add_role(
                name=role["name"],
                description=role["description"],
                role=role["role"],
                alias=role["alias"],
            )

        self.ministers = Ministers(*ministers)
        self.banks = Banks(banks)

    def allow_to_connect_player(self) -> bool:
        """Функция проверкии пользователя.

        На возможность присоединения к игре.
        """
        if self.game_status == GameStates.lobby:
            return True
        else:
            return False

    def set_game_status(self, status):
        self.game_status = getattr(GameStates, status)

    def set_game_status_lobby(self) -> None:
        """Функция изменения статуса игры на лобби."""
        self.game_status = GameStates.lobby

    def set_game_status_in_process(self) -> None:
        """Функция изменения статуса игры в процессе."""
        self.game_status = GameStates.in_process

    def set_game_status_finished(self) -> None:
        """Функция изменения статуса игры на завершена."""
        self.game_status = GameStates.finished

    def set_game_status_changing_year(self) -> None:
        """Функция изменения статуса игры смена года."""
        self.game_status = GameStates.changing_year


class GamesContainer(Singleton):
    """Контейнер хранящий инстансы игры.

    Может создать, удалить и вернуть игру.
    """

    _games: {int: Game} = {}

    def create_game(
        self,
        game_id: int,
        coordinator: int,
        start_time,
    ) -> Game:
        """Метод создающий инстанс игры, и возвращает его."""
        new_game = Game(game_id, coordinator, start_time)
        self._games[game_id] = new_game
        return new_game

    def get_game_by_game_id(self, requested_game_id: int) -> Game | bool:
        """Возращает игру по айди игры. Если нет игры возращает None."""
        game = self._games.get(int(requested_game_id))
        if game:
            return game
        return False

    def delete_game(self, deleted_game_id: int) -> bool:
        """Метод удаления игры.

        Удаляет игру, возвращает True, если игра была найдена и удалена,
        возвращает False, если игра не была найдена.
        """
        game = self._games.get(deleted_game_id)
        if game:
            del self._games[deleted_game_id]
            return True
        return False

    def load_game(self, game):
        """Метод загрузки игры."""
        self._games[game.game_id] = game
