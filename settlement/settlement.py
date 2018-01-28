from abc import abstractmethod

from settlement.fee import Fee
from settlement.withdraw import Withdraw


class Settlement(object):
    def __init__(self):
        self.__withdraws = {}
        self.__withdraw_fees = {}
        self.__buy_fees = {}
        self.__sell_fees = {}

    @abstractmethod
    def get_buy_fee_dicts(self):
        pass

    @abstractmethod
    def get_default_buy_fee_dict(self):
        pass

    def get_buy_fee_calculator(self, exchange_pair):
        # type: (str) -> Fee
        exchange_pair_lower = exchange_pair.lower()
        if exchange_pair_lower not in self.__buy_fees:
            buy_fee_dict = self.get_default_buy_fee_dict()
            if exchange_pair_lower in self.get_buy_fee_dicts():
                buy_fee_dict = self.get_buy_fee_dicts()[exchange_pair_lower]
            buy_fee = Fee(buy_fee_dict)
            self.__buy_fees[exchange_pair_lower] = buy_fee
        return self.__buy_fees[exchange_pair_lower]

    @abstractmethod
    def get_sell_fee_dicts(self):
        pass

    @abstractmethod
    def get_default_sell_fee_dict(self):
        pass

    def get_sell_fee_calculator(self, exchange_pair):
        # type: (str) -> Fee
        exchange_pair_lower = exchange_pair.lower()
        if exchange_pair_lower not in self.__sell_fees:
            sell_fee_dict = self.get_default_sell_fee_dict()
            if exchange_pair_lower in self.get_sell_fee_dicts():
                sell_fee_dict = self.get_sell_fee_dicts()[exchange_pair_lower]
            sell_fee = Fee(sell_fee_dict)
            self.__sell_fees[exchange_pair_lower] = sell_fee
        return self.__sell_fees[exchange_pair_lower]

    def calculate_buy_fee(self, exchange_pair, price, quantity):
        # type: (str, float, float) -> float
        buy_fee_calculator = self.get_buy_fee_calculator(exchange_pair)
        return buy_fee_calculator.calculate_fee(price, quantity)

    def calculate_sell_fee(self, exchange_pair, price, quantity):
        # type: (str, float, float) -> float
        sell_fee_calculator = self.get_sell_fee_calculator(exchange_pair)
        return sell_fee_calculator.calculate_fee(price, quantity)

    @abstractmethod
    def get_withdraw_dicts(self):
        pass

    @abstractmethod
    def get_default_withdraw_dict(self):
        pass

    def get_withdraw(self, coin):
        # type: (str) -> Withdraw
        coin_lower = coin.lower()
        if coin_lower not in self.__withdraws:
            withdraw_dict = self.get_default_withdraw_dict()
            if coin_lower in self.get_withdraw_dicts():
                withdraw_dict = self.get_withdraw_dicts()[coin_lower]
            withdraw = Withdraw(withdraw_dict)
            self.__withdraws[coin_lower] = withdraw
        return self.__withdraws[coin_lower]

    def get_withdraw_fee_calculator(self, coin):
        # type: (str) -> Fee
        coin_lower = coin.lower()
        if coin_lower not in self.__withdraw_fees:
            fee_dict = self.get_default_withdraw_dict()
            if coin_lower in self.get_withdraw_dicts():
                fee_dict = self.get_withdraw_dicts()[coin_lower]
            withdraw_fee = Fee(fee_dict)
            self.__withdraw_fees[coin_lower] = withdraw_fee
        return self.__withdraw_fees[coin_lower]

    def calculate_withdraw_fee(self, coin, amount):
        # type: (str, float) -> float
        coin = coin.lower()
        withdraw_fee = self.get_withdraw_fee_calculator(coin)
        return withdraw_fee.calculate_fee(1.0, amount)
