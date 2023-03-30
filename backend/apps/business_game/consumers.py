import time
from abc import ABC
from threading import Thread

from asgiref.sync import async_to_sync
from services.bussines_games.bussines_games import Game, GamesContainer, PlayerGame
from services.bussines_games.deocarators.decorators import (
    game_status_check,
    send_data_to_coordinator,
    validate,
)
from services.bussines_games.notice import Notice
from services.bussines_games.roles.roles import (
    Bank,
    MinisterEconomy,
    MinisterEducation,
    MinisterJKH,
    MinisterMVD,
    Ministers,
    President,
    RoleSMI,
)
from services.bussines_games.save_game.save_game import GameSaver, save_game
from services.bussines_games.utils.game_utils import GameStates
from services.bussines_games.validators.data_validators import (
    AcceptOrCloseData,
    AllChatData,
    ArchitectActions,
    BuilderActions,
    CreditCounterOffer,
    CreditData,
    LifeTimeLicensesData,
    Limits,
    MakePayCreditData,
    ManufacturerActions,
    PrivateChatData,
    TakeMoneyFromBankData,
    TradeData,
    TradeToEducationMinister,
    TradeToJKH,
    TradeToMVDData,
    TradeToSMI,
    WagesData,
)
from services.websockets.base_websocket_api import WebsocketActionAPI
from services.websockets.permissions import (
    access_true,
    is_bank,
    is_coordinator,
    is_economy_minister,
    is_education_minister,
    is_minister_jkh,
    is_mvd,
    is_player,
    is_president,
    is_smi,
)


class ConnectToGame(WebsocketActionAPI, ABC):
    connect_action_and_permissions = {"connect_to_game": [access_true]}

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.game = None
        self.game_id = None
        self.game_group_id = None

    def action_connect_to_game(self):
        connection_data = self._get_connection_data()
        player = self.game.get_player(self.user.id)
        self.send_to_channel(
            channel_name=self.channel_name,
            player=player,
            action="connect_to_game",
            data=connection_data.get("data"),
            notice=connection_data.get("notice"),
        )

    @save_game
    def connect(self):
        """Метод подключения к сокету игры."""
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.user = self.scope["user"]
        self.game_group_id = "game_%s" % self.game_id

        self.game: Game = self._load_game_id(self.game_id)
        if self.game:
            self._add_to_game()
            async_to_sync(self.channel_layer.group_add)(
                self.game_group_id, self.channel_name
            )
            self.accept()
            return
        self.close()

    @staticmethod
    def _load_game_id(game_id):
        """."""
        game: Game = (
            GamesContainer().get_game_by_game_id(game_id)
            or GameSaver.load_game(game_id)
            or GameSaver.load_reserve_file(game_id)
        )
        if not game:
            return None
        GamesContainer().load_game(game)
        return game

    def _get_connection_data(self):
        status = self.game.game_status
        result = getattr(self, status)()
        return result

    def lobby(self):
        if self.user.id == self.game.coordinator.coordinator_id:
            data = {
                "data": {
                    "time_start": {
                        "date": self.game.game_start_time.strftime("%d/%m/%Y"),
                        "time": self.game.game_start_time.strftime("%H:%M"),
                    },
                    "players": [
                        {"name": player.name, "id": player.player_id}
                        for player in self.game.players.values()
                        if player.player_id != self.user.id
                    ],
                    "game_status": GameStates.lobby,
                }
            }
        else:
            data = {
                "data": {
                    "time_start": {
                        "date": self.game.game_start_time.strftime("%d/%m/%Y"),
                        "time": self.game.game_start_time.strftime("%H:%M"),
                    },
                    "game_status": GameStates.lobby,
                    "players": [
                        {"name": player.name, "id": player.player_id}
                        for player in self.game.players.values()
                        if player.player_id != self.user.id
                    ],
                }
            }
        return data

    def in_process(self):
        if self.user.id == self.game.coordinator.coordinator_id:
            data = {
                "data": {
                    "time_start": {
                        "date": self.game.game_start_time.strftime("%d/%m/%Y"),
                        "time": self.game.game_start_time.strftime("%H:%M"),
                    },
                    "players": [
                        player.player_data_for_coordinator()
                        for player in self.game.players.values()
                    ],
                    "game_status": GameStates.in_process,
                }
            }
        else:
            data = self.game.get_player(self.user.id).player_data_for_player()
            data["data"]["players"] = [
                {"name": player.name, "id": player.player_id}
                for player in self.game.players.values()
                if player.player_id != self.user.id
            ]
        return data

    @staticmethod
    def changing_year():
        data = {
            "notice": Notice.create_info_notice(
                "Происходит смена года. Перейдите в чат."
            ),
        }
        return data

    def _add_to_game(self):

        if self.user.id == self.game.coordinator.coordinator_id:
            self.game.coordinator.connect(self.game, self.channel_name)
            return

        player = self.game.get_player(self.user.id)
        if not player:
            name = self.user.get_full_name() or self.user.email
            result = self.game.add_player(self.user.id, name, self.channel_name)
            if not result:
                self.send_to_channel(
                    self.channel_name,
                    notice=Notice.create_error_notice(
                        "Игра уже началась."
                        " К сожалению, вы не успели подключится вовремя."
                    ),
                )
                self.close()
        else:
            player.update_channel(self.channel_name)


class TradeResourcesMinistersConsumer(ConnectToGame, ABC):
    trade_with_ministers_action_and_permissions = {
        "send_trade_to_mvd": [is_player],
        "send_trade_to_jkh": [is_player],
        "send_trade_to_education_minister": [is_player],
        "send_trade_to_smi": [is_player],
    }

    def send_messages_to_player_and_minister(
        self, player, minister, seller_notice, buyer_notice
    ):

        player_trades = player.game_role.trades_with_ministers.get_all_items()
        minister_trades = minister.game_role.trades_with_ministers.get_all_items()

        self.send_to_channel(
            player.channel,
            player=player,
            data={"trades_with_ministers": player_trades},
            notice=seller_notice,
        )
        self.send_to_channel(
            minister.channel,
            player=minister,
            data={"trades_with_ministers": minister_trades},
            notice=buyer_notice,
        )

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @validate(validator=TradeToMVDData)
    def action_send_trade_to_mvd(self):
        data = self.validated_data

        player = self.game.get_player(self.user.id)
        minister_mvd = self.game.ministers.get_mvd()

        if minister_mvd == player:
            self.send_to_channel(
                minister_mvd.channel,
                notice=Notice.create_error_notice("Нельзя покупать у себя ресурсы!"),
            )
            return

        controlled_price = getattr(self.game.resources.controlled_prices, data.resource)
        if controlled_price < data.price_per_one:
            self.send_to_channel(
                player.channel,
                notice=Notice.create_error_notice(
                    "Указанная цена больше определенной министром экономики."
                ),
            )
            return

        result = player.game_role.send_offer_to_minister(
            minister=minister_mvd,
            resource=data.resource,
            quantity=data.quantity,
            price_per_one=data.price_per_one,
            trade_id=self.game.counter_ids.increase_counter(),
        )

        if not result[0]:
            self.send_to_channel(
                player.channel, notice=Notice.create_error_notice(result[1])
            )
            return

        self.send_messages_to_player_and_minister(
            player,
            minister_mvd,
            Notice.create_info_notice("Отправлено предложение обмена министру."),
            Notice.create_info_notice("Обмен отправлен на рассмотрение."),
        )

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @validate(validator=TradeToJKH)
    def action_send_trade_to_jkh(self):
        data = self.validated_data

        player = self.game.get_player(self.user.id)
        minister_jkh = self.game.ministers.get_minister_jkh()

        if data.resource_license == "building_license":
            building_licenses = player.game_role.resources.get_building_license()
            if len(building_licenses) > 0:
                self.send_to_channel(
                    player.channel,
                    notice=Notice.create_error_notice(
                        "Лицензия на строительство может быть только одна."
                    ),
                )
                return
        elif data.resource_license == "architecting_license":
            architecting_licenses = (
                player.game_role.resources.get_architecting_license()
            )
            if len(architecting_licenses) > 0:
                self.send_to_channel(
                    player.channel,
                    notice=Notice.create_error_notice(
                        "Лицензия на архитектурную деятельность может быть только одна."
                    ),
                )
                return

        result = player.game_role.send_offer_to_minister(
            minister=minister_jkh,
            resource=data.resource_license,
            quantity=1,
            price_per_one=data.price,
            trade_id=self.game.counter_ids.increase_counter(),
        )

        if not result[0]:
            self.send_to_channel(
                player.channel, notice=Notice.create_error_notice(result[1])
            )
            return

        self.send_messages_to_player_and_minister(
            player,
            minister_jkh,
            Notice.create_info_notice("Отправлено предложение обмена министру."),
            Notice.create_info_notice("Обмен отправлен на рассмотрение."),
        )

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @validate(validator=TradeToEducationMinister)
    def action_send_trade_to_education_minister(self):
        data = self.validated_data

        player = self.game.get_player(self.user.id)

        if player.game_role.get_diploma_state(data.diploma):
            self.send_to_channel(
                player.channel,
                notice=Notice.create_error_notice("У вас уже имеется диплом."),
            )
            return

        controlled_price = getattr(self.game.resources.controlled_prices, data.diploma)
        if controlled_price < data.price:
            self.send_to_channel(
                player.channel,
                notice=Notice.create_error_notice(
                    "Указанная цена больше определенной министром экономики."
                ),
            )
            return

        minister_education = self.game.ministers.get_minister_education()

        result = player.game_role.send_offer_to_minister(
            minister=minister_education,
            resource=data.diploma,
            quantity=1,
            price_per_one=data.price,
            trade_id=self.game.counter_ids.increase_counter(),
        )

        if not result[0]:
            self.send_to_channel(
                player.channel, notice=Notice.create_error_notice(result[1])
            )
            return

        self.send_messages_to_player_and_minister(
            player,
            minister_education,
            Notice.create_info_notice(
                "Отправлено предложение обмена министру образования."
            ),
            Notice.create_info_notice("Обмен отправлен на рассмотрение."),
        )

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @validate(validator=TradeToSMI)
    def action_send_trade_to_smi(self):
        data = self.validated_data
        player = self.game.get_player(self.user.id)
        smi = self.game.get_player(data.smi_id)

        result = player.game_role.send_offer_to_minister(
            minister=smi,
            resource="advertising",
            quantity=1,
            price_per_one=data.price_per_one,
            trade_id=self.game.counter_ids.increase_counter(),
        )

        if not result[0]:
            self.send_to_channel(
                player.channel, notice=Notice.create_error_notice(result[1])
            )
            return

        self.send_messages_to_player_and_minister(
            player,
            smi,
            Notice.create_info_notice("Отправлено предложение СМИ."),
            Notice.create_info_notice("Обмен отправлен на рассмотрение."),
        )


class TradeConsumer(ConnectToGame, ABC):
    trade_action_and_permissions = {
        "create_trade": [is_player],
        "accept_trade": [is_player],
        "close_trade": [is_player],
        "infinity_resources": [is_player],
    }

    def send_messages_to_seller_and_buyer(
        self, seller, buyer, seller_notice, buyer_notice
    ):

        seller_trades = seller.game_role.trades.incoming_trades(seller)
        buyer_trades = buyer.game_role.trades.incoming_trades(buyer)

        self.send_to_channel(
            seller.channel,
            player=seller,
            data={"trades": seller_trades},
            notice=seller_notice,
        )
        self.send_to_channel(
            buyer.channel,
            player=buyer,
            data={"trades": buyer_trades},
            notice=buyer_notice,
        )

    @save_game
    @send_data_to_coordinator
    def action_infinity_resources(self):
        current_player = self.game.get_player(self.user.id)
        current_player.game_role.resources.infinity()
        notice = Notice.create_info_notice("Ресурсы успешно зачислены.")
        self.send_to_channel(
            self.channel_name,
            player=current_player,
            notice=notice,
        )

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @validate(validator=TradeData)
    def action_create_trade(self):
        """."""
        data = self.validated_data
        buyer: PlayerGame = self.game.get_player(self.user.id)
        seller: PlayerGame = self.game.get_player(data.seller_id)

        result = buyer.game_role.send_offer_to_players(
            seller=seller,
            resource=data.resource,
            quantity=data.quantity,
            price_per_one=data.price_per_one,
            trade_id=self.game.counter_ids.increase_counter(),
        )

        if not result[0]:
            self.send_to_channel(
                buyer.channel, notice=Notice.create_error_notice(result[1])
            )
            return

        self.send_messages_to_seller_and_buyer(
            seller,
            buyer,
            Notice.create_info_notice("Новое предложение обмена."),
            Notice.create_info_notice("Обмен отправлен на рассмотрение."),
        )

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @send_data_to_coordinator
    @validate(validator=AcceptOrCloseData)
    def action_accept_trade(self):
        data: AcceptOrCloseData = self.validated_data

        current_player: PlayerGame = self.game.get_player(self.user.id)

        result = current_player.game_role.accept_offer(data.item_id)

        if not result[0]:
            self.send_to_channel(
                current_player.channel,
                notice=Notice.create_error_notice(result[1]),
            )
            return

        seller, buyer = result

        self.send_messages_to_seller_and_buyer(
            seller,
            buyer,
            Notice.create_info_notice("Обмен успешно совершен."),
            Notice.create_info_notice("Обмен успешно совершен."),
        )

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @validate(validator=AcceptOrCloseData)
    def action_close_trade(self):

        data: AcceptOrCloseData = self.validated_data

        current_player: PlayerGame = self.game.get_player(self.user.id)

        result = current_player.game_role.close_offer(data.item_id)

        if not result[0]:
            self.send_to_channel(
                current_player.channel,
                notice=Notice.create_error_notice(result[1]),
            )
            return

        seller, buyer = result

        self.send_messages_to_seller_and_buyer(
            seller,
            buyer,
            Notice.create_info_notice("Обмен отменен."),
            Notice.create_info_notice("Обмен отменен."),
        )


class CreditConsumer(ConnectToGame, ABC):
    credit_action_and_permissions = {
        "send_credit_offer": [is_player],
        "accept_credit_offer": [is_player, is_bank],
        "make_credit_pay": [is_player],
        "take_money_from_bank": [is_player, is_bank],
        "decline_credit_offer": [is_player],
        "counter_offer": [is_player, is_bank],
        "take_money_from_user": [is_player, is_bank],
    }

    def send_messages_to_player_and_bank(
        self, player, bank, player_notice, bank_notice
    ):
        player_credits = player.game_role.credits.get_all_items()
        credits_bank = bank.game_role.credits.get_all_items()

        self.send_to_channel(
            player.channel,
            player=player,
            data={"credits": player_credits},
            notice=player_notice,
        )
        self.send_to_channel(
            bank.channel,
            player=bank,
            data={"credits": credits_bank},
            notice=bank_notice,
        )

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @send_data_to_coordinator
    @validate(validator=MakePayCreditData)
    def action_take_money_from_user(self):
        data = self.validated_data
        bank = self.game.get_player(self.user.id)
        result = bank.take_money_from_user(data.item_id, data.money)

        if not result[0]:
            self.send_to_channel(
                self.send_to_channel(
                    bank.channel, notice=Notice.create_error_notice(result[1])
                )
            )
            return
        bank, player = result
        self.send_messages_to_player_and_bank(
            player,
            bank,
            Notice.create_info_notice("Банк изъял ваши деньги."),
            Notice.create_info_notice("Деньги успешно получены."),
        )

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @validate(validator=CreditCounterOffer)
    def action_counter_offer(self):
        data = self.validated_data
        bank = self.game.get_player(self.user.id)
        offer = bank.game_role.credits.get_item_by_id(data.item_id)
        player = offer.player
        result = bank.game_role.current_offer(offer, data.percent)

        if not result[0]:
            self.send_to_channel(
                bank.channel, notice=Notice.create_error_notice(result[1])
            )
            return

        self.send_messages_to_player_and_bank(
            player,
            bank,
            Notice.create_info_notice("Получено встречное предложение от банка."),
            Notice.create_info_notice("Встречное предложение отправлено."),
        )

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @validate(validator=AcceptOrCloseData)
    def action_decline_credit_offer(self):
        data = self.validated_data
        player_or_bank = self.game.get_player(self.user.id)

        result = player_or_bank.game_role.close_credit_offer(data.item_id)

        if not result[0]:
            self.send_to_channel(
                player_or_bank.channel,
                notice=Notice.create_error_notice(result[1]),
            )
            return

        bank, player = result

        self.send_messages_to_player_and_bank(
            player,
            bank,
            Notice.create_info_notice("Предложение кредита было отменено."),
            Notice.create_info_notice("Предложение кредита было отменено."),
        )

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @validate(validator=CreditData)
    def action_send_credit_offer(self):
        data: CreditData = self.validated_data

        current_user: PlayerGame = self.game.get_player(self.user.id)
        bank: PlayerGame = self.game.get_player(data.bank_id)

        result = current_user.game_role.send_credit_offer(
            data=data,
            bank=bank,
            credit_id=self.game.counter_ids.increase_counter(),
        )

        if not result[0]:
            self.send_to_channel(
                self.channel_name,
                notice=Notice.create_error_notice(result[1]),
            )
            return

        self.send_messages_to_player_and_bank(
            current_user,
            bank,
            Notice.create_info_notice(result[1]),
            Notice.create_info_notice("У вас новый запрос на кредит."),
        )

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @send_data_to_coordinator
    @validate(validator=AcceptOrCloseData)
    def action_accept_credit_offer(self):
        data: AcceptOrCloseData = self.validated_data

        bank: PlayerGame = self.game.get_player(self.user.id)

        result = bank.game_role.accept_credit_offer(data.item_id)

        if not result[0]:
            self.send_to_channel(
                self.channel_name,
                notice=Notice.create_error_notice(result[1]),
            )
            return
        bank, player = result

        self.send_messages_to_player_and_bank(
            player,
            bank,
            Notice.create_info_notice("Кредит одобрен."),
            Notice.create_info_notice("Кредит одобрен."),
        )

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @send_data_to_coordinator
    @validate(validator=MakePayCreditData)
    def action_make_credit_pay(self):
        data: MakePayCreditData = self.validated_data

        current_user: PlayerGame = self.game.get_player(self.user.id)

        result = current_user.game_role.make_pay(data.item_id, data.money)

        if not result:
            self.send_to_channel(
                self.channel_name,
                notice=Notice.create_error_notice(
                    "Не достаточно ресурсов для платежа."
                ),
            )
            return

        bank, player = result

        self.send_messages_to_player_and_bank(
            player,
            bank,
            Notice.create_info_notice("Платеж успешно совершен."),
            Notice.create_info_notice("Поступил платеж по кредиту."),
        )

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @send_data_to_coordinator
    @validate(validator=TakeMoneyFromBankData)
    def action_take_money_from_bank(self):
        data: TakeMoneyFromBankData = self.validated_data

        bank = self.game.get_player(self.user.id)

        result = bank.game_role.take_money(data.money)

        if not result[0]:
            self.send_to_channel(
                self.channel_name,
                notice=Notice.create_error_notice(result[1]),
            )
            return

        self.send_to_channel(
            bank.channel,
            player=bank,
            notice=Notice.create_info_notice("Средства успешно зачислены."),
        )


class ChatConsumer(ConnectToGame, ABC):
    chat_action_and_permissions = {
        "game_chat_send_message": [access_true],
        "private_chat_send_message": [access_true],
    }

    @game_status_check(
        statuses=[GameStates.in_process],
        special_status=[
            GameStates.president_time,
            GameStates.smi_1_time,
            GameStates.smi_2_time,
        ],
    )
    @validate(validator=AllChatData)
    def action_game_chat_send_message(self):
        """Метод отправки сообщения в общий чат."""
        data: AllChatData = self.validated_data
        message = data.message

        email_or_full_name = self.user.get_full_name() or self.user.email

        data_message = {"user": email_or_full_name, "message": message}

        self.send_to_the_group(self.game_group_id, data_message)

    # @game_status_check(statuses=[GameStates.in_process])
    @validate(validator=PrivateChatData)
    def action_private_chat_send_message(self):
        """Метод отправки в личный чат."""
        data: PrivateChatData = self.validated_data
        self.send_private_chat_message(data.user_id, data.message)

    def send_private_chat_message(self, receiver_id, message):
        sender: PlayerGame = self.game.get_player(self.user.id)
        receiver: PlayerGame = self.game.get_player(receiver_id)
        coordinator_channel = self.game.coordinator.channel

        sender_data = {
            "chat": receiver.player_id,
            "user": {
                "user_id": sender.player_id,
                "name": sender.name,
            },
            "message": message,
        }
        receiver_data = {
            "chat": sender.player_id,
            "user": {
                "user_id": sender.player_id,
                "name": sender.name,
            },
            "message": message,
        }
        coordinator_data = {
            "sender": sender.name,
            "receiver": receiver.name,
            "message": message,
        }
        self.send_to_channel(sender.channel, data=sender_data)
        self.send_to_channel(receiver.channel, data=receiver_data)
        self.send_to_channel(coordinator_channel, data=coordinator_data)


class PresidentConsumer(ConnectToGame, ABC):
    president_action_and_permissions = {
        "set_wages": [is_player, is_president],
    }

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @validate(validator=WagesData)
    def action_set_wages(self):
        """."""
        data: WagesData = self.validated_data

        total_wage = data.total_wage
        payments = data.payments

        president = self.game.get_player(self.user.id)

        is_set = president.game_role.make_paycheck(total_wage, payments)
        if is_set:
            self.send_to_channel(
                self.channel_name,
                notice=Notice.create_info_notice("Зарплата успешно назначена"),
            )
            return None
        self.send_to_channel(
            self.channel_name,
            notice=Notice.create_error_notice("В казне не достаточно средств"),
        )


class MVDConsumer(ConnectToGame, ABC):
    mvd_action_and_permissions = {
        "set_licenses_life_time": [is_player, is_mvd],
        "accept_mvd_trade": [is_player, is_mvd],
        "close_mvd_trade": [is_player, is_mvd],
    }

    def send_messages_to_player_and_minister(
        self, player, minister, player_notice, minister_notice
    ):

        player_trades = player.game_role.trades_with_ministers.get_all_items()
        minister_trades = minister.game_role.trades_with_ministers.get_all_items()

        self.send_to_channel(
            player.channel,
            player=player,
            data={"trades_with_ministers": player_trades},
            notice=player_notice,
        )
        self.send_to_channel(
            minister.channel,
            player=minister,
            data={"trades_with_ministers": minister_trades},
            notice=minister_notice,
        )

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @validate(validator=LifeTimeLicensesData)
    def action_set_licenses_life_time(self):
        data: LifeTimeLicensesData = self.validated_data

        minister_mvd = self.game.get_player(self.user.id)

        result = minister_mvd.game_role.set_licenses_life_time(data)

        if not result:
            pass

        self.send_to_channel(
            minister_mvd.channel,
            data={"life_times": self.game.resources.get_life_times()},
            notice=Notice.create_info_notice(result[0]),
        )

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @send_data_to_coordinator
    @validate(validator=AcceptOrCloseData)
    def action_accept_mvd_trade(self):

        minister_mvd = self.game.get_player(self.user.id)

        result = minister_mvd.game_role.accept_trade_with_minister_mvd(
            self.validated_data.item_id
        )

        if not result[0]:
            self.send_to_channel(
                minister_mvd.channel,
                notice=Notice.create_error_notice(result[1]),
            )
            return

        minister_mvd, player = result

        self.send_messages_to_player_and_minister(
            player,
            minister_mvd,
            Notice.create_info_notice("Министр МВД принял обмен."),
            Notice.create_info_notice("Обмен успешно принят."),
        )

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @validate(validator=AcceptOrCloseData)
    def action_close_mvd_trade(self):
        minister_mvd = self.game.get_player(self.user.id)

        result = minister_mvd.game_role.close_trade_with_minister_mvd(
            self.validated_data.item_id
        )

        if not result[0]:
            self.send_to_channel(
                minister_mvd.channel,
                notice=Notice.create_error_notice(result[1]),
            )
            return

        minister_mvd, player = result

        self.send_messages_to_player_and_minister(
            player,
            minister_mvd,
            Notice.create_info_notice("Министр МВД отменил обмен."),
            Notice.create_info_notice("Обмен успешно отменен."),
        )


class MinisterJKHConsumer(ConnectToGame, ABC):
    minister_jkh_action_and_permissions = {
        "accept_license_buy": [is_player, is_minister_jkh],
        "decline_license_buy": [is_player, is_minister_jkh],
    }

    def send_messages_to_player_and_minister(
        self, player, minister, player_notice, minister_notice
    ):

        player_trades = player.game_role.trades_with_ministers.get_all_items()
        minister_trades = minister.game_role.trades_with_ministers.get_all_items()

        self.send_to_channel(
            player.channel,
            player=player,
            data={"trades_with_ministers": player_trades},
            notice=player_notice,
        )
        self.send_to_channel(
            minister.channel,
            player=minister,
            data={"trades_with_ministers": minister_trades},
            notice=minister_notice,
        )

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @send_data_to_coordinator
    @validate(validator=AcceptOrCloseData)
    def action_accept_license_buy(self):
        data = self.validated_data

        minister_jkh = self.game.ministers.get_minister_jkh()

        result = minister_jkh.game_role.accept_trade_with_minister_jkh(data.item_id)

        if not result[0]:
            self.send_to_channel(
                minister_jkh.channel,
                notice=Notice.create_error_notice(result[1]),
            )
            return

        minister_mvd, player = result

        self.send_messages_to_player_and_minister(
            player,
            minister_mvd,
            Notice.create_info_notice("Министр ЖКХ подтвердил обмен."),
            Notice.create_info_notice("Обмен успешно подтвержден."),
        )

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @validate(validator=AcceptOrCloseData)
    def action_decline_license_buy(self):
        data = self.validated_data

        minister_jkh = self.game.ministers.get_minister_jkh()

        result = minister_jkh.game_role.close_trade_with_minister_jkh(data.item_id)

        if not result[0]:
            self.send_to_channel(
                minister_jkh.channel,
                notice=Notice.create_error_notice(result[1]),
            )
            return

        minister_mvd, player = result

        self.send_messages_to_player_and_minister(
            player,
            minister_mvd,
            Notice.create_info_notice("Министр ЖКХ отменил обмен."),
            Notice.create_info_notice("Обмен успешно отменен."),
        )


class EducationsMinisterConsumer(ConnectToGame, ABC):
    educations_minister_action_and_permissions = {
        "accept_diploma_buy": [is_player, is_education_minister],
        "decline_diploma_buy": [is_player, is_education_minister],
    }

    def send_messages_to_player_and_minister(
        self, player, minister, player_notice, minister_notice
    ):

        player_trades = player.game_role.trades_with_ministers.get_all_items()
        minister_trades = minister.game_role.trades_with_ministers.get_all_items()

        self.send_to_channel(
            player.channel,
            player=player,
            data={"trades_with_ministers": player_trades},
            notice=player_notice,
        )
        self.send_to_channel(
            minister.channel,
            player=minister,
            data={"trades_with_ministers": minister_trades},
            notice=minister_notice,
        )

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @send_data_to_coordinator
    @validate(validator=AcceptOrCloseData)
    def action_accept_diploma_buy(self):
        data = self.validated_data

        minister_education = self.game.ministers.get_minister_education()

        result = minister_education.game_role.accept_trade_with_minister_education(
            data.item_id
        )

        if not result[0]:
            self.send_to_channel(
                minister_education.channel,
                notice=Notice.create_error_notice(result[1]),
            )
            return

        minister_education, player = result

        self.send_messages_to_player_and_minister(
            player,
            minister_education,
            Notice.create_info_notice("Министр Образования подтвердил обмен."),
            Notice.create_info_notice("Обмен успешно подтвержден."),
        )

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @validate(validator=AcceptOrCloseData)
    def action_decline_diploma_buy(self):
        data = self.validated_data

        minister_education = self.game.ministers.get_minister_education()

        result = minister_education.game_role.close_trade_with_minister_education(
            data.item_id
        )

        if not result[0]:
            self.send_to_channel(
                minister_education.channel,
                notice=Notice.create_error_notice(result[1]),
            )
            return

        minister_education, player = result

        self.send_messages_to_player_and_minister(
            player,
            minister_education,
            Notice.create_info_notice("Министр Образования отменил обмен."),
            Notice.create_info_notice("Обмен успешно отменен."),
        )


class EconomyMinisterConsumer(ConnectToGame, ABC):
    finance_minister_action_and_permissions = {
        "set_controlled_prices": [is_player, is_economy_minister],
    }

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @validate(validator=Limits)
    def action_set_controlled_prices(self):
        data = self.validated_data
        minister_finance = self.game.ministers.get_minister_economy()
        minister_finance.game_role.set_limits(data)

        self.send_to_channel(
            self.channel_name,
            notice=Notice.create_info_notice("Ограничения установлены!"),
        )


class SMIConsumer(ConnectToGame, ABC):
    minister_smi_action_and_permissions = {
        "accept_advertising_buy": [is_player, is_smi],
        "decline_advertising_buy": [is_player, is_smi],
    }

    def send_messages_to_player_and_minister(
        self, player, minister, player_notice, minister_notice
    ):

        player_trades = player.game_role.trades_with_ministers.get_all_items()
        minister_trades = minister.game_role.trades_with_ministers.get_all_items()

        self.send_to_channel(
            player.channel,
            player=player,
            data={"trades_with_ministers": player_trades},
            notice=player_notice,
        )
        self.send_to_channel(
            minister.channel,
            player=minister,
            data={"trades_with_ministers": minister_trades},
            notice=minister_notice,
        )

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @send_data_to_coordinator
    @validate(validator=AcceptOrCloseData)
    def action_accept_advertising_buy(self):
        data = self.validated_data
        smi = self.game.get_player(self.user.id)

        result = smi.game_role.accept_trade_with_smi(data.item_id)

        if not result[0]:
            self.send_to_channel(
                smi.channel,
                notice=Notice.create_error_notice(result[1]),
            )
            return

        smi, player = result

        self.send_messages_to_player_and_minister(
            player,
            smi,
            Notice.create_info_notice("СМИ приняло предложение."),
            Notice.create_info_notice("Предложение принято."),
        )

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @validate(validator=AcceptOrCloseData)
    def action_decline_advertising_buy(self):
        data = self.validated_data

        smi = self.game.get_player(self.user.id)

        result = smi.game_role.close_trade_with_smi(data.item_id)

        if not result[0]:
            self.send_to_channel(
                smi.channel,
                notice=Notice.create_error_notice(result[1]),
            )
            return

        minister_education, player = result

        self.send_messages_to_player_and_minister(
            player,
            minister_education,
            Notice.create_info_notice("СМИ отклонило предложение."),
            Notice.create_info_notice("Предложение успешно отклонено."),
        )


class BaseRoleConsumer(ConnectToGame, ABC):
    base_role_action_and_permissions = {
        "get_house_plan": [is_player],
        "build_house": [is_player],
        "get_resource_by_license": [is_player],
    }

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @send_data_to_coordinator
    @validate(validator=ArchitectActions)
    def action_get_house_plan(self):
        data = self.validated_data
        player = self.game.get_player(self.user.id)
        result, message = player.game_role.get_plan(data.method)
        if not result:
            notice = Notice.create_error_notice(message)
        else:
            notice = Notice.create_info_notice(message)
        self.send_to_channel(
            player.channel,
            player=player,
            notice=notice,
        )

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @send_data_to_coordinator
    @validate(validator=BuilderActions)
    def action_build_house(self):
        data = self.validated_data
        player = self.game.get_player(self.user.id)
        result, message = player.game_role.get_house(data.method)
        if not result:
            notice = Notice.create_error_notice(message)
        else:
            notice = Notice.create_info_notice(message)
        self.send_to_channel(
            player.channel,
            player=player,
            notice=notice,
        )

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    @send_data_to_coordinator
    @validate(validator=ManufacturerActions)
    def action_get_resource_by_license(self):
        data = self.validated_data
        player = self.game.get_player(self.user.id)
        result, message = player.game_role.get_resource(data.method)
        if not result:
            notice = Notice.create_error_notice(message)
        else:
            notice = Notice.create_info_notice(message)
        self.send_to_channel(
            player.channel,
            player=player,
            notice=notice,
        )


class CoordinatorConsumer(ConnectToGame, ABC):
    coordinator_action_and_permissions = {
        "start_game": [is_coordinator],
        "change_year": [is_coordinator],
    }

    @game_status_check(statuses=[GameStates.lobby])
    @save_game
    def action_start_game(self):
        """Метод начала игры."""
        # if 16 <= len(self.game.players) <= 31:
        if True:
            self.game.set_game_status_in_process()
            self.game.set_role_for_users()
            # self.send_to_the_group()
            return
        self.send_to_channel(
            self.channel_name,
            notice=Notice.create_error_notice(
                "Невозможно начать игру. Допустимое число игроков от 16 до 31"
            ),
        )

    @game_status_check(statuses=[GameStates.in_process])
    @save_game
    def action_change_year(self):
        game = self.game
        game.set_game_status_changing_year()
        thread = Thread(target=self.chat_queue)

        thread.start()
        data = {
            "user": "console",
            "message": "Старый год подошел к концу!\n"
            "Новый год не заставит себя ждать. Игра продолжается!",
        }
        self.send_to_the_group(action="game_chat_send_message", data=data)
        game.on_change_year()
        game.set_game_status(GameStates.in_process)

    def chat_queue(self):
        def timer(message, end_message, name=""):
            for index in reversed(range(1, 11)):
                data = {
                    "user": "Console",
                    "message": message.format(index=index, name=name),
                }
                self.send_to_the_group(action="game_chat_send_message", data=data)
                time.sleep(1)
            else:
                data = {"user": "console", "message": end_message.format(name=name)}
                self.send_to_the_group(action="game_chat_send_message", data=data)

        game = self.game
        timer(
            message="До выступления президента осталось {index} сек.",
            end_message="Речь президента.",
        )
        game.set_game_status(GameStates.president_time)
        time.sleep(60)
        # smi_1 = game.ministers.get_smi_1()
        timer(
            message="До выступления СМИ:{name} осталось {index} сек.",
            end_message="Речь СМИ:{name}.",
            name="1",
        )
        time.sleep(60)
        # smi_2 = game.ministers.get_smi_2()
        timer(
            message="До выступления СМИ:{name} осталось {index} сек.",
            end_message="Речь СМИ:{name}.",
            name="2",
        )
        time.sleep(60)
        timer(
            message="Игра продолжится через {index} сек.",
            end_message="Речь СМИ:{name}.",
            name="2",
        )


class GameWebsocketAPI(
    MinisterJKHConsumer,
    EconomyMinisterConsumer,
    PresidentConsumer,
    TradeConsumer,
    ChatConsumer,
    CreditConsumer,
    TradeResourcesMinistersConsumer,
    MVDConsumer,
    EducationsMinisterConsumer,
    BaseRoleConsumer,
    CoordinatorConsumer,
    SMIConsumer,
):
    """Вебсокет для игры."""

    action_and_permissions = {
        "change_role": [is_player],
        "add_ministers": [is_player],
        "pay_paycheck": [is_player],
        "set_roles": [is_player],
        "test": [access_true],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @save_game
    def action_change_role(self):
        current_user: PlayerGame = self.game.get_player(self.user.id)
        current_user.game_role = MinisterEducation(
            self.game, current_user, game_role_name="minister_education"
        )
        self.game.resources.cash_in_wallet(500)
        # current_user.game_role.increase_bank_money(10000000)
        self.game.ministers = Ministers(minister_education=current_user)
        notice = Notice.create_info_notice("Роль успешно изменена.")
        self.send_to_channel(self.channel_name, notice=notice)

    @save_game
    def action_add_ministers(self):
        president = self.game.get_player(10)
        president.game_role = President(self.game, president)
        jkh = self.game.get_player(11)
        jkh.game_role = MinisterJKH(self.game, jkh)
        mvd = self.game.get_player(12)
        mvd.game_role = MinisterMVD(self.game, mvd)
        smi = self.game.get_player(13)
        smi.game_role = RoleSMI(self.game, smi)
        education = self.game.get_player(14)
        education.game_role = MinisterEducation(self.game, education)
        economy = self.game.get_player(15)
        economy.game_role = MinisterEconomy(self.game, economy)
        bank = self.game.get_player(16)
        bank.game_role = Bank(self.game, bank)
        player = self.game.get_player(18)
        self.game.ministers = Ministers(
            president=president,
            minister_economy=economy,
            minister_education=education,
            smi_1=smi,
            mvd=mvd,
            minister_jkh=jkh,
        )
        bank.game_role.increase_bank_money(10000000)
        self.game.resources.cash_in_wallet(500)
        player.game_role.resources.infinity()
        notice = Notice.create_info_notice("Роль успешно изменена.")
        self.send_to_channel(self.channel_name, notice=notice)

    @save_game
    def action_set_roles(self):
        president = self.game.get_player(10)
        president.game_role = President(self.game, president)
        jkh = self.game.get_player(11)
        jkh.game_role = MinisterJKH(self.game, jkh)
        mvd = self.game.get_player(12)
        mvd.game_role = MinisterMVD(self.game, mvd)
        smi = self.game.get_player(13)
        smi.game_role = RoleSMI(self.game, smi)
        education = self.game.get_player(14)
        education.game_role = MinisterEducation(self.game, education)
        economy = self.game.get_player(15)
        economy.game_role = MinisterEconomy(self.game, economy)

    @save_game
    def action_pay_paycheck(self):
        self.game.resources.pay_paycheck(self.game.ministers.get_all_ministers())

    @save_game
    def action_test(self):
        self.game.set_game_status_lobby()
        pass
