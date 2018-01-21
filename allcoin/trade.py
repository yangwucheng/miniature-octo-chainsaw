from utils import build_all_coin_sign, http_post


class AllCoinTrade(object):
    BALANCE_RESOURCE = '/api/v1/userinfo'
    ORDER_RESOURCE = '/api/v1/trade'
    CANCEL_RESOURCE = '/api/v1/cancel_order'
    OPEN_ORDERS_RESOURCE = '/api/v1/order_history'

    def __init__(self, url, api_key, secret_key):
        self.__url = url
        self.__api_key = api_key
        self.__secret_key = secret_key

    def get_balance(self):
        params = {'api_key': self.__api_key}
        params['sign'] = build_all_coin_sign(params, self.__secret_key)
        return http_post(self.__url + AllCoinTrade.BALANCE_RESOURCE, params)

    def get_fund_free(self, assets):
        # type: (list) -> dict
        balance = self.get_balance()
        fund_frees = {}
        for asset in assets:
            fund_frees[asset] = balance['info']['funds']['free'][asset]
        return fund_frees

    def order(self, order_type, symbol, price, amount):
        # type: (str, str, float, float) -> str
        params = {'api_key': self.__api_key, 'symbol': symbol, 'type': order_type, 'price': str(price), 'amount': str(amount)}
        params['sign'] = build_all_coin_sign(params, self.__secret_key)
        result = http_post(self.__url + AllCoinTrade.ORDER_RESOURCE, params)
        if result['result']:
            return result['order_id']
        print(result)
        return None

    def buy(self, symbol, price, amount):
        return self.order('buy', symbol, price, amount)

    def sell(self, symbol, price, amount):
        return self.order('sell', symbol, price, amount)

    def cancel_order(self, symbol, order_id):
        params = {'api_key': self.__api_key, 'symbol': symbol, 'order_id': str(order_id)}
        params['sign'] = build_all_coin_sign(params, self.__secret_key)
        result = http_post(self.__url + AllCoinTrade.CANCEL_RESOURCE, params)
        if 'result' in result:
            return result['result']
        return result

    def get_open_orders(self, symbol):
        params = {'api_key': self.__api_key, 'symbol': symbol, 'status': '0', 'current_page': 1, 'page_length': 200}
        params['sign'] = build_all_coin_sign(params, self.__secret_key)
        return http_post(self.__url + AllCoinTrade.OPEN_ORDERS_RESOURCE, params)

    def cancel_orders(self, open_orders):
        for open_order in open_orders:
            if 'order_id' in open_order:
                print('cancel order', open_order )
                self.cancel_order(open_order['symbol'], open_order['order_id'])

    def cancel_all_orders(self, symbol):
        open_orders = self.get_open_orders(symbol)
        self.cancel_orders(open_orders['order'])

    WITHDRAW_FEES = {
        'qtum': {'fee_ratio': 0.002, 'min_fee': 0.002, 'daily_quota': 1000.00, 'min_amount': 0.2},
        'btc': {'fee_ratio': 0.002, 'min_fee': 0.0015, 'daily_quota': 50.00, 'min_amount': 0.01}
    }
    DEFAULT_WITHDRAW_FEE = {'fee_ratio': 0.002, 'min_fee': 0.002, 'daily_quota': 1000.00, 'min_amount': 0.2}

    @staticmethod
    def withdraw_fee(coin, amount):
        # type: (str, float) -> float
        coin = coin.lower()
        if coin in AllCoinTrade.WITHDRAW_FEES:
            withdraw_fee = AllCoinTrade.WITHDRAW_FEES[coin]
        else:
            withdraw_fee = AllCoinTrade.DEFAULT_WITHDRAW_FEE

        fee = amount * withdraw_fee['fee_ratio']
        if fee < withdraw_fee['min_fee']:
            fee = withdraw_fee['min_fee']

        return fee

    TRADE_FEES = {
        'spc_qtum': {'buy_fee_ratio': 0.0, 'sell_fee_ratio': 0.002, 'min_price': 0.000800, 'max_price': 0.800000, 'min_quantity': 2.00}
    }
    DEFAULT_TRADE_FEE = {'buy_fee_ratio': 0.0, 'sell_fee_ratio': 0.002, 'min_price': 0.000800, 'max_price': 0.800000, 'min_quantity': 2.00}

    @staticmethod
    def buy_fee(symbol, amount, price):
        # type: (str, float, float) -> float
        if symbol.lower() in AllCoinTrade.TRADE_FEES:
            trade_fee = AllCoinTrade.TRADE_FEES[symbol.lower()]
        else:
            trade_fee = AllCoinTrade.DEFAULT_TRADE_FEE

        return trade_fee['buy_fee_ratio'] * amount * price

    @staticmethod
    def sell_fee(symbol, amount, price):
        # type: (str, float, float) -> float
        if symbol.lower() in AllCoinTrade.TRADE_FEES:
            trade_fee = AllCoinTrade.TRADE_FEES[symbol.lower()]
        else:
            trade_fee = AllCoinTrade.DEFAULT_TRADE_FEE

        return trade_fee['sell_fee_ratio'] * amount * price

    @staticmethod
    def is_valid_order(symbol, amount, price):
        # type: (str, float, float) -> bool
        if symbol.lower() in AllCoinTrade.TRADE_FEES:
            trade_fee = AllCoinTrade.TRADE_FEES[symbol.lower()]
        else:
            trade_fee = AllCoinTrade.DEFAULT_TRADE_FEE

        return price >= trade_fee['min_price'] and price <= trade_fee['max_price'] and amount >= trade_fee['min_quantity']
