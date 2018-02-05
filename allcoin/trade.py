import logging
import time

import redis

from allcoin.helper import AllCoinHelper
from constants import Constants
from utils import build_all_coin_sign, http_post, extract_symbol


class AllCoinTrade(object):
    ORDER_RESOURCE = '/api/v1/trade'
    CANCEL_RESOURCE = '/api/v1/cancel_order'
    OPEN_ORDERS_RESOURCE = '/api/v1/order_history'
    ORDER_INFO_RESOURCE = '/api/v1/order_info'

    def __init__(self, url, api_key, secret_key):
        # type: (str, str, str) -> None
        self.__url = url
        self.__api_key = api_key
        self.__secret_key = secret_key
        self.__redis = redis.StrictRedis()
        logging.basicConfig(format='%(asctime)-15s %(name)-10s %(message)s', level=logging.DEBUG)
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(logging.DEBUG)

    def get_position(self, coin: str) -> float:
        """

        :param coin:
        :return: corresponding position
        """
        quantity = self.__redis.hget(Constants.REDIS_KEY_ALL_COIN_POSITIONS, coin)
        if quantity is None:
            quantity = 0.0
        else:
            quantity = float(quantity.decode())
        return quantity

    def update_position(self, coin: str, delta: float):
        quantity = self.get_position(coin)
        self.__redis.hset(Constants.REDIS_KEY_ALL_COIN_POSITIONS, coin, quantity + delta)

    def get_market_buy_quantity(self, symbol: str):
        market_buy_quantity = self.__redis.get(Constants.REDIS_KEY_ALL_COIN_MARKET_BUY_PREFIX + ':' + symbol)
        if market_buy_quantity is None:
            return 0.0
        return float(market_buy_quantity.decode())

    def update_market_buy_quantity(self, symbol: str, delta: float):
        old_market_buy_quantity = self.get_market_buy_quantity(symbol)
        self.__redis.set(Constants.REDIS_KEY_ALL_COIN_MARKET_BUY_PREFIX + ':' + symbol, old_market_buy_quantity + delta)

    def get_market_sell_quantity(self, symbol: str):
        market_sell_quantity = self.__redis.get(Constants.REDIS_KEY_ALL_COIN_MARKET_SELL_PREFIX + ':' + symbol)
        if market_sell_quantity is None:
            return 0.0
        return float(market_sell_quantity.decode())

    def update_market_sell_quantity(self, symbol: str, delta: float):
        old_market_sell_quantity = self.get_market_sell_quantity(symbol)
        self.__redis.set(Constants.REDIS_KEY_ALL_COIN_MARKET_SELL_PREFIX + ':' + symbol,
                         old_market_sell_quantity + delta)

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
            order_id = result['order_id']
            self.__logger.info('add order(%s) into open order ids when create', order_id)
            self.__redis.sadd(Constants.REDIS_KEY_ALL_COIN_OPEN_ORDER_IDS_PREFIX + ':' + symbol, order_id)
            self.__logger.info('hmset order(%s, %d, %s, %.8f, %.8f) when create',
                               order_id, AllCoinHelper.get_order_type(order_type),
                               symbol, price, amount)
            self.__redis.hmset(Constants.REDIS_KEY_ALL_COIN_ORDER_PREFIX + ':' + symbol + ':' + order_id, {
                'order_id': order_id,
                'order_type': AllCoinHelper.get_order_type(order_type),
                'symbol': symbol,
                'order_price': price,
                'avg_price': price,
                'quantity': amount,
                'filled_quantity': 0.0,
                'fee': 0.0,
                'created': time.time(),
                'status': Constants.ORDER_STATUS_NEW
            })
            trade_pair = extract_symbol(symbol)
            exchange_coin = trade_pair[0]
            base_coin = trade_pair[1]
            if order_type == 'buy':
                base_coin_delta = -1 * float(price) * float(amount)
                self.__logger.info('update base coin(%s, %.8f) position when create buy order(%s)',
                                   base_coin, base_coin_delta, order_id)
                self.update_position(base_coin, base_coin_delta)
                self.__logger.info('update market buy quantity(%s, %s) position when create buy order(%s)',
                                   symbol, amount, order_id)
                self.update_market_buy_quantity(symbol, float(amount))
            else:
                exchange_coin_delta = -1 * float(amount)
                self.__logger.info('update exchange coin(%s, %.8f) position when create sell order(%s)',
                                   exchange_coin, exchange_coin_delta, order_id)
                self.update_position(exchange_coin, exchange_coin_delta)
                self.__logger.info('update market sell quantity(%s, %s) position when create sell order(%s)',
                                   symbol, amount, order_id)
                self.update_market_sell_quantity(symbol, float(amount))
            return order_id
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
            self.__redis.srem(Constants.REDIS_KEY_ALL_COIN_OPEN_ORDER_IDS_PREFIX + ':' + symbol, order_id)
            self.__redis.sadd(Constants.REDIS_KEY_ALL_COIN_CANCELLED_ORDER_IDS_PREFIX + ':' + symbol, order_id)
            self.__redis.hset(Constants.REDIS_KEY_ALL_COIN_ORDER_PREFIX + ':' + symbol + ':' + order_id, 'status',
                              Constants.ORDER_STATUS_CANCELLED)
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

    def get_order_info(self, symbol, order_id):
        params = {'api_key': self.__api_key, 'symbol': symbol, 'order_id': order_id}
        params['sign'] = build_all_coin_sign(params, self.__secret_key)
        return http_post(self.__url + AllCoinTrade.ORDER_INFO_RESOURCE, params, verify=False)
