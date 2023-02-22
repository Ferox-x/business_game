from dataclasses import dataclass

from services.bussines_games.resources.lincenses.lincenses import License


class ResourcesGame:
    """Глобальные параметры игры."""

    @dataclass
    class _Salary:
        """Класс зарплат министров."""

        president: int = 0
        MVD: int = 0
        minister_economy: int = 0
        minister_education: int = 0
        minister_JKH: int = 0
        SMI: int = 0

    @dataclass
    class _Economy:
        """Класс налогов."""

        tax: int = 0
        percent_credit: int = 0

    def __init__(self):
        """Инициализация."""
        self.salary = self._Salary()
        self.economy = self._Economy()


class ResourcesPlayer:
    """Ресурсы игрока."""

    @dataclass
    class _NonTradeResources:
        """Не передаваемые ресурсы."""

        building_diploma: bool = False
        architect_diploma: bool = False
        building_license: License = License(quantity=0, life_time=0)
        architecting_license: License = License(quantity=0, life_time=0)
        wood_license: License = License(quantity=0, life_time=0)
        glass_license: License = License(quantity=0, life_time=0)
        brick_license: License = License(quantity=0, life_time=0)
        shingles_license: License = License(quantity=0, life_time=0)
        advertising: int = 0

    @dataclass
    class _TradeResources:
        """Передаваемые ресурсы."""

        money: int = 0
        wood: int = 0
        glass: int = 0
        brick: int = 0
        shingles: int = 0
        small_area: int = 0
        big_area: int = 0
        tap: int = 0
        communications: int = 0
        plan_of_small_house: int = 0
        plan_of_big_house: int = 0
        small_house: int = 0
        big_house: int = 0

    def __init__(self):
        """Инициализация."""
        self.non_trade_resources = self._NonTradeResources()
        self.trade_resources = self._TradeResources()
