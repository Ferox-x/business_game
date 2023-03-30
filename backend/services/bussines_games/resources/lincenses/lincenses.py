class License:
    """Лицензия на ресурсы."""

    def __init__(self, name, life_time, player):
        """Инициализация лицензии."""
        self.player = player
        self.resource = name
        self.life_time = life_time
        self.quantity = 6

    def using_license(self):
        self.life_time -= 1
        self.player.game_role.increase_resource_by_name(self.resource, self.quantity)

        if self.life_time == 0:
            return False
        return True

    def to_json(self, title):

        return {
            "title": title,
            "life_time": self.life_time,
        }
