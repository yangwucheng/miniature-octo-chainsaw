import configparser
import traceback

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
        'oc': 33178.00,
        'btc': 0.09247294
    },
    position_redis_key=Constants.REDIS_KEY_ALL_COIN_POSITIONS,
    open_order_redis_key_prefix=Constants.REDIS_KEY_ALL_COIN_OPEN_ORDER_IDS_PREFIX,
    cancelled_order_redis_key_prefix=Constants.REDIS_KEY_ALL_COIN_CANCELLED_ORDER_IDS_PREFIX,
    closed_order_redis_key_prefix=Constants.REDIS_KEY_ALL_COIN_CLOSED_ORDER_IDS_PREFIX,
    order_redis_key_prefix=Constants.REDIS_KEY_ALL_COIN_ORDER_PREFIX,
    trade_pair_redis_key=Constants.REDIS_KEY_ALL_COIN_TRADE_PAIRS,
    market_buy_redis_key_prefix=Constants.REDIS_KEY_ALL_COIN_MARKET_BUY_PREFIX,
    market_sell_redis_key_prefix=Constants.REDIS_KEY_ALL_COIN_MARKET_SELL_PREFIX,
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
        'oc': 64706.67,
        'btc': 0.03162183
    },
    position_redis_key=Constants.REDIS_KEY_BIT_Z_POSITIONS,
    open_order_redis_key_prefix=Constants.REDIS_KEY_BIT_Z_OPEN_ORDER_IDS_PREFIX,
    cancelled_order_redis_key_prefix=Constants.REDIS_KEY_BIT_Z_CANCELLED_ORDER_IDS_PREFIX,
    closed_order_redis_key_prefix=Constants.REDIS_KEY_BIT_Z_CLOSED_ORDER_IDS_PREFIX,
    order_redis_key_prefix=Constants.REDIS_KEY_BIT_Z_ORDER_PREFIX,
    trade_pair_redis_key=Constants.REDIS_KEY_BIT_Z_TRADE_PAIRS,
    market_buy_redis_key_prefix=Constants.REDIS_KEY_BIT_Z_MARKET_BUY_PREFIX,
    market_sell_redis_key_prefix=Constants.REDIS_KEY_BIT_Z_MARKET_SELL_PREFIX,
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

r.set(Constants.REDIS_KEY_ALL_COIN_MARKET_BUY_PREFIX + ":oc_btc", 0.0)
r.set(Constants.REDIS_KEY_ALL_COIN_MARKET_SELL_PREFIX + ":oc_btc", 0.0)

r.set(Constants.REDIS_KEY_BIT_Z_MARKET_BUY_PREFIX + ':oc_btc', 0.0)
r.set(Constants.REDIS_KEY_BIT_Z_MARKET_SELL_PREFIX + ':oc_btc', 0.0)

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
    try:
        bit_z_position.run()
        all_coin_position.run()
    except Exception as e:
        traceback.print_exc()
