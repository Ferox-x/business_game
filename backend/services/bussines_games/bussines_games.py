import random

from services.bussines_games.resources.resources import ResourcesGame, ResourcesPlayer
from services.bussines_games.roles.roles import BaseRole


class Player:
    """Класс игрока."""

    def __init__(self, player_id, channel, game):
        """Метод инициализации игрока."""
        self.player_id: int = player_id
        self.game = game
        self.game_role = None
        self.resources = ResourcesPlayer()
        self.channel = channel

    def add_role(self, role):
        """Метод добавления роли игроку."""
        self.game_role: BaseRole = BaseRole(game=self.game, player=self)


class Game:
    """Класс игры."""

    ROLE_LIST = [
        "Президент",
        "Министр экономики и финансов",
        "Министр ЖКХ",
        "Министр образования",
        "Министер внутренних дел,",
        "Комерческий банк",
        "Строитель",
        "Строитель",
        "Строитель",
        "Строитель",
        "Производитель",
        "Производитель",
        "Производитель",
        "Архитектор",
        "Архитектор",
        "СМИ",
        "Строитель",
        "Производитель",
        "Комерческий банк",
        "Архитектор",
        "Строитель",
        "Производитель",
        "Архитектор",
        "Комерческий банк",
        "СМИ",
        "Строитель",
        "Производитель",
        "Комерческий банк",
        "Архитектор",
        "Строитель",
        "Производитель",
    ]
    GAME_STATES = ["created", "lobby", "in process", "finished"]

    def __init__(self, game_id) -> None:
        """Инициализация игры."""
        self.game_id: int = game_id
        self.players: {int: Player} = {}
        self.game_status: str = self.GAME_STATES[1]
        self.resources: ResourcesGame = ResourcesGame()
        self.year: int = 0

    def add_player(self, player_id, channel) -> bool:
        """Добавить игрока."""
        if self.allow_to_connect_player(player_id):
            player = Player(player_id, channel, self)
            self.players[player_id] = player
            return True
        return False

    def get_player(self, player_id):
        """Получить игрока игрока."""
        player = self.players.get(player_id)
        return player

    def set_role_for_users(self) -> None:
        """Функция распределения ролей игрокам."""
        players_amount = len(self.players)
        players_instance = list(self.players.values())
        roles = self.ROLE_LIST[:players_amount]
        random.shuffle(roles)
        for index in range(players_amount):
            players_instance[index].add_role(roles[index])

    def allow_to_connect_player(self, player_id) -> bool:
        """Функция проверкии пользователя на возможность присоединения к игре."""
        if self.game_status == self.GAME_STATES[1]:
            return True
        elif self.game_status == self.GAME_STATES[2] and self.players.get(player_id):
            return True
        else:
            return False

    def set_game_status_lobby(self) -> None:
        """Функция изменения статуса игры на лобби."""
        self.game_status = self.GAME_STATES[1]

    def set_game_status_in_process(self) -> None:
        """Функция изменения статуса игры на в процессе."""
        self.game_status = self.GAME_STATES[2]

    def set_game_status_finished(self) -> None:
        """Функция изменения статуса игры на завершена."""
        self.game_status = self.GAME_STATES[3]


class GamesContainer:
    """Контейнер хранящий инстансы игры, можешь создать, удалить и вернуть игру."""

    _games: {int: Game} = {}

    def create_game(self, game_id: int) -> Game:
        """Метод создающий инстанс игры, и возвращает его."""
        new_game = Game(game_id)
        self._games[game_id] = new_game
        return new_game

    def get_game_by_game_id(self, requested_game_id: int) -> Game | None:
        """Возращает игру по айди игры. Если нет игры возращает None."""
        game = self._games.get(int(requested_game_id))
        if game:
            return game
        return None

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
