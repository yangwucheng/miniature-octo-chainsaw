import configparser
import traceback

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


def calculate_pnl_withdraw(buy_price, sell_price, amount, buy_fee, sell_fee, buy_withdraw_fee, sell_withdraw_fee):
    return sell_price * amount - buy_price * amount - buy_fee - sell_fee - sell_withdraw_fee - buy_withdraw_fee


def calculate_pnl(buy_price, sell_price, amount, buy_fee, sell_fee):
    return sell_price * amount - buy_price * amount - buy_fee - sell_fee


def all_coin_buy_bit_z_sell_best_price_volume():
    buy_price = None
    buy_volume = 0.0
    for ask in all_coin_asks:
        if buy_volume >= 1000.0:
            break
        buy_volume += ask[1]
        buy_price = ask[0]

    sell_price = None
    sell_volume = 0.0
    for bid in bit_z_bids:
        if sell_volume >= 1000.0:
            break
        sell_volume += float(bid[1])
        sell_price = float(bid[0])

    return [buy_price, buy_volume, sell_price, sell_volume]


def all_coin_buy_bit_z_sell():
    best_price_volume = all_coin_buy_bit_z_sell_best_price_volume()
    buy_price = best_price_volume[0]
    buy_volume = best_price_volume[1]
    sell_price = best_price_volume[2]
    sell_volume = best_price_volume[3]

    if buy_price is None or sell_price is None:
        return False

    bit_z_oc_position = bit_z_position.get_position('oc')
    all_coin_corresponding_oc_position = all_coin_position.get_position('btc') / buy_price
    if bit_z_oc_position < 1000.0 or all_coin_corresponding_oc_position < 1000.0:
        return False

    amount_float = buy_volume
    if amount_float > sell_volume:
        amount_float = sell_volume
    if amount_float > 10000.00:
        amount_float = 10000.00
    if amount_float > bit_z_oc_position:
        amount_float = bit_z_oc_position
    if amount_float > all_coin_corresponding_oc_position:
        amount_float = all_coin_corresponding_oc_position
    amount_float = float(int(amount_float))
    amount_str = '%.2f' % amount_float

    buy_fee = all_coin_settlement.calculate_buy_fee(symbol, buy_price, amount_float)
    sell_fee = bit_z_settlement.calculate_sell_fee(symbol, sell_price, amount_float)
    pnl = calculate_pnl(buy_price, sell_price, amount_float, buy_fee, sell_fee)
    if pnl > 0 and sell_price / buy_price > 1.03:
        sell_price_str = '%.8f' % sell_price
        bit_z_trade.sell(symbol, sell_price_str, amount_str)
        buy_price_str = '%.8f' % buy_price
        all_coin_trade.buy(symbol, buy_price_str, amount_str)
        print('### all coin buy bit z sell ###')
        print('all coin buy price %s buy amount %s' % (buy_price_str, amount_str))
        print('bit z sell price %s sell amount %s' % (sell_price_str, amount_str))
        print('')
        return True

    return False


def bit_z_buy_all_coin_sell_best_price_volume():
    buy_price = None
    buy_volume = 0.0
    for i in range(0, len(bit_z_asks)):
        if buy_volume >= 1000.0:
            break
        buy_volume += float(bit_z_asks[len(bit_z_asks) - 1 - i][1])
        buy_price = float(bit_z_asks[len(bit_z_asks) - 1 - i][0])

    sell_price = None
    sell_volume = 0.0
    for bid in all_coin_bids:
        if sell_volume >= 1000.0:
            break
        sell_volume += bid[1]
        sell_price = bid[0]

    return [buy_price, buy_volume, sell_price, sell_volume]


def bit_z_buy_all_coin_sell():
    best_price_volume = bit_z_buy_all_coin_sell_best_price_volume()
    buy_price = best_price_volume[0]
    buy_volume = best_price_volume[1]
    sell_price = best_price_volume[2]
    sell_volume = best_price_volume[3]
    if buy_price is None or sell_price is None:
        return False

    all_coin_oc_position = all_coin_position.get_position('oc')
    bit_z_corresponding_oc_position = bit_z_position.get_position('btc') / buy_price
    if all_coin_oc_position < 1000.0 or bit_z_corresponding_oc_position < 1000.0:
        return False

    amount_float = buy_volume
    if amount_float > sell_volume:
        amount_float = sell_volume
    if amount_float > 10000.00:
        amount_float = 10000.00
    if amount_float > all_coin_oc_position:
        amount_float = all_coin_oc_position
    if amount_float > bit_z_corresponding_oc_position:
        amount_float = bit_z_corresponding_oc_position
    amount_float = float(int(amount_float))
    amount_str = '%.2f' % amount_float

    buy_fee = bit_z_settlement.calculate_buy_fee(symbol, buy_price, amount_float)
    sell_fee = all_coin_settlement.calculate_sell_fee(symbol, sell_price, amount_float)
    pnl = calculate_pnl(buy_price, sell_price, amount_float, buy_fee, sell_fee)
    if pnl > 0 and sell_price / buy_price > 1.03:
        buy_price_str = '%.8f' % buy_price
        bit_z_trade.buy(symbol, buy_price_str, amount_str)
        sell_price_str = '%.8f' % sell_price
        all_coin_trade.sell(symbol, sell_price_str, amount_str)
        print('### bit z buy all coin sell ###')
        print('bit z buy price %s buy amount %s' % (buy_price_str, amount_str))
        print('all coin sell price %s sell amount %s' % (sell_price_str, amount_str))
        print('')
        return True

    return False


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(['config.ini', 'secret_config.ini'])

    all_coin_market_url = config['allcoin']['market_url']
    all_coin_market = AllCoinMarket(all_coin_market_url)

    all_coin_trade_url = config['allcoin']['trade_url']
    all_coin_api_key = config['allcoin']['api_key']
    all_coin_secret_key = config['allcoin']['secret_key']
    all_coin_trade = AllCoinTrade(all_coin_trade_url, all_coin_api_key, all_coin_secret_key)

    all_coin_settlement = AllCoinSettlement()

    bit_z_market_url = config['bitz']['market_url']
    bit_z_market = BitZMarket(bit_z_market_url)

    bit_z_trade_url = config['bitz']['trade_url']
    bit_z_api_key = config['bitz']['api_key']
    bit_z_secret_key = config['bitz']['secret_key']
    bit_z_trade_pwd = config['bitz']['trade_pwd']

    bit_z_trade = BitZTrade(bit_z_trade_url, bit_z_api_key, bit_z_secret_key, bit_z_trade_pwd)

    bit_z_settlement = BitZSettlement()

    # all coin position manager
    all_coin_position = AllCoinPosition(
        init_positions=None,
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

    # bit z position manager
    bit_z_position = BitZPosition(
        init_positions=None,
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
    SettlementFactory.settlements = {
        Constants.EXCHANGE_NAME_ALL_COIN: all_coin_settlement,
        Constants.EXCHANGE_NAME_BIT_Z: bit_z_settlement
    }
    SettlementFactory.default_settlement = bit_z_settlement

    symbol = 'oc_btc'

    while True:
        try:
            all_coin_depth = all_coin_market.depth(symbol)
            all_coin_asks = all_coin_depth['asks']
            all_coin_bids = all_coin_depth['bids']

            bit_z_depth = bit_z_market.depth(symbol)
            bit_z_bids = bit_z_depth['data']['bids']
            bit_z_asks = bit_z_depth['data']['asks']

            if not all_coin_buy_bit_z_sell():
                bit_z_buy_all_coin_sell()
        except Exception as e:
            traceback.print_exc()
