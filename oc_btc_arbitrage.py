import configparser
from allcoin.market import AllCoinMarket
from allcoin.trade import AllCoinTrade
from bitz.market import BitZMarket
from bitz.trade import BitZTrade


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

    bit_z_market_url = config['bitz']['market_url']
    bit_z_market = BitZMarket(bit_z_market_url)

    all_coin_asks = all_coin_market.oc_btc_asks()
    all_coin_ask_1_price = float(all_coin_asks[0][0])
    all_coin_ask_1_volume = float(all_coin_asks[0][1])

    bit_z_bids = bit_z_market.oc_btc_bids()
    bit_z_bid_1_price = float(bit_z_bids[0][0])
    bit_z_bid_1_volume = float(bit_z_bids[0][1])

    sell_price = bit_z_bid_1_price
    buy_price = all_coin_ask_1_price
    amount = bit_z_bid_1_volume
    if amount > all_coin_ask_1_volume:
        amount = all_coin_ask_1_volume

    symbol = 'oc_btc'
    if AllCoinTrade.is_valid_order(symbol, amount, buy_price) and BitZTrade.is_valid_order(symbol, amount, sell_price):
        buy_fee = AllCoinTrade.buy_fee(symbol, amount, buy_price)
        sell_fee = BitZTrade.sell_fee(symbol, amount, sell_price)
        buy_withdraw_fee = AllCoinTrade.withdraw_fee('oc', amount) * buy_price
        sell_withdraw_fee = BitZTrade.withdraw_fee('btc', amount * sell_price)
        pnl = calculate_pnl(buy_price, sell_price, amount, buy_fee, sell_fee, buy_withdraw_fee, sell_withdraw_fee)
        if pnl > 0:
            print('ARB')

        print('sell price, buy price, amount, sell fee, buy fee, sell withdraw fee, buy withdraw fee, pnl')
        print(
            '%(sell_price)s, %(buy_price)s, %(amount)s, %(sell_fee)s, %(buy_fee)s, %(sell_withdraw_fee)s, '
            '%(buy_withdraw_fee)s, %(pnl)s' % {
                'sell_price': sell_price,
                'buy_price': buy_price,
                'amount': amount,
                'sell_fee': sell_fee,
                'buy_fee': buy_fee,
                'sell_withdraw_fee': sell_withdraw_fee,
                'buy_withdraw_fee': buy_withdraw_fee,
                'pnl': pnl
            })
