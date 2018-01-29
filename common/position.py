from abc import abstractmethod

import redis

from constants import Constants
from utils import extract_symbol


class Position(object):
    def __init__(self, init_positions: dict, position_redis_key: str, open_order_redis_key_prefix: str,
                 cancelled_order_redis_key_prefix: str, closed_order_redis_key_prefix: str,
                 order_redis_key_prefix: str, trade_pair_redis_key: str):
        self.__redis = redis.StrictRedis()
        self.__position_redis_key = position_redis_key
        self.__redis.hmset(position_redis_key, init_positions)
        self.__open_order_redis_key_prefix = open_order_redis_key_prefix
        self.__cancelled_order_redis_key_prefix = cancelled_order_redis_key_prefix
        self.__closed_order_redis_key_prefix = closed_order_redis_key_prefix
        self.__order_redis_key_prefix = order_redis_key_prefix
        self.__trade_pair_redis_key = trade_pair_redis_key

    @abstractmethod
    def get_orders(self, symbol: str, order_ids: list) -> list:
        """

        :param symbol:
        :param order_ids:
        :return: list of orders
        """
        pass

    def get_position(self, coin: str) -> float:
        """

        :param coin:
        :return: corresponding position
        """
        quantity = self.__redis.hget(self.__position_redis_key, coin)
        if quantity is None:
            quantity = 0.0
        else:
            quantity = float(quantity.decode())
        return quantity

    def update_position(self, coin: str, delta: float):
        quantity = self.get_position(coin)
        self.__redis.hset(self.__position_redis_key, coin, quantity + delta)

    def run(self):
        symbols = self.__redis.smembers(self.__trade_pair_redis_key)
        symbols = [x.decode() for x in symbols]

        for symbol in symbols:
            open_order_ids = self.__redis.smembers(self.__open_order_redis_key_prefix + ':' + symbol)
            open_order_ids = set([x.decode() for x in open_order_ids])
            cancelled_order_ids = self.__redis.smembers(self.__cancelled_order_redis_key_prefix + ':' + symbol)
            cancelled_order_ids = set([x.decode() for x in cancelled_order_ids])
            order_ids = open_order_ids | cancelled_order_ids
            orders = self.get_orders(symbol, order_ids)
            for order in orders:
                order_id = order.get_order_id()
                quantity = order.get_quantity()
                filled_quantity = order.get_filled_quantity()
                avg_price = order.get_avg_price()
                fee = order.get_fee()
                status = order.get_status()
                self.__redis.hmset(self.__order_redis_key_prefix + ':' + symbol + ':' + order_id, {
                    'order_id': order_id,
                    'avg_price': avg_price,
                    'filled_quantity': filled_quantity,
                    'fee': fee,
                    'status': status
                })

                if status == Constants.ORDER_STATUS_FILLED or status == Constants.ORDER_STATUS_CANCELLED:
                    trade_pair = extract_symbol(symbol)
                    exchange_coin = trade_pair[0]
                    base_coin = trade_pair[1]
                    if order.is_buy():
                        exchange_coin_delta = -1 * (fee / avg_price)
                        exchange_coin_delta += filled_quantity
                        if status == Constants.ORDER_STATUS_FILLED:
                            # base_coin_delta = -1 * avg_price * filled_quantity
                            # base coin has already update when create order
                            base_coin_delta = 0.0
                        else:
                            base_coin_delta = avg_price * (quantity - filled_quantity)
                    else:
                        if status == Constants.ORDER_STATUS_FILLED:
                            # exchange_coin_delta = -1 * filled_quantity
                            # exchange coin has already update when create order
                            exchange_coin_delta = 0.0
                        else:
                            exchange_coin_delta = quantity - filled_quantity
                        base_coin_delta = -1 * fee
                        base_coin_delta += avg_price * filled_quantity

                    self.update_position(exchange_coin, exchange_coin_delta)
                    self.update_position(base_coin, base_coin_delta)

            for order_id in cancelled_order_ids:
                self.__redis.srem(self.__cancelled_order_redis_key_prefix + ':' + symbol, order_id)
                self.__redis.sadd(self.__closed_order_redis_key_prefix + ':' + symbol, order_id)
