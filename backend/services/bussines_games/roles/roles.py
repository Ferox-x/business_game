from abc import ABC


class TradeStatus:
    """."""

    open = "Открытый"
    close = "Закрытый"
    accepted = "Принятый"


class Trade:
    """."""

    counter = 0

    def __init__(self, buyer, seller, resource, quantity, price_per_one):
        """."""
        self.counter += 1
        self.offer_id = self.counter
        self.seller = seller
        self.buyer = buyer
        self.resource = resource
        self.quantity = quantity
        self.price_per_one = price_per_one
        self.status = TradeStatus.open

    def send_trade_offer(self):
        """."""
        buyer = self.buyer

        buyer.game_role.add_open_trade(self)

    def accept_offer(self, offer_id):
        """."""
        pass

    def send_offer_to_minister(self, price_per_one, quantity):
        """."""
        pass

    def _check_resources(self, buyer_id, seller_id):
        """."""
        pass

    def to_json(self):
        """."""
        return {
            "seller": self.seller.player_id,
            "buyer": self.buyer.player_id,
            "resource": self.seller.player_id,
            "price_per_one": self.price_per_one,
            "status": self.status,
        }


class Credit:
    """."""

    counter = 0

    def __init__(self):
        """."""
        self.counter += 1
        self.offer_id = self.counter

    def take_credit(self):
        """."""
        pass

    def make_pay(self):
        """."""
        pass


class BaseRole(ABC):
    """Класс базовый для роли."""

    def __init__(self, game, player):
        """."""
        self.trades: {Trade} = {
            TradeStatus.open: {},
            TradeStatus.close: {},
            TradeStatus.accepted: {},
        }
        self.credits: {Credit} = {}
        self.game = game
        self.player = player

    def send_offer_to_player(self, seller_id, resource, quantity, price_per_one):
        """."""
        seller = self.game.get_player(seller_id)
        trade = Trade(
            buyer=self.player,
            seller=seller,
            resource=resource,
            quantity=quantity,
            price_per_one=price_per_one,
        )
        trade = self.add_open_trade(trade)
        trade.send_trade_offer()

    def add_open_trade(self, trade):
        """."""
        self.trades[TradeStatus.open][trade.offer_id] = trade
        return trade

    @classmethod
    def _to_json_trades(cls, trades: dict):
        """."""
        return {str(key): value.to_json() for key, value in trades.items()}

    def get_all_trades(self):
        """."""
        open_trades = self.trades.get(TradeStatus.open, {})
        closed_trades = self.trades.get(TradeStatus.close, {})
        accepted_trades = self.trades.get(TradeStatus.accepted, {})

        open_trades = self._to_json_trades(open_trades)
        closed_trades = self._to_json_trades(closed_trades)
        accepted_trades = self._to_json_trades(accepted_trades)

        return {
            TradeStatus.open: open_trades,
            TradeStatus.close: closed_trades,
            TradeStatus.accepted: accepted_trades,
        }


class President(BaseRole):
    """Роль президент."""

    pass


class MinisterEconomy(BaseRole):
    """Роль министр экономики."""

    pass


class MinisterJKH(BaseRole):
    """Роль министр ЖКХ."""

    pass


class MinisterMVD(BaseRole):
    """Роль министр МВД."""

    pass


class RoleSMI(BaseRole):
    """Роль СМИ."""

    pass


class MinisterEducation(BaseRole):
    """Роль министр Образования."""

    pass
