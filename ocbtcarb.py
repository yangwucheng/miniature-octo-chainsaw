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
    SettlementFactory.settlements = {
        Constants.EXCHANGE_NAME_ALL_COIN: all_coin_settlement,
        Constants.EXCHANGE_NAME_BIT_Z: bit_z_settlement
    }
    SettlementFactory.default_settlement = bit_z_settlement

    symbol = 'oc_btc'
    min_amount = all_coin_settlement.get_min_buy_quantity(symbol)
    if min_amount <= bit_z_settlement.get_min_sell_quantity(symbol):
        min_amount = bit_z_settlement.get_min_sell_quantity(symbol)

    while True:
        try:
            bit_z_oc_position = bit_z_position.get_position('oc')
            if bit_z_oc_position < min_amount:
                break

            all_coin_asks = all_coin_market.oc_btc_asks()
            all_coin_ask_1_price_float = all_coin_asks[0][0]
            all_coin_ask_1_volume_float = all_coin_asks[0][1]

            bit_z_bids = bit_z_market.oc_btc_bids()
            bit_z_bid_1_price_str = bit_z_bids[0][0]
            bit_z_bid_1_volume_str = bit_z_bids[0][1]
            bit_z_bid_1_price_float = float(bit_z_bid_1_price_str)
            bit_z_bid_1_volume_float = float(bit_z_bid_1_volume_str)

            sell_price_str = bit_z_bid_1_price_str
            sell_price_float = float(sell_price_str)
            buy_price_float = all_coin_ask_1_price_float
            buy_price_str = '%.8f' % buy_price_float

            all_coin_corresponding_oc_position = all_coin_position.get_position('btc') / buy_price_float
            if all_coin_corresponding_oc_position < min_amount:
                break

            amount_float = bit_z_bid_1_volume_float
            if amount_float > all_coin_ask_1_volume_float:
                amount_float = all_coin_ask_1_volume_float
            if amount_float > 10000.00:
                amount_float = 10000.00
            if amount_float > bit_z_oc_position:
                amount_float = bit_z_oc_position
            if amount_float > all_coin_corresponding_oc_position:
                amount_float = all_coin_corresponding_oc_position
            if amount_float < min_amount:
                amount_float = min_amount
            amount_str = '%.2f' % amount_float

            if all_coin_settlement.is_valid_buy_order(symbol, buy_price_float, amount_float) and \
                    bit_z_settlement.is_valid_sell_order(symbol, sell_price_float, amount_float):
                buy_fee = all_coin_settlement.calculate_buy_fee(symbol, buy_price_float, amount_float)
                sell_fee = bit_z_settlement.calculate_sell_fee(symbol, sell_price_float, amount_float)
                # buy_withdraw_fee = all_coin_settlement.calculate_withdraw_fee('oc', amount_float) * buy_price_float
                # sell_withdraw_fee = bit_z_settlement.calculate_withdraw_fee('btc', amount_float * sell_price_float)
                # pnl = calculate_pnl(buy_price_float, sell_price_float, amount_float, buy_fee, sell_fee, buy_withdraw_fee, sell_withdraw_fee)
                pnl = calculate_pnl(buy_price_float, sell_price_float, amount_float, buy_fee, sell_fee)
                if pnl > 0 and sell_price_float / buy_price_float > 1.10:
                    all_coin_trade.buy(symbol, buy_price_str, amount_str)
                    bit_z_trade.sell(symbol, sell_price_str, amount_str)

                    print('buy price %s buy amount %s' % (buy_price_str, amount_str))
                    print('sell price %s sell amount %s' % (sell_price_str, amount_str))

                    # print('sell price, buy price, amount, sell fee, buy fee, pnl')
                    # print(
                    #     '%(sell_price)s, %(buy_price)s, %(amount)s, %(sell_fee).8f, %(buy_fee).8f, '
                    #     '%(pnl).8f' % {
                    #         'sell_price': sell_price_str,
                    #         'buy_price': buy_price_str,
                    #         'amount': amount_str,
                    #         'sell_fee': sell_fee,
                    #         'buy_fee': buy_fee,
                    #         'pnl': pnl
                    #     })

                    # print('sell price, buy price, amount, sell fee, buy fee, sell withdraw fee, buy withdraw fee, pnl')
                    # print(
                    #     '%(sell_price)s, %(buy_price).8f, %(amount)s, %(sell_fee).8f, %(buy_fee).8f, '
                    #     '%(sell_withdraw_fee).8f, %(buy_withdraw_fee).8f, %(pnl).8f' % {
                    #         'sell_price': sell_price_str,
                    #         'buy_price': buy_price_float,
                    #         'amount': amount_str,
                    #         'sell_fee': sell_fee,
                    #         'buy_fee': buy_fee,
                    #         'sell_withdraw_fee': sell_withdraw_fee,
                    #         'buy_withdraw_fee': buy_withdraw_fee,
                    #         'pnl': pnl
                    #     })
        except Exception as e:
            print(e)
