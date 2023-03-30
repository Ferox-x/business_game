from services.bussines_games.resources.lincenses.lincenses import License
from services.bussines_games.roles.generic.base_role import (
    Architect,
    Builder,
    Manufacturer,
)
from services.bussines_games.roles.generic.credit_role import CreditRole
from services.bussines_games.roles.generic.trade_role import TradeRole
from services.bussines_games.trades.container import ItemStatus


class BaseGameRole(CreditRole, TradeRole, Architect, Builder, Manufacturer):
    def to_json_role_data(self):
        return None


class President(BaseGameRole):
    """Роль президент."""

    def make_paycheck(self, total_wage, payments):
        """."""
        if not self.game.resources.check_money_in_wallet(total_wage):
            return False
        self.game.resources.make_paycheck(payments)
        self.game.resources.salary.total_wage = total_wage

        return True


class MinisterEconomy(BaseGameRole):
    """Роль министр экономики."""

    def set_limits(self, data):
        self.game.resources.set_controlled_prices(data)
        self.game.resources.economy.percent_credit = data.percent_credit
        self.game.resources.economy.tax = data.tax


class MinisterJKH(BaseGameRole):
    """Роль министр ЖКХ."""

    def accept_trade_with_minister_jkh(self, item_id):
        trade = self.trades_with_ministers.get_item_by_id(item_id)

        if not trade:
            return False, "Данного обмена не существует."

        try:
            trade.check_resources_minister_trade()
        except ValueError as ex:
            return False, str(ex)

        buyer = trade.buyer
        seller = trade.seller

        money_with_tax = trade.calculate_money_with_tax()

        self.game.resources.pay_tax(money_with_tax)

        buyer.game_role.decrease_money(money_with_tax)

        buyer.game_role.trades_with_ministers.open_pop(trade.item_id)
        seller.game_role.trades_with_ministers.open_pop(trade.item_id)

        buyer.game_role.trades_with_ministers.add_accepted_item(trade)
        seller.game_role.trades_with_ministers.add_accepted_item(trade)

        game = seller.game
        life_time = game.resources.get_license_life_time_by_name(trade.resource)
        new_license = License(name=trade.resource, life_time=life_time, player=buyer)
        buyer.game_role.resources.add_new_licenses(new_license)

        return seller, buyer

    def close_trade_with_minister_jkh(self, item_id):
        trade = self.trades_with_ministers.open_pop(item_id)

        if not trade:
            return False, "Данного обмена не существует."

        buyer = trade.buyer
        seller = trade.seller

        buyer.game_role.trades_with_ministers.open_pop(trade.item_id)
        seller.game_role.trades_with_ministers.open_pop(trade.item_id)

        buyer.game_role.trades_with_ministers.add_closed_item(trade)
        seller.game_role.trades_with_ministers.add_closed_item(trade)

        return seller, buyer

    def to_json_role_data(self):

        all_open_trades = self.trades_with_ministers.items.get(ItemStatus.open)
        return {
            str(trade.item_id): {**trade.to_json()}
            for trade in all_open_trades
            if trade.seller == self.player
        }


class MinisterMVD(BaseGameRole):
    """Роль министр МВД."""

    def set_licenses_life_time(self, life_times):
        self.game.resources.set_life_time_to_licenses(life_times)
        return True, "Время жизни лицензий успешно назначено."

    def accept_trade_with_minister_mvd(self, item_id):
        trade = self.trades_with_ministers.get_item_by_id(item_id)

        if not trade:
            return False, "Данного обмена не существует."

        try:
            trade.check_resources_minister_trade()
        except ValueError as ex:
            return False, str(ex)

        buyer = trade.buyer
        seller = trade.seller

        money_with_tax = trade.calculate_money_with_tax()

        self.game.resources.pay_tax(money_with_tax)

        buyer.game_role.decrease_money(money_with_tax)

        buyer.game_role.increase_resource_by_name(trade.resource, trade.quantity)

        buyer.game_role.trades_with_ministers.open_pop(trade.item_id)
        seller.game_role.trades_with_ministers.open_pop(trade.item_id)

        buyer.game_role.trades_with_ministers.add_accepted_item(trade)
        seller.game_role.trades_with_ministers.add_accepted_item(trade)

        return seller, buyer

    def close_trade_with_minister_mvd(self, item_id):
        trade = self.trades_with_ministers.open_pop(item_id)

        if not trade:
            return False, "Данного обмена не существует."

        buyer = trade.buyer
        seller = trade.seller

        buyer.game_role.trades_with_ministers.open_pop(trade.item_id)
        seller.game_role.trades_with_ministers.open_pop(trade.item_id)

        buyer.game_role.trades_with_ministers.add_closed_item(trade)
        seller.game_role.trades_with_ministers.add_closed_item(trade)

        return seller, buyer

    def to_json_role_data(self):

        all_open_trades = self.trades_with_ministers.items.get(ItemStatus.open)
        return {
            str(trade.item_id): {**trade.to_json()}
            for trade in all_open_trades
            if trade.seller == self.player
        }


class RoleSMI(BaseGameRole):
    """Роль СМИ."""

    def accept_trade_with_smi(self, item_id):
        trade = self.trades_with_ministers.get_item_by_id(item_id)

        if not trade:
            return False, "Данного обмена не существует."

        try:
            trade.check_resources_minister_trade()
        except ValueError as ex:
            return False, str(ex)

        buyer = trade.buyer
        seller = trade.seller

        money_with_tax = trade.calculate_money_with_tax()

        self.game.resources.pay_tax(money_with_tax)

        buyer.game_role.decrease_money(money_with_tax)

        buyer.game_role.trades_with_ministers.open_pop(trade.item_id)
        seller.game_role.trades_with_ministers.open_pop(trade.item_id)

        buyer.game_role.trades_with_ministers.add_accepted_item(trade)
        seller.game_role.trades_with_ministers.add_accepted_item(trade)

        buyer.game_role.resources.add_new_advertising(trade.quantity)

        return seller, buyer

    def close_trade_with_smi(self, item_id):
        trade = self.trades_with_ministers.open_pop(item_id)

        if not trade:
            return False, "Данного обмена не существует."

        buyer = trade.buyer
        seller = trade.seller

        buyer.game_role.trades_with_ministers.open_pop(trade.item_id)
        seller.game_role.trades_with_ministers.open_pop(trade.item_id)

        buyer.game_role.trades_with_ministers.add_closed_item(trade)
        seller.game_role.trades_with_ministers.add_closed_item(trade)

        return seller, buyer

    def to_json_role_data(self):

        all_open_trades = self.trades_with_ministers.get_all_items().get(
            ItemStatus.open
        )
        return {
            str(trade_id): {**trade}
            for trade_id, trade in all_open_trades.items()
            if trade["seller"] == self.player.name
        }


class MinisterEducation(BaseGameRole):
    """Роль министр Образования."""

    def accept_trade_with_minister_education(self, item_id):
        trade = self.trades_with_ministers.get_item_by_id(item_id)

        if not trade:
            return False, "Данного обмена не существует."

        try:
            trade.check_resources_minister_trade()
        except ValueError as ex:
            return False, str(ex)

        buyer = trade.buyer
        seller = trade.seller

        if buyer.game_role.get_diploma_state(trade.resource):
            buyer.game_role.trades_with_ministers.open_pop(trade.item_id)
            seller.game_role.trades_with_ministers.open_pop(trade.item_id)

            buyer.game_role.trades_with_ministers.add_closed_item(trade)
            seller.game_role.trades_with_ministers.add_closed_item(trade)

            return False, "У игрока уже имеется диплом. Обмен отклонен"

        buyer.game_role.trades_with_ministers.add_accepted_item(trade)
        seller.game_role.trades_with_ministers.add_accepted_item(trade)

        money_with_tax = trade.calculate_money_with_tax()
        self.game.resources.pay_tax(money_with_tax)
        buyer.game_role.decrease_money(money_with_tax)

        buyer.game_role.set_diploma_state(trade.resource, True)

        return seller, buyer

    def close_trade_with_minister_education(self, item_id):
        trade = self.trades_with_ministers.open_pop(item_id)

        if not trade:
            return False, "Данного обмена не существует."

        buyer = trade.buyer
        seller = trade.seller

        buyer.game_role.trades_with_ministers.open_pop(trade.item_id)
        seller.game_role.trades_with_ministers.open_pop(trade.item_id)

        buyer.game_role.trades_with_ministers.add_closed_item(trade)
        seller.game_role.trades_with_ministers.add_closed_item(trade)

        return seller, buyer

    def to_json_role_data(self):

        all_open_trades = self.trades_with_ministers.items.get(ItemStatus.open)
        return {
            str(trade.item_id): {**trade.to_json()}
            for trade in all_open_trades
            if trade.seller == self.player
        }


class Bank(BaseGameRole):
    def __init__(self, game, player):
        super().__init__(game, player)
        self.bank_money: int = 0
        self.banker_salary: int = 0

    def on_change_year(self):
        super().on_change_year()
        self.bank_money += 10000

    def get_bank_money(self):
        """Метод получения денег банка."""
        return self.bank_money

    def increase_bank_money(self, money):
        self.bank_money += money
        return self.bank_money

    def increase_banker_salary(self, money):
        self.banker_salary += money
        return self.banker_salary

    def decrease_bank_money(self, money):
        self.bank_money -= money
        return self.bank_money

    def decrease_banker_salary(self, money):
        self.banker_salary -= money
        return self.banker_salary

    def accept_credit_offer(self, credit_id):
        """Метод принятие кредита банком."""
        credit = self.credits.get_item_by_id(credit_id)

        bank = credit.bank
        player = credit.player

        try:
            credit.check_resources()
        except ValueError as ex:
            return False, str(ex)

        credit.change_status_to_accept()

        bank.game_role.credits.open_pop(credit_id)
        player.game_role.credits.open_pop(credit_id)

        bank.game_role.credits.add_accepted_item(credit)
        player.game_role.credits.add_accepted_item(credit)

        bank.game_role.decrease_bank_money(credit.total_money)
        player.game_role.increase_money(credit.total_money)

        return bank, player

    def take_money(self, money):

        if money >= self.banker_salary:
            return False, "У банка недостаточно средств"

        bank = self
        player = self

        bank.decrease_bank_money(money)
        player.increase_money(money)

        return True, None

    def current_offer(self, offer, percent):
        if self.game.resources.economy.percent_credit > percent:
            return False, "Указанный процент больше заданного министром экономики."
        offer.percent = percent
        return True, None

    def take_money_from_user(self, item_id, money):

        offer = self.credits.get_item_by_id(item_id)
        player = offer.player
        player_money = player.game_role.resources.money
        if player_money < money:
            money = player_money
        result = player.make_pay(item_id, money)
        return result

    def to_json_role_data(self):

        all_credits = self.credits.items

        open_credits = all_credits.get(ItemStatus.open)
        accepted_credits = all_credits.get(ItemStatus.accepted)
        return {
            "accepted": {
                str(credit.item_id): {**credit.to_json()}
                for credit in accepted_credits
                if credit.bank == self.player
            },
            "open": {
                str(credit.item_id): {**credit.to_json()}
                for credit in open_credits
                if credit.bank == self.player
            },
        }


class Ministers:
    def __init__(
        self,
        president: President = None,
        minister_economy: MinisterEconomy = None,
        minister_jkh: MinisterJKH = None,
        minister_education: MinisterEducation = None,
        mvd: MinisterMVD = None,
        smi_1: RoleSMI = None,
        smi_2: RoleSMI = None,
    ):
        self.president = president
        self.minister_economy = minister_economy
        self.minister_jkh = minister_jkh
        self.minister_education = minister_education
        self.mvd = mvd
        self.smi_1 = smi_1
        self.smi_2 = smi_2

    def get_all_ministers(self):
        """Получить всех министров."""
        ministers = {
            "president": self.president,
            "minister_economy": self.minister_economy,
            "minister_JKH": self.minister_jkh,
            "minister_education": self.minister_education,
            "MVD": self.mvd,
            "SMI_1": self.smi_1,
        }
        if self.smi_2 is not None:
            ministers["SMI_2"] = self.smi_2

        return ministers

    def get_president(self):
        """Получить президента."""
        return self.president

    def get_minister_economy(self):
        """Получить министра экономики."""
        return self.minister_economy

    def get_minister_jkh(self):
        """Получить министра ЖКХ."""
        return self.minister_jkh

    def get_minister_education(self):
        """Получить министра образования."""
        return self.minister_education

    def get_mvd(self):
        """Получить МВД."""
        return self.mvd

    def get_smi(self):
        """Получить все СМИ."""
        return self.smi_1, self.smi_2

    def get_smi_1(self):
        """Получить первое СМИ."""
        return self.smi_1

    def get_smi_2(self):
        """Получить второе СМИ."""
        return self.smi_2


class Banks:
    def __init__(self, banks: list):
        self.banks = banks

    def get_all_banks_name(self):
        dict_to_return = dict()

        for bank in self.banks:
            dict_to_return[str(bank.player_id)] = bank.name

        return dict_to_return
