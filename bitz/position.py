import random
import time

import redis

from bitz.order import BitZOrder
from common.position import Position
from constants import Constants
from utils import http_post, build_bit_z_sign


class BitZPosition(Position):
    OPEN_ORDERS_RESOURCE = '/api_v1/openOrders'

    def __init__(self,
                 init_positions,
                 position_redis_key,
                 open_order_redis_key_prefix,
                 cancelled_order_redis_key_prefix,
                 closed_order_redis_key_prefix,
                 order_redis_key_prefix,
                 trade_pair_redis_key,
                 market_buy_redis_key_prefix,
                 market_sell_redis_key_prefix,
                 url,
                 api_key,
                 secret_key
                 ):
        super(BitZPosition, self).__init__(
            init_positions=init_positions,
            position_redis_key=position_redis_key,
            open_order_redis_key_prefix=open_order_redis_key_prefix,
            cancelled_order_redis_key_prefix=cancelled_order_redis_key_prefix,
            closed_order_redis_key_prefix=closed_order_redis_key_prefix,
            order_redis_key_prefix=order_redis_key_prefix,
            trade_pair_redis_key=trade_pair_redis_key,
            market_buy_redis_key_prefix=market_buy_redis_key_prefix,
            market_sell_redis_key_prefix=market_sell_redis_key_prefix
        )
        self.__url = url
        self.__api_key = api_key
        self.__secret_key = secret_key
        self.__redis = redis.StrictRedis()

    def get_order_from_redis(self, symbol, order_id):
        order_dict = self.__redis.hgetall(Constants.REDIS_KEY_BIT_Z_ORDER_PREFIX + ':' + symbol + ':' + order_id)
        return BitZOrder(symbol=symbol, order_redis_dict=order_dict)

    def get_orders(self, symbol: str, order_ids: list) -> list:
        """

        :param symbol:
        :param order_ids:
        :return:
        {
            'code': 0,
            'msg': 'Success',
            'data': [{
                'id': '85493197',
                'price': '0.00000214',
                'number': '10000.0000',
                'numberover': '10000.0000',
                'flag': 'sale',
                'status': '0',
                'datetime': '2018-01-28 09:30:42'
            }]
        }
        """

        params = {'api_key': self.__api_key, 'timestamp': str(int(time.time())),
                  'nonce': '%06d' % random.randint(0, 999999), 'coin': symbol}
        params['sign'] = build_bit_z_sign(params, self.__secret_key)

        # {
        #     'code': 0,
        #     'msg': 'Success',
        #     'data': [{
        #         'id': '85493197',
        #         'price': '0.00000214',
        #         'number': '10000.0000',
        #         'numberover': '10000.0000',
        #         'flag': 'sale',
        #         'status': '0',
        #         'datetime': '2018-01-28 09:30:42'
        #     }]
        # }

        # {'code': 0, 'msg': 'Success', 'data': [
        # {'id': '87692842', 'price': '0.00800000', 'number': '1000.0000', 'numberover': '1000.0000', 'flag': 'sale', 'status': '0', 'datetime': '2018-01-30 09:25:53'},
        # {'id': '87692808', 'price': '0.00800000', 'number': '1000.0000', 'numberover': '1000.0000', 'flag': 'sale', 'status': '0', 'datetime': '2018-01-30 09:25:49'},
        # {'id': '87692733', 'price': '0.00800000', 'number': '1000.0000', 'numberover': '1000.0000', 'flag': 'sale', 'status': '0', 'datetime': '2018-01-30 09:25:44'}]
        # }

        result = http_post(self.__url + BitZPosition.OPEN_ORDERS_RESOURCE, params)
        orders = []
        response_order_ids = []
        if result['code'] == 0:
            for order_dict in result['data']:
                if order_dict['id'] in order_ids:
                    order = BitZOrder(order_dict, symbol)
                    orders.append(order)
                    response_order_ids.append(order_dict['id'])

            filled_order_ids = set(order_ids) - set(response_order_ids)
            for filled_order_id in filled_order_ids:
                order = self.get_order_from_redis(symbol, filled_order_id)
                order.set_status(Constants.ORDER_STATUS_FILLED)
                order.set_filled_quantity(order.get_quantity())
                order.set_avg_price(order.get_price())
                orders.append(order)

        return orders
