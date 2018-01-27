import time

from utils import build_exx_sign, http_get


class ExxTrade(object):
    BALANCE_RESOURCE = '/api/getBalance'
    ORDER_RESOURCE = '/api/order'
    OPEN_ORDERS_RESOURCE = '/api/getOpenOrders'
    CANCEL_RESOURCE = '/api/cancel'

    def __init__(self, url, access_key, secret_key):
        self.__url = url
        self.__access_key = access_key
        self.__secret_key = secret_key

    def get_balance(self):
        # type: () -> dict
        params = {'accesskey': self.__access_key, 'nonce': str(int(time.time() * 1000))}
        params['signature'] = build_exx_sign(params, self.__secret_key)
        param_str = 'accesskey=%(accesskey)s&nonce=%(nonce)s&signature=%(signature)s' % params
        return http_get(self.__url + ExxTrade.BALANCE_RESOURCE + '?' + param_str)

    def get_fund_balance(self, assets):
        # type: (list) -> dict
        balance = self.get_balance()
        fund_balances = {}
        for asset in assets:
            fund_balances[asset] = balance['funds'][asset]['balance']
        return fund_balances

    def get_spc_qtum_balance(self):
        return self.get_fund_balance(['SPC', 'QTUM'])

    def order(self, order_type, currency, price, amount):
        # type: (str, str, float, float) -> str
        params = {'accesskey': self.__access_key, 'amount': str(amount), 'currency': currency,
                  'nonce': str(int(time.time() * 1000)), 'price': str(price), 'type': order_type}
        params['signature'] = build_exx_sign(params, self.__secret_key)
        param_str = 'accesskey=%(accesskey)s&amount=%(amount)s&currency=%(currency)s&nonce=%(nonce)s&price=%(' \
                    'price)s&type=%(type)s&signature=%(signature)s' % params
        result = http_get(self.__url + ExxTrade.ORDER_RESOURCE + '?' + param_str)
        if result['code'] == 100:
            return result['id']
        print(result['message'])
        return None

    def buy(self, currency, price, amount):
        return self.order('buy', currency, price, amount)

    def sell(self, currency, price, amount):
        return self.order('sell', currency, price, amount)

    def get_open_orders(self, currency, order_type):
        # type: (str, str) -> list
        params = {'accesskey': self.__access_key, 'currency': currency, 'nonce': str(int(time.time() * 1000)),
                  'pageIndex': '1', 'type': order_type}
        params['signature'] = build_exx_sign(params, self.__secret_key)
        param_str = 'accesskey=%(accesskey)s&currency=%(currency)s&nonce=%(nonce)s&pageIndex=%(pageIndex)s&type=%(' \
                    'type)s&signature=%(signature)s' % params
        return http_get(self.__url + ExxTrade.OPEN_ORDERS_RESOURCE + '?' + param_str)

    def cancel_order(self, currency, order_id):
        # type: (str, str) -> bool
        params = {'accesskey': self.__access_key, 'currency': currency, 'id': str(order_id),
                  'nonce': str(int(time.time() * 1000))}
        params['signature'] = build_exx_sign(params, self.__secret_key)
        param_str = 'accesskey=%(accesskey)s&currency=%(currency)s&id=%(id)s&nonce=%(nonce)s&signature=%(signature)s' % params
        result = http_get(self.__url + ExxTrade.CANCEL_RESOURCE + '?' + param_str)
        if result['code'] == 100:
            return True
        print(result['message'])
        return False

    def cancel_orders(self, open_orders):
        for open_order in open_orders:
            if 'id' in open_order:
                print('cancel order', open_order)
                self.cancel_order(open_order['currency'], open_order['id'])

    def cancel_all_orders(self, currency):
        open_orders = self.get_open_orders(currency, 'buy')
        self.cancel_orders(open_orders)

        open_orders = self.get_open_orders(currency, 'sell')
        self.cancel_orders(open_orders)

    WITHDRAW_FEES = {
        'qtum': {'fee_type': 'float', 'fee_ratio': 0.01, 'min_fee': 0.0000001, 'daily_quota': 5000.00, 'each_quota': 1000.00,
                 'min_amount': 0.0000001},
        'btc': {'fee_type': 'float', 'fee_ratio': 0.001, 'min_fee': 0.0000001, 'daily_quota': 10, 'each_quota': 3, 'min_amount': 0.0000001},
        'spc': {'fee_type': 'fixed', 'fee_ratio': 20.0, 'min_fee': 20, 'daily_quota': 1000000, 'each_quota': 100000,
                'min_amount': 100}
    }
    DEFAULT_WITHDRAW_FEE = {'fee_type': 'float', 'fee_ratio': 0.01, 'min_fee': 0.0000001, 'daily_quota': 5000.00, 'each_quota': 1000.00,
                            'min_amount': 0.0000001}

    @staticmethod
    def withdraw_fee(coin, amount):
        # type: (str, float) -> float
        coin = coin.lower()
        if coin in ExxTrade.WITHDRAW_FEES:
            withdraw_fee = ExxTrade.WITHDRAW_FEES[coin]
        else:
            withdraw_fee = ExxTrade.DEFAULT_WITHDRAW_FEE

        if withdraw_fee['fee_type'] == 'float':
            fee = amount * withdraw_fee['fee_ratio']
            if fee < withdraw_fee['min_fee']:
                fee = withdraw_fee['min_fee']
        else:
            fee = withdraw_fee['fee_ratio']

        return fee

    TRADE_FEE = 0.001

    @staticmethod
    def trade_fee(turnover):
        return turnover * ExxTrade.TRADE_FEE

    @staticmethod
    def buy_fee(currency, amount, price):
        return ExxTrade.trade_fee(amount * price)

    @staticmethod
    def sell_fee(currency, amount, price):
        return ExxTrade.trade_fee(amount * price)

    @staticmethod
    def is_valid_order(symbol, amount, price):
        return True
