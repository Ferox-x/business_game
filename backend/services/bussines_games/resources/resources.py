from dataclasses import dataclass, field

from services.bussines_games.resources.lincenses.lincenses import License


class ResourcesGame:
    """Глобальные параметры игры."""

    @dataclass
    class _Salary:
        """Класс зарплат министров."""

        president: int = 0
        minister_economy: int = 0
        minister_JKH: int = 0
        minister_education: int = 0
        MVD: int = 0
        SMI: int = 0
        total_wage: int = 0

    @dataclass
    class _Economy:
        """Класс налогов."""

        tax: int = 0
        percent_credit: int = 0

    @dataclass
    class _LicensesLifeTime:
        building_license: int = -1
        architecting_license: int = -1
        wood_license: int = -1
        glass_license: int = -1
        brick_license: int = -1
        shingles_license: int = -1

    @dataclass
    class _Treasury:
        """."""

        wallet: int = 0

    @dataclass
    class _ControlledPrices:
        small_area: int = None
        big_area: int = None
        crane: int = None
        communications: int = None
        builder_diploma: int = None
        architect_diploma: int = None

    def __init__(self):
        """Инициализация."""
        self.salary = self._Salary()
        self.economy = self._Economy()
        self.licenses_life_time = self._LicensesLifeTime()
        self.treasury = self._Treasury()
        self.controlled_prices = self._ControlledPrices()

    def on_change_year(self):
        self.salary = self._Salary()
        self.economy = self._Economy()
        self.licenses_life_time = self._LicensesLifeTime()
        self.controlled_prices = self._ControlledPrices()

    def set_controlled_prices(self, data):
        self.controlled_prices.small_area = data.small_area
        self.controlled_prices.big_area = data.big_area
        self.controlled_prices.crane = data.crane
        self.controlled_prices.communications = data.communications
        self.controlled_prices.builder_diploma = data.builder_diploma
        self.controlled_prices.architect_diploma = data.architect_diploma

    def get_tax_percent(self):
        return 1 + (self.economy.tax / 100)

    def get_credit_percents(self):
        return self.economy.percent_credit

    def pay_tax(self, tax):
        self.treasury.wallet += tax

    def set_life_time_to_licenses(self, life_times):
        self.licenses_life_time.building_license = life_times.building_license
        self.licenses_life_time.architecting_license = life_times.architecting_license
        self.licenses_life_time.wood_license = life_times.wood_license
        self.licenses_life_time.glass_license = life_times.glass_license
        self.licenses_life_time.brick_license = life_times.brick_license
        self.licenses_life_time.shingles_license = life_times.shingles_license

    def get_life_times(self):
        data = {
            "building_license": self.licenses_life_time.building_license,
            "architecting_license": self.licenses_life_time.architecting_license,
            "wood_license": self.licenses_life_time.wood_license,
            "glass_license": self.licenses_life_time.glass_license,
            "brick_license": self.licenses_life_time.brick_license,
            "shingles_license": self.licenses_life_time.shingles_license,
        }
        return data

    def get_license_life_time_by_name(self, name):
        return getattr(self.licenses_life_time, name)

    def spend_wallet(self, amount):
        """."""
        self.treasury.wallet -= amount

    def cash_in_wallet(self, amount):
        """."""
        self.treasury.wallet += amount

    def check_money_in_wallet(self, amount):
        """."""
        if self.treasury.wallet >= amount:
            return True
        return False

    def make_paycheck(self, payments):
        """Назначить зарплаты министрам."""
        self.salary.president = payments.president
        self.salary.minister_economy = payments.minister_economy
        self.salary.minister_JKH = payments.minister_JKH
        self.salary.minister_education = payments.minister_education
        self.salary.MVD = payments.MVD
        self.salary.SMI = payments.SMI

    def pay_paycheck(self, ministers):
        """Выплатить зарплаты министрам (В конце года)."""
        self.spend_wallet(self.salary.total_wage)
        ministers["president"].game_role.increase_money(self.salary.president)
        ministers["minister_economy"].game_role.increase_money(
            self.salary.minister_economy
        )
        ministers["minister_JKH"].game_role.increase_money(self.salary.minister_JKH)
        ministers["minister_education"].game_role.increase_money(
            self.salary.minister_education
        )
        ministers["MVD"].game_role.increase_money(self.salary.MVD)
        if ministers.get("SMI_2"):
            ministers["SMI_1"].game_role.increase_money(self.salary.SMI / 2)
            ministers["SMI_2"].game_role.increase_money(self.salary.SMI / 2)
        else:
            ministers["SMI_1"].game_role.increase_money(self.salary.SMI)


class ResourcesPlayer:
    """Ресурсы игрока."""

    @dataclass
    class _NonTradeResources:
        """Не передаваемые ресурсы."""

        building_licenses: [License] = field(default_factory=list)
        architecting_licenses: [License] = field(default_factory=list)
        wood_licenses: [License] = field(default_factory=list)
        glass_licenses: [License] = field(default_factory=list)
        brick_licenses: [License] = field(default_factory=list)
        shingles_licenses: [License] = field(default_factory=list)
        building_diploma: bool = False
        architect_diploma: bool = False
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
        crane: int = 0
        communications: int = 0
        plan_of_small_house: int = 0
        plan_of_big_house: int = 0
        small_house: int = 0
        big_house: int = 0

    @dataclass
    class _IsResourceAvailable:
        """Флаги на проверку доступности ресурсов в этому году."""

        wood: bool = True
        brick: bool = True
        glass: bool = True
        shingles: bool = True

    def __init__(self):
        """Инициализация."""
        self.non_trade_resources = self._NonTradeResources()
        self.trade_resources = self._TradeResources()
        self.is_available = self._IsResourceAvailable()

    def on_change_year(self):

        wood_licenses = self.non_trade_resources.wood_licenses
        glass_licenses = self.non_trade_resources.glass_licenses
        brick_licenses = self.non_trade_resources.brick_licenses
        shingles_licenses = self.non_trade_resources.shingles_licenses

        self._change_accessibility()
        self._use_license(wood_licenses)
        self._use_license(glass_licenses)
        self._use_license(brick_licenses)
        self._use_license(shingles_licenses)

    def _change_accessibility(self):
        self.is_available.wood = True
        self.is_available.glass = True
        self.is_available.brick = True
        self.is_available.shingles = True

    @staticmethod
    def _use_license(licenses):
        for resource_license in licenses:
            result = resource_license.using_license()

            if not result:
                licenses.remove(resource_license)

    def add_new_licenses(self, resource_license):
        name = resource_license.resource
        attributes = dir(self.non_trade_resources)
        licenses = None
        for attribute in attributes:
            if attribute.startswith(name):
                licenses = getattr(self.non_trade_resources, attribute)

        licenses.append(resource_license)

    def add_new_advertising(self, quantity):
        self.non_trade_resources.advertising += quantity

    def get_building_license(self):
        return self.non_trade_resources.building_licenses

    def get_architecting_license(self):
        return self.non_trade_resources.architecting_licenses

    def to_json_trade_resources(self):
        data = {
            "money": self.trade_resources.money,
            "wood": self.trade_resources.wood,
            "glass": self.trade_resources.glass,
            "brick": self.trade_resources.brick,
            "shingles": self.trade_resources.shingles,
            "small_house": self.trade_resources.small_house,
            "big_house": self.trade_resources.big_house,
            "advertising": self.non_trade_resources.advertising,
            "small_area": self.trade_resources.small_area,
            "big_area": self.trade_resources.big_area,
            "crane": self.trade_resources.crane,
            "communications": self.trade_resources.communications,
            "plan_of_small_house": self.trade_resources.plan_of_small_house,
            "plan_of_big_house": self.trade_resources.plan_of_big_house,
        }
        return data

    def get_license_and_diploma(self):
        licences = [
            *[
                resource_license.to_json("Лицензия на строительство")
                for resource_license in self.non_trade_resources.building_licenses
            ],
            *[
                resource_license.to_json("Лицензия на архитектурную деятельность")
                for resource_license in self.non_trade_resources.architecting_licenses
            ],
            *[
                resource_license.to_json("Лицензия на дерево")
                for resource_license in self.non_trade_resources.wood_licenses
            ],
            *[
                resource_license.to_json("Лицензия на стекло")
                for resource_license in self.non_trade_resources.glass_licenses
            ],
            *[
                resource_license.to_json("Лицензия на кирпич")
                for resource_license in self.non_trade_resources.brick_licenses
            ],
            *[
                resource_license.to_json("Лицензия на черепицу")
                for resource_license in self.non_trade_resources.shingles_licenses
            ],
        ]

        diplomas = []

        if self.non_trade_resources.building_diploma:
            diplomas.append({"title": "Диплом строителя", "life_time": "Бессрочно"})

        if self.non_trade_resources.architect_diploma:
            diplomas.append({"title": "Диплом архитектора", "life_time": "Бессрочно"})

        data = [*licences, *diplomas]

        return data

    def build_small_house(self):
        resources = self.trade_resources
        result = self._is_enough_resource_for_small_house()
        if result:
            resources.wood -= 1
            resources.glass -= 1
            resources.brick -= 1
            resources.shingles -= 1
            resources.small_area -= 1
            resources.crane -= 1
            resources.communications -= 1
            resources.plan_of_small_house -= 1
            resources.small_house += 1
            resources.money += 1000
            return True, "Малый дом успешно построен!"
        return False, "У вас недостаточно ресурсов"

    def build_big_house(self):

        resources = self.trade_resources
        result = self._is_enough_resource_for_big_house()
        if result:
            resources.wood -= 2
            resources.glass -= 2
            resources.brick -= 2
            resources.shingles -= 2
            resources.big_area -= 1
            resources.crane -= 1
            resources.communications -= 1
            resources.plan_of_big_house -= 1
            resources.small_house += 1
            resources.money += 2000
            return True, "Большой дом успешно построен!"
        return False, "У вас недостаточно ресурсов"

    def _is_enough_resource_for_small_house(self):
        resources = self.trade_resources

        if (
            resources.wood < 1
            or resources.glass < 1
            or resources.brick < 1
            or resources.shingles < 1
            or resources.small_area < 1
            or resources.crane < 1
            or resources.communications < 1
            or resources.plan_of_small_house < 1
        ):
            return False
        return True

    def _is_enough_resource_for_big_house(self):
        resources = self.trade_resources

        if (
            resources.wood < 2
            or resources.glass < 2
            or resources.brick < 2
            or resources.shingles < 2
            or resources.big_area < 1
            or resources.crane < 1
            or resources.communications < 1
            or resources.plan_of_big_house < 1
        ):
            return False
        return True

    def get_possibilities(self):
        possibilities = []
        resource = self.non_trade_resources
        is_builder = resource.building_diploma and resource.building_licenses != []
        is_architect = (
            resource.architect_diploma and resource.architecting_licenses != []
        )
        if self._is_enough_resource_for_small_house() and is_builder:
            possibilities.append(
                {
                    "name": "Построить малый дом",
                    "attribute": "small_house",
                }
            )
        if self._is_enough_resource_for_big_house() and is_builder:
            possibilities.append(
                {
                    "name": "Построить большой дом",
                    "attribute": "big_house",
                }
            )
        if is_architect:
            possibilities.append(
                {
                    "name": "Начертить план большего дома",
                    "attribute": "small_house_plan",
                }
            )
            possibilities.append(
                {
                    "name": "Начертить план малого дома",
                    "attribute": "big_house_plan",
                }
            )
        if resource.shingles_licenses != [] and self.is_available.shingles:
            possibilities.append(
                {
                    "name": "Получить черепицу",
                    "attribute": "shingles",
                }
            )
        if resource.wood_licenses != [] and self.is_available.wood:
            possibilities.append({"name": "Получить дерево", "attribute": "wood"})
        if resource.glass_licenses != [] and self.is_available.glass:
            possibilities.append({"name": "Получить стекло", "attribute": "glass"})
        if resource.brick_licenses != [] and self.is_available.brick:
            possibilities.append({"name": "Получить кирпич", "attribute": "brick"})
        return possibilities

    def infinity(self):
        self.trade_resources.money = 999
        self.trade_resources.wood = 999
        self.trade_resources.glass = 999
        self.trade_resources.brick = 999
        self.trade_resources.shingles = 999
        self.trade_resources.small_area = 999
        self.trade_resources.big_area = 999
        self.trade_resources.crane = 999
        self.trade_resources.communications = 999
        self.trade_resources.plan_of_small_house = 999
        self.trade_resources.plan_of_big_house = 999
        self.trade_resources.small_house = 999
        self.trade_resources.big_house = 999
        self.non_trade_resources.advertising = 999
        self.non_trade_resources.architect_diploma = True
        self.non_trade_resources.building_diploma = True
        self.non_trade_resources.wood_licenses = [
            License(name="wood", life_time=2, player=None)
        ]
        self.non_trade_resources.architecting_licenses = [
            License(name="wood", life_time=2, player=None)
        ]
        self.non_trade_resources.building_licenses = [
            License(name="wood", life_time=2, player=None)
        ]
