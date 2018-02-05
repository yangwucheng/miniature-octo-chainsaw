import logging
from abc import abstractmethod

import redis

from common.order import Order
from constants import Constants
from utils import extract_symbol


class Position(object):
    def __init__(self, init_positions: dict, position_redis_key: str, open_order_redis_key_prefix: str,
                 cancelled_order_redis_key_prefix: str, closed_order_redis_key_prefix: str,
                 order_redis_key_prefix: str, trade_pair_redis_key: str, market_buy_redis_key_prefix: str,
                 market_sell_redis_key_prefix: str):
        self.__redis = redis.StrictRedis()
        self.__position_redis_key = position_redis_key
        if init_positions is not None:
            self.__redis.hmset(position_redis_key, init_positions)
        self.__open_order_redis_key_prefix = open_order_redis_key_prefix
        self.__cancelled_order_redis_key_prefix = cancelled_order_redis_key_prefix
        self.__closed_order_redis_key_prefix = closed_order_redis_key_prefix
        self.__order_redis_key_prefix = order_redis_key_prefix
        self.__trade_pair_redis_key = trade_pair_redis_key
        self.__market_buy_redis_key_prefix = market_buy_redis_key_prefix
        self.__market_sell_redis_key_prefix = market_sell_redis_key_prefix

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

    @abstractmethod
    def get_order_from_redis(self, symbol: str, order_id: str) -> Order:
        pass

    def get_sell_quantity(self, symbol: str) -> float:
        sell_quantity = self.__redis.get(Constants.REDIS_KEY_SELL_QUANTITY_PREFIX + ':' + symbol)
        if sell_quantity is None:
            return 0.0
        return float(sell_quantity.decode())

    def update_sell_quantity(self, symbol: str, delta: float):
        old_sell_quantity = self.get_sell_quantity(symbol)
        self.__redis.set(Constants.REDIS_KEY_SELL_QUANTITY_PREFIX + ':' + symbol, old_sell_quantity + delta)

    def get_buy_quantity(self, symbol: str) -> float:
        buy_quantity = self.__redis.get(Constants.REDIS_KEY_BUY_QUANTITY_PREFIX + ':' + symbol)
        if buy_quantity is None:
            return 0.0
        return float(buy_quantity.decode())

    def update_buy_quantity(self, symbol: str, delta: float):
        old_buy_quantity = self.get_buy_quantity(symbol)
        self.__redis.set(Constants.REDIS_KEY_BUY_QUANTITY_PREFIX + ':' + symbol, old_buy_quantity + delta)

    def get_buy_price(self, symbol: str) -> float:
        buy_price = self.__redis.get(Constants.REDIS_KEY_BUY_PRICE_PREFIX + ':' + symbol)
        if buy_price is None:
            return 0.0
        return float(buy_price.decode())

    def update_buy_price(self, symbol: str, filled_quantity: float, avg_price: float, old_filled_quantity: float,
                         old_avg_price: float):
        old_buy_price = self.get_buy_price(symbol)
        old_buy_quantity = self.get_buy_quantity(symbol)

        if (old_buy_quantity - old_filled_quantity + filled_quantity) > 0.00000001:
            buy_price = (
                            old_buy_price * old_buy_quantity - old_filled_quantity * old_avg_price + filled_quantity * avg_price) \
                        / (old_buy_quantity - old_filled_quantity + filled_quantity)
        else:
            buy_price = avg_price

        self.__redis.set(Constants.REDIS_KEY_BUY_PRICE_PREFIX + ':' + symbol, buy_price)

    def get_sell_price(self, symbol: str) -> float:
        sell_price = self.__redis.get(Constants.REDIS_KEY_SELL_PRICE_PREFIX + ':' + symbol)
        if sell_price is None:
            return 0.0
        return float(sell_price.decode())

    def update_sell_price(self, symbol: str, filled_quantity: float, avg_price: float, old_filled_quantity: float,
                          old_avg_price: float):
        old_sell_price = self.get_sell_price(symbol)
        old_sell_quantity = self.get_sell_quantity(symbol)

        if (old_sell_quantity - old_filled_quantity + filled_quantity) > 0.00000001:
            sell_price = (
                                 old_sell_price * old_sell_quantity - old_filled_quantity * old_avg_price + filled_quantity * avg_price) \
                         / (old_sell_quantity - old_filled_quantity + filled_quantity)
        else:
            sell_price = avg_price

        self.__redis.set(Constants.REDIS_KEY_SELL_PRICE_PREFIX + ':' + symbol, sell_price)

    def get_market_buy_quantity(self, symbol: str):
        market_buy_quantity = self.__redis.get(self.__market_buy_redis_key_prefix + ':' + symbol)
        if market_buy_quantity is None:
            return 0.0
        return float(market_buy_quantity.decode())

    def update_market_buy_quantity(self, symbol: str, delta: float):
        old_market_buy_quantity = self.get_market_buy_quantity(symbol)
        self.__redis.set(self.__market_buy_redis_key_prefix + ':' + symbol, old_market_buy_quantity + delta)

    def get_market_sell_quantity(self, symbol: str):
        market_sell_quantity = self.__redis.get(self.__market_sell_redis_key_prefix + ':' + symbol)
        if market_sell_quantity is None:
            return 0.0
        return float(market_sell_quantity.decode())

    def update_market_sell_quantity(self, symbol: str, delta: float):
        old_market_sell_quantity = self.get_market_sell_quantity(symbol)
        self.__redis.set(self.__market_sell_redis_key_prefix + ':' + symbol, old_market_sell_quantity + delta)

    def run(self):
        symbols = self.__redis.smembers(self.__trade_pair_redis_key)
        symbols = [x.decode() for x in symbols]
        open_orders_by_symbol = {}

        for symbol in symbols:
            open_order_ids = self.__redis.smembers(self.__open_order_redis_key_prefix + ':' + symbol)
            open_order_ids = set([x.decode() for x in open_order_ids])
            cancelled_order_ids = self.__redis.smembers(self.__cancelled_order_redis_key_prefix + ':' + symbol)
            cancelled_order_ids = set([x.decode() for x in cancelled_order_ids])
            order_ids = list(open_order_ids | cancelled_order_ids)
            orders = self.get_orders(symbol, order_ids)
            for order in orders:
                order_id = order.get_order_id()
                quantity = order.get_quantity()
                filled_quantity = order.get_filled_quantity()
                avg_price = order.get_avg_price()
                fee = order.get_fee()
                status = order.get_status()

                old_order = self.get_order_from_redis(symbol, order_id)
                old_filled_quantity = old_order.get_filled_quantity()
                old_avg_price = old_order.get_avg_price()
                old_fee = old_order.get_fee()

                if order.get_status() == Constants.ORDER_STATUS_FILLED:
                    self.__logger.info('remove order id %s from open order ids when order filled', order_id)
                    self.__redis.srem(self.__open_order_redis_key_prefix + ':' + symbol, order_id)

                self.__logger.info('hmset order (%s, %.8f, %.8f, %.8f, %d) when get order',
                                   order_id, avg_price, filled_quantity, fee, status)
                self.__redis.hmset(self.__order_redis_key_prefix + ':' + symbol + ':' + order_id, {
                    'order_id': order_id,
                    'avg_price': avg_price,
                    'filled_quantity': filled_quantity,
                    'fee': fee,
                    'status': status
                })

                trade_pair = extract_symbol(symbol)
                exchange_coin = trade_pair[0]
                base_coin = trade_pair[1]

                if order.is_buy():
                    self.__logger.info('update buy price (%s, %.8f, %.8f, %.8f, %.8f) when get order (%s)',
                                       symbol, filled_quantity, avg_price, old_filled_quantity, old_avg_price, order_id)
                    self.update_buy_price(symbol, filled_quantity, avg_price, old_filled_quantity, old_avg_price)
                    self.__logger.info('update buy quantity (%s, %.8f) when get order (%s)',
                                       symbol, filled_quantity - old_filled_quantity, order_id)
                    self.update_buy_quantity(symbol, filled_quantity - old_filled_quantity)

                    self.update_market_buy_quantity(symbol, old_filled_quantity - filled_quantity)
                else:
                    self.__logger.info('update sell price (%s, %.8f, %.8f, %.8f, %.8f) when get order (%s)',
                                       symbol, filled_quantity, avg_price, old_filled_quantity, old_avg_price, order_id)
                    self.update_sell_price(symbol, filled_quantity, avg_price, old_filled_quantity, old_avg_price)
                    self.__logger.info('update sell quantity (%s, %.8f) when get order (%s)',
                                       symbol, filled_quantity - old_filled_quantity, order_id)
                    self.update_sell_quantity(symbol, filled_quantity - old_filled_quantity)

                    self.update_market_sell_quantity(symbol, old_filled_quantity - filled_quantity)

                if status == Constants.ORDER_STATUS_FILLED or status == Constants.ORDER_STATUS_CANCELLED:
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

                    self.__logger.info("update exchange coin(%s, %.8f) position when order(%s) finished",
                                       exchange_coin, exchange_coin_delta, order_id)
                    self.update_position(exchange_coin, exchange_coin_delta)
                    self.__logger.info("update base coin(%s, %.8f) position when order(%s) finished",
                                       base_coin, base_coin_delta, order_id)
                    self.update_position(base_coin, base_coin_delta)
                else:
                    if symbol not in open_orders_by_symbol:
                        open_orders_by_symbol[symbol] = []
                    open_orders_by_symbol[symbol].append(order)

            for order_id in cancelled_order_ids:
                self.__logger.info("remove order(%s) from cancelled orders when finish cancel",
                                   order_id)
                self.__redis.srem(self.__cancelled_order_redis_key_prefix + ':' + symbol, order_id)
                self.__logger.info("add order(%s) into closed orders when finish cancel",
                                   order_id)
                self.__redis.sadd(self.__closed_order_redis_key_prefix + ':' + symbol, order_id)

        return open_orders_by_symbol
