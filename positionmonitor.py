import configparser

import redis

from allcoin.market import AllCoinMarket
from allcoin.position import AllCoinPosition
from allcoin.settlement import AllCoinSettlement
from allcoin.trade import AllCoinTrade
from bitz.market import BitZMarket
from bitz.position import BitZPosition
from bitz.settlement import BitZSettlement
from bitz.trade import BitZTrade
from common.settlementfactory import SettlementFactory
from constants import Constants

# read config
config = configparser.ConfigParser()
config.read(['config.ini', 'secret_config.ini'])

# all coin config
all_coin_trade_url = config['allcoin']['trade_url']
all_coin_api_key = config['allcoin']['api_key']
all_coin_secret_key = config['allcoin']['secret_key']

# all coin position manager
all_coin_position = AllCoinPosition(
    init_positions={
        'oc': 0.0,
        'btc': 0.08604735
    },
    position_redis_key=Constants.REDIS_KEY_ALL_COIN_POSITIONS,
    open_order_redis_key_prefix=Constants.REDIS_KEY_ALL_COIN_OPEN_ORDER_IDS_PREFIX,
    cancelled_order_redis_key_prefix=Constants.REDIS_KEY_ALL_COIN_CANCELLED_ORDER_IDS_PREFIX,
    closed_order_redis_key_prefix=Constants.REDIS_KEY_ALL_COIN_CLOSED_ORDER_IDS_PREFIX,
    order_redis_key_prefix=Constants.REDIS_KEY_ALL_COIN_ORDER_PREFIX,
    trade_pair_redis_key=Constants.REDIS_KEY_ALL_COIN_TRADE_PAIRS,
    url=all_coin_trade_url,
    api_key=all_coin_api_key,
    secret_key=all_coin_secret_key
)

# bit z config
bit_z_trade_url = config['bitz']['trade_url']
bit_z_api_key = config['bitz']['api_key']
bit_z_secret_key = config['bitz']['secret_key']

# bit z position manager
bit_z_position = BitZPosition(
    init_positions={
        'oc': 45454.49000000,
        'btc': 0.0
    },
    position_redis_key=Constants.REDIS_KEY_BIT_Z_POSITIONS,
    open_order_redis_key_prefix=Constants.REDIS_KEY_BIT_Z_OPEN_ORDER_IDS_PREFIX,
    cancelled_order_redis_key_prefix=Constants.REDIS_KEY_BIT_Z_CANCELLED_ORDER_IDS_PREFIX,
    closed_order_redis_key_prefix=Constants.REDIS_KEY_BIT_Z_CLOSED_ORDER_IDS_PREFIX,
    order_redis_key_prefix=Constants.REDIS_KEY_BIT_Z_ORDER_PREFIX,
    trade_pair_redis_key=Constants.REDIS_KEY_BIT_Z_TRADE_PAIRS,
    url=bit_z_trade_url,
    api_key=bit_z_api_key,
    secret_key=bit_z_secret_key
)

# settlement set up
all_coin_settlement = AllCoinSettlement()
bit_z_settlement = BitZSettlement()
SettlementFactory.settlements = {
    Constants.EXCHANGE_NAME_ALL_COIN: all_coin_settlement,
    Constants.EXCHANGE_NAME_BIT_Z: bit_z_settlement
}
SettlementFactory.default_settlement = bit_z_settlement

# init trading pairs
r = redis.StrictRedis()
oc_btc_symbol = 'oc_btc'
r.sadd(Constants.REDIS_KEY_ALL_COIN_TRADE_PAIRS, oc_btc_symbol)
r.sadd(Constants.REDIS_KEY_BIT_Z_TRADE_PAIRS, oc_btc_symbol)

r.set(Constants.REDIS_KEY_BUY_QUANTITY_PREFIX + ':oc_btc', 0.0)
r.set(Constants.REDIS_KEY_BUY_PRICE_PREFIX + ':oc_btc', 0.0)
r.set(Constants.REDIS_KEY_SELL_QUANTITY_PREFIX + ':oc_btc', 0.0)
r.set(Constants.REDIS_KEY_SELL_PRICE_PREFIX + ':oc_btc', 0.0)

all_coin_market_url = config['allcoin']['market_url']
all_coin_market = AllCoinMarket(all_coin_market_url)

all_coin_trade_url = config['allcoin']['trade_url']
all_coin_api_key = config['allcoin']['api_key']
all_coin_secret_key = config['allcoin']['secret_key']
all_coin_trade = AllCoinTrade(all_coin_trade_url, all_coin_api_key, all_coin_secret_key)

bit_z_market_url = config['bitz']['market_url']
bit_z_market = BitZMarket(bit_z_market_url)

bit_z_trade_url = config['bitz']['trade_url']
bit_z_api_key = config['bitz']['api_key']
bit_z_secret_key = config['bitz']['secret_key']
bit_z_trade_pwd = config['bitz']['trade_pwd']
bit_z_trade = BitZTrade(bit_z_trade_url, bit_z_api_key, bit_z_secret_key, bit_z_trade_pwd)

while True:
    bit_z_open_orders = bit_z_position.run()
    all_coin_open_orders = all_coin_position.run()

    oc_btc_buy_quantity = bit_z_position.get_buy_quantity(oc_btc_symbol)
    oc_btc_buy_price = bit_z_position.get_buy_quantity(oc_btc_symbol)
    oc_btc_sell_quantity = bit_z_position.get_sell_quantity(oc_btc_symbol)
    oc_btc_sell_price = bit_z_position.get_sell_price(oc_btc_symbol)

    delta = oc_btc_buy_quantity - oc_btc_sell_quantity
    feed = 0

    if oc_btc_symbol in bit_z_open_orders:
        for order in bit_z_open_orders[oc_btc_symbol]:
            if order.is_buy():
                if delta > 0:
                    bit_z_trade.cancel_order(order.get_symbol(), order.get_order_id())
                elif delta < 0:
                    if feed >= -1 * delta:
                        bit_z_trade.cancel_order(order.get_symbol(), order.get_order_id())
                    else:
                        feed += order.get_quantity() - order.get_filled_quantity()
                else:
                    bit_z_trade.cancel_order(order.get_symbol(), order.get_order_id())
            else:
                if delta < 0:
                    bit_z_trade.cancel_order(order.get_symbol(), order.get_order_id())
                elif delta > 0:
                    if feed >= delta:
                        bit_z_trade.cancel_order(order.get_symbol(), order.get_order_id())
                    else:
                        feed += order.get_quantity() - order.get_filled_quantity()
                else:
                    bit_z_trade.cancel_order(order.get_symbol(), order.get_order_id())

    if oc_btc_symbol in all_coin_open_orders:
        for order in all_coin_open_orders[oc_btc_symbol]:
            if order.is_buy():
                if delta > 0:
                    all_coin_trade.cancel_order(order.get_symbol(), order.get_order_id())
                elif delta < 0:
                    if feed >= -1 * delta:
                        all_coin_trade.cancel_order(order.get_symbol(), order.get_order_id())
                    else:
                        feed += order.get_quantity() - order.get_filled_quantity()
                else:
                    all_coin_trade.cancel_order(order.get_symbol(), order.get_order_id())
            else:
                if delta < 0:
                    all_coin_trade.cancel_order(order.get_symbol(), order.get_order_id())
                elif delta > 0:
                    if feed >= delta:
                        all_coin_trade.cancel_order(order.get_symbol(), order.get_order_id())
                    else:
                        feed += order.get_quantity() - order.get_filled_quantity()
                else:
                    all_coin_trade.cancel_order(order.get_symbol(), order.get_order_id())
