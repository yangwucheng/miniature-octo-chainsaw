import configparser

from allcoin.market import AllCoinMarket
from allcoin.trade import AllCoinTrade
from exx.market import ExxMarket
from exx.trade import ExxTrade


def calculate_pnl(buy_price, sell_price, amount, buy_fee, sell_fee, buy_withdraw_fee, sell_withdraw_fee):
    return sell_price * amount - buy_price * amount - buy_fee - sell_fee - sell_withdraw_fee - buy_withdraw_fee


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(['config.ini', 'secret_config.ini'])

    all_coin_market_url = config['allcoin']['market_url']
    all_coin_market = AllCoinMarket(all_coin_market_url)

    all_coin_trade_url = config['allcoin']['trade_url']
    all_coin_api_key = config['allcoin']['api_key']
    all_coin_secret_key = config['allcoin']['secret_key']
    all_coin_trade = AllCoinTrade(all_coin_trade_url, all_coin_api_key, all_coin_secret_key)

    exx_market_url = config['exx']['market_url']
    exx_market = ExxMarket(exx_market_url)

    exx_trade_url = config['exx']['trade_url']
    exx_access_key = config['exx']['access_key']
    exx_secret_key = config['exx']['secret_key']
    exx_trade = ExxTrade(exx_trade_url, exx_access_key, exx_secret_key)

    exx_asks = exx_market.spc_qtum_asks()
    exx_ask_1_price_str = exx_asks[-1][0]
    exx_ask_1_volume_str = exx_asks[-1][1]
    exx_ask_1_volume_float = float(exx_ask_1_volume_str)

    all_coin_bids = all_coin_market.spc_qtum_bids()
    all_coin_bid_1_price_float = all_coin_bids[0][0]
    all_coin_bid_1_volume_float = all_coin_bids[0][1]

    sell_price_float = all_coin_bid_1_price_float
    sell_price_str = '%.8f' % sell_price_float
    buy_price_str = exx_ask_1_price_str
    buy_price_float = float(buy_price_str)

    amount_float = all_coin_bid_1_volume_float
    if amount_float > exx_ask_1_volume_float:
        amount_float = exx_ask_1_volume_float

    amount_str = '%.2f' % amount_float

    symbol = 'spc_qtum'
    if ExxTrade.is_valid_order(symbol, amount_float, buy_price_float) and AllCoinTrade.is_valid_order(symbol,
                                                                                                      amount_float,
                                                                                                      sell_price_float):
        buy_fee = ExxTrade.buy_fee(symbol, amount_float, buy_price_float)
        sell_fee = AllCoinTrade.sell_fee(symbol, amount_float, sell_price_float)
        buy_withdraw_fee = ExxTrade.withdraw_fee('spc', amount_float) * buy_price_float
        sell_withdraw_fee = AllCoinTrade.withdraw_fee('qtum', amount_float * sell_price_float)
        pnl = calculate_pnl(buy_price_float, sell_price_float, amount_float, buy_fee, sell_fee, buy_withdraw_fee,
                            sell_withdraw_fee)
        if pnl > 0:
            print('ARB')

        print('sell price, buy price, amount, sell fee, buy fee, sell withdraw fee, buy withdraw fee, pnl')
        print(
            '%(sell_price)s, %(buy_price)s, %(amount)s, %(sell_fee).8f, %(buy_fee).8f, %(sell_withdraw_fee).8f, '
            '%(buy_withdraw_fee).8f, %(pnl).8f' % {
                'sell_price': sell_price_str,
                'buy_price': buy_price_str,
                'amount': amount_str,
                'sell_fee': sell_fee,
                'buy_fee': buy_fee,
                'sell_withdraw_fee': sell_withdraw_fee,
                'buy_withdraw_fee': buy_withdraw_fee,
                'pnl': pnl
            })
