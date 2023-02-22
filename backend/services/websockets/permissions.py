def is_coordinator(user):
    """Проверка пользователя на координатора."""
    if user and user.is_coordinator:
        return True


def is_player(user):
    """Проверка пользователя на игрока."""
    if user and user.is_player:
        return True


def access_true(user):
    """Проверка пользователя."""
    return True
