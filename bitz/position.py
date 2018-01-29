import random
import time

from bitz.order import BitZOrder
from common.position import Position
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
            trade_pair_redis_key=trade_pair_redis_key
        )
        self.__url = url
        self.__api_key = api_key
        self.__secret_key = secret_key

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
        result = http_post(self.__url + BitZPosition.OPEN_ORDERS_RESOURCE, params)
        orders = []
        if result['code'] == 0:
            for order_dict in result['data']:
                if order_dict['id'] in order_ids:
                    order = BitZOrder(order_dict, symbol)
                    orders.append(order)
        return orders
