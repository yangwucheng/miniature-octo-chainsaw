import configparser

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


def all_coin_buy_bit_z_sell_price_amount(all_coin_asks, bit_z_bids):
    all_coin_buy_quantity = 0.0
    all_coin_buy_turnover = 0.0
    all_coin_buy_price = None
    for i in range(0, len(all_coin_asks)):
        if all_coin_buy_quantity > 100:
            break
        all_coin_buy_price = all_coin_asks[i][0]
        all_coin_buy_turnover += all_coin_buy_price * all_coin_asks[i][1]
        all_coin_buy_quantity += all_coin_asks[i][1]

    bit_z_sell_quantity = 0.0
    bit_z_sell_turnover = 0.0
    bit_z_sell_price = None
    for i in range(0, len(bit_z_bids)):
        if bit_z_sell_quantity > 100:
            break
        bit_z_sell_price = float(bit_z_bids[i][0])
        bit_z_sell_turnover += bit_z_sell_price * float(bit_z_bids[i][1])
        bit_z_sell_quantity += float(bit_z_bids[i][1])

    return [all_coin_buy_price, all_coin_buy_quantity, all_coin_buy_turnover,
            bit_z_sell_price, bit_z_sell_quantity, bit_z_sell_turnover]


def all_coin_buy_bit_z_sell(all_coin_asks, bit_z_bids):
    result = all_coin_buy_bit_z_sell_price_amount(all_coin_asks, bit_z_bids)

    buy_price_float = result[0]
    buy_price_str = '%.8f' % buy_price_float
    buy_quantity_float = result[1]
    buy_turnover_float = result[2]

    sell_price_float = result[3]
    sell_price_str = '%.8f' % sell_price_float
    sell_quantity_float = result[4]
    sell_turnover_float = result[5]

    bit_z_oc_position = bit_z_position.get_position('oc')
    all_coin_corresponding_oc_position = all_coin_position.get_position('btc') / buy_price_float
    if bit_z_oc_position < min_amount or all_coin_corresponding_oc_position < min_amount:
        return False

    amount_float = buy_quantity_float
    if amount_float > sell_quantity_float:
        amount_float = sell_quantity_float
    if amount_float > 10000.00:
        amount_float = 10000.00
    if amount_float > bit_z_oc_position:
        amount_float = bit_z_oc_position
    if amount_float > all_coin_corresponding_oc_position:
        amount_float = all_coin_corresponding_oc_position
    if amount_float < min_amount:
        amount_float = min_amount
    amount_float = float(int(amount_float))
    amount_str = '%.2f' % amount_float

    if all_coin_settlement.is_valid_buy_order(symbol, buy_price_float, amount_float) and \
            bit_z_settlement.is_valid_sell_order(symbol, sell_price_float, amount_float):
        buy_fee = all_coin_settlement.calculate_buy_fee(symbol, buy_price_float, amount_float)
        sell_fee = bit_z_settlement.calculate_sell_fee(symbol, sell_price_float, amount_float)
        pnl = calculate_pnl(buy_price_float, sell_price_float, amount_float, buy_fee, sell_fee)
        if pnl > 0 and sell_price_float / buy_price_float > 1.10:
            all_coin_trade.buy(symbol, buy_price_str, amount_str)
            bit_z_trade.sell(symbol, sell_price_str, amount_str)

            print('buy price %s buy amount %s' % (buy_price_str, amount_str))
            print('sell price %s sell amount %s' % (sell_price_str, amount_str))
            return True

    return False


def bit_z_buy_all_coin_sell_price_amount(bit_z_asks, all_coin_bids):
    bit_z_buy_quantity = 0.0
    bit_z_buy_turnover = 0.0
    bit_z_buy_price = None
    bit_z_asks_len = len(bit_z_asks)
    for i in range(0, bit_z_asks_len):
        if bit_z_buy_quantity > 100:
            break
        bit_z_buy_price = float(bit_z_asks[bit_z_asks_len - 1 - i][0])
        bit_z_buy_turnover += bit_z_buy_price * float(bit_z_asks[bit_z_asks_len - 1 - i][1])
        bit_z_buy_quantity += float(bit_z_asks[bit_z_asks_len - 1 - i][1])

    all_coin_sell_quantity = 0.0
    all_coin_sell_turnover = 0.0
    all_coin_sell_price = None
    for i in range(0, len(all_coin_bids)):
        if all_coin_sell_quantity > 100:
            break
        all_coin_sell_price = all_coin_bids[i][0]
        all_coin_sell_turnover += all_coin_sell_price * all_coin_bids[i][1]
        all_coin_sell_quantity += all_coin_bids[i][1]

    return [bit_z_buy_price, bit_z_buy_quantity, bit_z_buy_turnover,
            all_coin_sell_price, all_coin_sell_quantity, all_coin_sell_turnover]


def bit_z_buy_all_coin_sell(bit_z_asks, all_coin_bids):
    result = bit_z_buy_all_coin_sell_price_amount(bit_z_asks, all_coin_bids)

    buy_price_float = result[0]
    buy_price_str = '%.8f' % buy_price_float
    buy_quantity_float = result[1]
    buy_turnover_float = result[2]

    sell_price_float = result[3]
    sell_price_str = '%.8f' % sell_price_float
    sell_quantity_float = result[4]
    sell_turnover_float = result[5]

    all_coin_oc_position = all_coin_position.get_position('oc')
    bit_z_corresponding_oc_position = bit_z_position.get_position('btc') / buy_price_float
    if all_coin_oc_position < min_amount or bit_z_corresponding_oc_position < min_amount:
        return False

    amount_float = buy_quantity_float
    if amount_float > sell_quantity_float:
        amount_float = sell_quantity_float
    if amount_float > 10000.00:
        amount_float = 10000.00
    if amount_float > all_coin_oc_position:
        amount_float = all_coin_oc_position
    if amount_float > bit_z_corresponding_oc_position:
        amount_float = bit_z_corresponding_oc_position
    if amount_float < min_amount:
        amount_float = min_amount
    amount_float = float(int(amount_float))
    amount_str = '%.2f' % amount_float

    if bit_z_settlement.is_valid_buy_order(symbol, buy_price_float, amount_float) and \
            all_coin_settlement.is_valid_sell_order(symbol, sell_price_float, amount_float):
        buy_fee = bit_z_settlement.calculate_buy_fee(symbol, buy_price_float, amount_float)
        sell_fee = all_coin_settlement.calculate_sell_fee(symbol, sell_price_float, amount_float)
        pnl = calculate_pnl(buy_price_float, sell_price_float, amount_float, buy_fee, sell_fee)
        if pnl > 0 and sell_price_float / buy_price_float > 1.01:
            bit_z_trade.buy(symbol, buy_price_str, amount_str)
            all_coin_trade.sell(symbol, sell_price_str, amount_str)

            print('buy price %s buy amount %s' % (buy_price_str, amount_str))
            print('sell price %s sell amount %s' % (sell_price_str, amount_str))
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
    min_amount = all_coin_settlement.get_min_buy_quantity(symbol)
    if min_amount <= bit_z_settlement.get_min_sell_quantity(symbol):
        min_amount = bit_z_settlement.get_min_sell_quantity(symbol)

    try:
        # all_coin_trade.buy(symbol, '0.00000150', '1000')
        # bit_z_trade.sell(symbol, '0.00000159', '1000')
        print(all_coin_trade.get_order_info(symbol, '60539373'))
        pass

    except Exception as e:
        print(e)
