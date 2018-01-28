from utils import build_all_coin_sign, http_post


class AllCoinTrade(object):
    BALANCE_RESOURCE = '/api/v1/userinfo'
    ORDER_RESOURCE = '/api/v1/trade'
    CANCEL_RESOURCE = '/api/v1/cancel_order'
    OPEN_ORDERS_RESOURCE = '/api/v1/order_history'

    def __init__(self, url, api_key, secret_key):
        # type: (str, str, str) -> None
        self.__url = url
        self.__api_key = api_key
        self.__secret_key = secret_key

    def get_balance(self):
        """

        :return:
        {
            'info': {
                'funds': {
                    'free': {
                        'a0101': '0.0000000000000000',
                        'acc': '0.0000000000000000',
                        'act': '0.0000000000000000',
                        'aic': '0.0000000000000000',
                        'aicc': '0.0000000000000000',
                        'aidoc': '0.0000000000000000',
                        'atn': '0.0000000000000000',
                        'awr': '0.0000000000000000',
                        'bash': '0.0000000000000000',
                        'bcd': '0.0000000000000000',
                        'bch': '0.0000000000000000',
                        'bec': '0.0000000000000000',
                        'bot': '0.0000000000000000',
                        'btc': '0.0419170382000000',
                        'bte': '0.0000000000000000',
                        'btf': '0.0000000000000000',
                        'btg': '0.0000000000000000',
                        'btm': '0.0000000000000000',
                        'cfs': '0.0000000000000000',
                        'cfun': '0.0000000000000000',
                        'ck.usd': '0.0000000000000000',
                        'cnet': '0.0000000000000000',
                        'dbc': '0.0000000000000000',
                        'dwc': '0.0000000000000000',
                        'ent': '0.0000000000000000',
                        'eth': '0.0000000000000000',
                        'fid': '0.0000000000000000',
                        'game': '0.0000000000000000',
                        'gnx': '0.0000000000000000',
                        'god': '0.0000000000000000',
                        'gp': '0.0000000000000000',
                        'gxs': '0.0000000000000000',
                        'hlc': '0.0000000000000000',
                        'hpb': '0.0000000000000000',
                        'hsr': '0.0000000000000000',
                        'ink': '0.0000000000000000',
                        'int': '0.0000000000000000',
                        'iqt': '0.0000000000000000',
                        'kct': '0.0000000000000000',
                        'lbtc': '0.0000000000000000',
                        'lmc': '0.0000000000000000',
                        'ltc': '0.0000000000000000',
                        'mcc': '0.0000000000000000',
                        'mda': '0.0000000000000000',
                        'mgo': '0.0000000000000000',
                        'nas': '0.0000000000000000',
                        'neo': '0.0000000000000000',
                        'oc': '22725.1200000000000000',
                        'pcash': '0.0000000000000000',
                        'put': '0.0000000000000000',
                        'qbt': '0.0000000000000000',
                        'qtum': '0.0002990000000000',
                        'sbtc': '0.0000000000000000',
                        'sigma': '0.0000000000000000',
                        'spc': '0.0000000000000000',
                        'tsl': '0.0000000000000000',
                        'ugc': '0.0000000000000000',
                        'uip': '0.0000000000000000',
                        'usd': '0.0000000000000000',
                        'walton': '0.0000000000000000',
                        'wid': '0.0000000000000000',
                        'xkc': '0.0000000000000000',
                        'ybct': '0.0000000000000000',
                        'yuan': '0.0000000000000000',
                        'zec': '0.0000000000000000'
                    },
                    'freezed': {
                        'a0101': '0.0000000000000000',
                        'acc': '0.0000000000000000',
                        'act': '0.0000000000000000',
                        'aic': '0.0000000000000000',
                        'aicc': '0.0000000000000000',
                        'aidoc': '0.0000000000000000',
                        'atn': '0.0000000000000000',
                        'awr': '0.0000000000000000',
                        'bash': '0.0000000000000000',
                        'bcd': '0.0000000000000000',
                        'bch': '0.0000000000000000',
                        'bec': '0.0000000000000000',
                        'bot': '0.0000000000000000',
                        'btc': '0.0000000000000000',
                        'bte': '0.0000000000000000',
                        'btf': '0.0000000000000000',
                        'btg': '0.0000000000000000',
                        'btm': '0.0000000000000000',
                        'cfs': '0.0000000000000000',
                        'cfun': '0.0000000000000000',
                        'ck.usd': '0.0000000000000000',
                        'cnet': '0.0000000000000000',
                        'dbc': '0.0000000000000000',
                        'dwc': '0.0000000000000000',
                        'ent': '0.0000000000000000',
                        'eth': '0.0000000000000000',
                        'fid': '0.0000000000000000',
                        'game': '0.0000000000000000',
                        'gnx': '0.0000000000000000',
                        'god': '0.0000000000000000',
                        'gp': '0.0000000000000000',
                        'gxs': '0.0000000000000000',
                        'hlc': '0.0000000000000000',
                        'hpb': '0.0000000000000000',
                        'hsr': '0.0000000000000000',
                        'ink': '0.0000000000000000',
                        'int': '0.0000000000000000',
                        'iqt': '0.0000000000000000',
                        'kct': '0.0000000000000000',
                        'lbtc': '0.0000000000000000',
                        'lmc': '0.0000000000000000',
                        'ltc': '0.0000000000000000',
                        'mcc': '0.0000000000000000',
                        'mda': '0.0000000000000000',
                        'mgo': '0.0000000000000000',
                        'nas': '0.0000000000000000',
                        'neo': '0.0000000000000000',
                        'oc': '500.0000000000000000',
                        'pcash': '0.0000000000000000',
                        'put': '0.0000000000000000',
                        'qbt': '0.0000000000000000',
                        'qtum': '0.0000000000000000',
                        'sbtc': '0.0000000000000000',
                        'sigma': '0.0000000000000000',
                        'spc': '5951.0000000000000000',
                        'tsl': '0.0000000000000000',
                        'ugc': '0.0000000000000000',
                        'uip': '0.0000000000000000',
                        'usd': '0.0000000000000000',
                        'walton': '0.0000000000000000',
                        'wid': '0.0000000000000000',
                        'xkc': '0.0000000000000000',
                        'ybct': '0.0000000000000000',
                        'yuan': '0.0000000000000000',
                        'zec': '0.0000000000000000'
                    }
                }
            },
            'result': 'true'
        } {
            'oc': '22725.1200000000000000',
            'btc': '0.0419170382000000'
        }
        """
        params = {'api_key': self.__api_key}
        params['sign'] = build_all_coin_sign(params, self.__secret_key)
        return http_post(self.__url + AllCoinTrade.BALANCE_RESOURCE, params, verify=False)

    def get_fund_free(self, assets):
        # type: (list) -> dict
        """

        :return:
        {'oc': '22925.1200000000000000', 'btc': '0.0419170382000000'}
        """
        balance = self.get_balance()
        print(balance)
        fund_frees = {}
        for asset in assets:
            fund_frees[asset] = balance['info']['funds']['free'][asset]
        return fund_frees

    def order(self, order_type, symbol, price, amount):
        # type: (str, str, str, str) -> str
        """

        :param order_type:
        :param symbol:
        :param price:
        :param amount:
        :return:
        """
        params = {'api_key': self.__api_key, 'symbol': symbol, 'type': order_type, 'price': price,
                  'amount': amount}
        params['sign'] = build_all_coin_sign(params, self.__secret_key)
        # {'result': 'true', 'order_id': '59769693'}
        # {'error_code': '10013', 'result': False}
        result = http_post(self.__url + AllCoinTrade.ORDER_RESOURCE, params, verify=False)
        if result['result'] == 'true':
            return result['order_id']
        print(result)
        return None

    def buy(self, symbol, price, amount):
        # type: (str, str, str) -> str
        return self.order('buy', symbol, price, amount)

    def sell(self, symbol, price, amount):
        # type: (str, str, str) -> str
        return self.order('sell', symbol, price, amount)

    def cancel_order(self, symbol, order_id):
        # type: (str, str) -> object
        """

        :param symbol:
        :param order_id:
        :return:
        """
        params = {'api_key': self.__api_key, 'symbol': symbol, 'order_id': order_id}
        params['sign'] = build_all_coin_sign(params, self.__secret_key)
        # {'order_id': '59770590', 'result': True}
        result = http_post(self.__url + AllCoinTrade.CANCEL_RESOURCE, params, verify=False)
        if 'result' in result:
            return result['result']
        return result

    def get_open_orders(self, symbol):
        """

        :param symbol:
        :return:
        {
            'current_page': 1,
            'order': [{
                'amount': 100.0,
                'deal_amount': 0.0,
                'avg_price': 0.0,
                'create_data': 1517110886325,
                'order_id': 59768240,
                'price': 0.000214,
                'status': 0,
                'symbol': 'oc_btc',
                'type': 'sell'
            }],
            'page_length': 200,
            'total': 1
        }
        """
        params = {'api_key': self.__api_key, 'symbol': symbol, 'status': '0', 'current_page': 1, 'page_length': 200}
        params['sign'] = build_all_coin_sign(params, self.__secret_key)
        return http_post(self.__url + AllCoinTrade.OPEN_ORDERS_RESOURCE, params, verify=False)

    def cancel_orders(self, open_orders):
        for open_order in open_orders:
            if 'order_id' in open_order:
                print('cancel order', open_order)
                self.cancel_order(open_order['symbol'], str(open_order['order_id']))

    def cancel_all_orders(self, symbol):
        open_orders = self.get_open_orders(symbol)
        self.cancel_orders(open_orders['order'])
