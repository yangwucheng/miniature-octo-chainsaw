import redis

from allcoin.order import AllCoinOrder
from common.position import Position
from constants import Constants
from utils import build_all_coin_sign, http_post


class AllCoinPosition(Position):
    def get_order_from_redis(self, symbol, order_id):
        order_dict = self.__redis.hgetall(Constants.REDIS_KEY_ALL_COIN_ORDER_PREFIX + ':' + symbol + ':' + order_id)
        return AllCoinOrder(symbol=symbol, order_redis_dict=order_dict)

    OPEN_ORDERS_RESOURCE = '/api/v1/order_history'
    ORDERS_INFO_RESOURCE = '/api/v1/orders_info'

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
        super(AllCoinPosition, self).__init__(
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
        return http_post(self.__url + AllCoinPosition.OPEN_ORDERS_RESOURCE, params, verify=False)

    def get_orders_info(self, symbol: str, order_ids: str) -> dict:
        params = {'api_key': self.__api_key, 'symbol': symbol, 'type': '0', 'order_id': order_ids}
        params['sign'] = build_all_coin_sign(params, self.__secret_key)
        # {'result': True, 'order': [
        #     {'amount': 1046.0, 'deal_amount': 0.0, 'avg_price': 0.0, 'order_id': 60119534, 'create_data': 1517274712768,
        #      'price': 3e-07, 'status': 0, 'symbol': 'oc_btc', 'type': 'buy'},
        #     {'amount': 1046.0, 'deal_amount': 0.0, 'avg_price': 0.0, 'order_id': 60119539, 'create_data': 1517274717502,
        #      'price': 3e-07, 'status': 0, 'symbol': 'oc_btc', 'type': 'buy'}]}
        open_orders = http_post(self.__url + AllCoinPosition.ORDERS_INFO_RESOURCE, params, verify=False)

        params = {'api_key': self.__api_key, 'symbol': symbol, 'type': '1', 'order_id': order_ids}
        params['sign'] = build_all_coin_sign(params, self.__secret_key)
        close_orders = http_post(self.__url + AllCoinPosition.ORDERS_INFO_RESOURCE, params, verify=False)

        orders = {}
        if close_orders['result']:
            for close_order in close_orders['order']:
                order = AllCoinOrder(close_order)
                orders[order.get_order_id()] = order

        if open_orders['result']:
            for open_order in open_orders['order']:
                if open_order['order_id'] not in orders:
                    order = AllCoinOrder(open_order)
                    orders[order.get_order_id()] = order

        return orders

    def get_orders(self, symbol: str, order_ids: list) -> list:
        orders = []
        order_count = len(order_ids)
        per_request_count = 50
        start_index = 0
        while start_index < order_count:
            request_order_ids = order_ids[start_index:(start_index + per_request_count)]
            start_index += per_request_count
            request_order_id_strs = ','.join(request_order_ids)
            orders.extend(self.get_orders_info(symbol, request_order_id_strs).values())

        return orders
