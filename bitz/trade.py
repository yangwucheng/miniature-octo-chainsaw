import random
import time

from utils import build_bit_z_sign, http_post


class BitZTrade(object):
    ORDER_RESOURCE = '/api_v1/tradeAdd'
    CANCEL_RESOURCE = '/api_v1/tradeCancel'
    OPEN_ORDERS_RESOURCE = '/api_v1/openOrders'

    def __init__(self, url, api_key, secret_key, trade_pwd):
        self.__url = url
        self.__api_key = api_key
        self.__secret_key = secret_key
        self.__trade_pwd = trade_pwd

    def order(self, type, coin, price, number):
        params = {'api_key': self.__api_key, 'timestamp': str(int(time.time())),
                  'nonce': '%06d' % random.randint(0, 999999), 'coin': coin, 'type': type, 'price': str(price),
                  'number': str(number), 'tradepwd': self.__trade_pwd}
        params['sign'] = build_bit_z_sign(params, self.__secret_key)
        result = http_post(self.__url + BitZTrade.ORDER_RESOURCE, params)
        if result['code'] == 0:
            return result['data']
        print(result)
        return None

    def buy(self, coin, price, number):
        return self.order('in', coin, price, number)

    def sell(self, coin, price, number):
        return self.order('out', coin, price, number)

    def cancel_order(self, order_id):
        params = {'api_key': self.__api_key, 'id': str(order_id), 'timestamp': str(int(time.time())),
                  'nonce': '%06d' % random.randint(0, 999999)}
        params['sign'] = build_bit_z_sign(params, self.__secret_key)
        result = http_post(self.__url + BitZTrade.CANCEL_RESOURCE, params)
        return result

    def get_open_orders(self, coin):
        params = {'api_key': self.__api_key, 'timestamp': str(int(time.time())),
                  'nonce': '%06d' % random.randint(0, 999999), 'coin': coin}
        params['sign'] = build_bit_z_sign(params, self.__secret_key)
        result = http_post(self.__url + BitZTrade.OPEN_ORDERS_RESOURCE, params)
        return result

    def cancel_orders(self, open_orders):
        for open_order in open_orders:
            print('cancel order', open_order )
            self.cancel_order(open_order)

    def cancel_all_orders(self, coin):
        open_orders = self.get_open_orders(coin)
        self.cancel_orders(open_orders['data'])

    WITHDRAW_FEES = {
        'btc': {'fee_type': 'float', 'fee_ratio': 0.01, 'min_fee': 0.000000001, 'daily_quota': 10.00, 'min_amount': 0.01}
    }
    DEFAULT_WITHDRAW_FEE = {'fee_type': 'float', 'fee_ratio': 0.005, 'min_fee': 0.002, 'daily_quota': 1000.00, 'min_amount': 0.2}

    @staticmethod
    def withdraw_fee(coin, amount):
        # type: (str, float) -> float
        coin = coin.lower()
        if coin in BitZTrade.WITHDRAW_FEES:
            withdraw_fee = BitZTrade.WITHDRAW_FEES[coin]
        else:
            withdraw_fee = BitZTrade.DEFAULT_WITHDRAW_FEE

        if withdraw_fee['fee_type'] == 'float':
            fee = amount * withdraw_fee['fee_ratio']
            if fee < withdraw_fee['min_fee']:
                fee = withdraw_fee['min_fee']
        else:
            fee = withdraw_fee['fee_ratio']

        return fee

    TRADE_FEES = {
        'oc_btc': {'buy_fee_ratio': 0.001, 'sell_fee_ratio': 0.001, 'min_price': 0.00000001, 'max_price': 999999, 'min_quantity': 100.00}
    }
    DEFAULT_TRADE_FEE = {'buy_fee_ratio': 0.001, 'sell_fee_ratio': 0.001, 'min_price': 0.00000001, 'max_price': 999999, 'min_quantity': 100.00}

    @staticmethod
    def buy_fee(symbol, amount, price):
        # type: (str, float, float) -> float
        if symbol.lower() in BitZTrade.TRADE_FEES:
            trade_fee = BitZTrade.TRADE_FEES[symbol.lower()]
        else:
            trade_fee = BitZTrade.DEFAULT_TRADE_FEE

        return trade_fee['buy_fee_ratio'] * amount * price

    @staticmethod
    def sell_fee(symbol, amount, price):
        # type: (str, float, float) -> float
        if symbol.lower() in BitZTrade.TRADE_FEES:
            trade_fee = BitZTrade.TRADE_FEES[symbol.lower()]
        else:
            trade_fee = BitZTrade.DEFAULT_TRADE_FEE

        return trade_fee['sell_fee_ratio'] * amount * price

    @staticmethod
    def is_valid_order(symbol, amount, price):
        # type: (str, float, float) -> bool
        if symbol.lower() in BitZTrade.TRADE_FEES:
            trade_fee = BitZTrade.TRADE_FEES[symbol.lower()]
        else:
            trade_fee = BitZTrade.DEFAULT_TRADE_FEE

        return price >= trade_fee['min_price'] and price <= trade_fee['max_price'] and amount >= trade_fee['min_quantity']
