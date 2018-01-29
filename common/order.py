from common.settlementfactory import SettlementFactory
from constants import Constants
from utils import extract_symbol


class Order(object):
    def __init__(self,
                 exchange=None,
                 order_id=None,
                 order_type=Constants.ORDER_TYPE_BUY,
                 symbol='oc_btc',
                 price=0.0,
                 avg_price=0.0,
                 quantity=0.0,
                 filled_quantity=0.0,
                 status=Constants.ORDER_STATUS_NEW
                 ):
        self.__exchange = exchange
        self.__order_id = order_id
        self.__order_type = order_type
        self.__symbol = symbol
        self.__exchange_coin = extract_symbol(symbol)[0]
        self.__base_coin = extract_symbol(symbol)[1]
        self.__price = price
        self.__avg_price = avg_price
        self.__quantity = quantity
        self.__filled_quantity = filled_quantity
        self.__settlement = SettlementFactory.get_settlement(exchange)
        if self.is_buy():
            self.__fee = self.__settlement.calculate_buy_fee(symbol, avg_price, filled_quantity)
        else:
            self.__fee = self.__settlement.calculate_sell_fee(symbol, avg_price, filled_quantity)
        self.__status = status

    def get_exchange(self):
        return self.__exchange

    def get_order_id(self):
        return self.__order_id

    def get_order_type(self):
        return self.__order_type

    def set_order_type(self, order_type):
        self.__order_type = order_type

    def get_symbol(self):
        return self.__symbol

    def get_quantity(self):
        return self.__quantity

    def get_filled_quantity(self):
        return self.__filled_quantity

    def get_avg_price(self):
        return self.__avg_price

    def get_fee(self):
        return self.__fee

    def get_status(self):
        return self.__status

    def is_buy(self) -> bool:
        if self.get_order_type() == Constants.ORDER_TYPE_BUY:
            return True
        return False

    def is_sell(self) -> bool:
        return not self.is_buy()
