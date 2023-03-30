from services.bussines_games.roles.roles import (
    Bank,
    MinisterEconomy,
    MinisterEducation,
    MinisterJKH,
    MinisterMVD,
    President,
    RoleSMI,
)


def is_coordinator(consumer):
    """Проверка пользователя на координатора."""
    if consumer.user and consumer.user.is_coordinator:
        return True


def is_player(consumer):
    """Проверка пользователя на игрока."""
    if consumer.user and consumer.user.is_player:
        return True


def is_president(consumer):
    """Проверка пользователя на роль президента."""
    player = consumer.game.get_player(consumer.user.id)
    if isinstance(player.game_role, President):
        return True


def is_bank(consumer):
    """Проверка пользователя на роль банка."""
    player = consumer.game.get_player(consumer.user.id)
    if isinstance(player.game_role, Bank):
        return True


def is_mvd(consumer):
    """Проверка пользователя на роль мвд."""
    player = consumer.game.get_player(consumer.user.id)
    if isinstance(player.game_role, MinisterMVD):
        return True


def is_minister_jkh(consumer):
    """Проверка пользователя на роль министра ЖКХ."""
    player = consumer.game.get_player(consumer.user.id)
    if isinstance(player.game_role, MinisterJKH):
        return True


def is_education_minister(consumer):
    """Проверка пользователя на роль министра ЖКХ."""
    player = consumer.game.get_player(consumer.user.id)
    if isinstance(player.game_role, MinisterEducation):
        return True


def is_economy_minister(consumer):
    """Проверка пользователя на роль министра ЖКХ."""
    player = consumer.game.get_player(consumer.user.id)
    if isinstance(player.game_role, MinisterEconomy):
        return True


def is_smi(consumer):
    """Проверка пользователя на роль СМИ."""
    player = consumer.game.get_player(consumer.user.id)
    if isinstance(player.game_role, RoleSMI):
        return True


def access_true(user):
    """Проверка пользователя."""
    return True
