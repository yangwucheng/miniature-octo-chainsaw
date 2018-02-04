import configparser
import logging
import tkinter.messagebox

from allcoin.market import AllCoinMarket
from bitz.market import BitZMarket

logger = logging.getLogger('watchdog')


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

    if sell_price / buy_price > 1.02:
        logger.info('all coin buy price %.8f quantity %.8f ', buy_price, buy_volume)
        logger.info('bit z sell price %.8f quantity %.8f ', sell_price, sell_volume)
        tkinter.messagebox.showinfo("价差达到2%以上",
                                    'all coin buy price %.8f quantity %.8f \n bit z sell price %.8f quantity %.8f' %
                                    (buy_price, buy_volume, sell_price, sell_volume)
                                    )
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

    if sell_price / buy_price > 1.02:
        logger.info('bit z buy price %.8f quantity %.8f ', buy_price, buy_volume)
        logger.info('all coin sell price %.8f quantity %.8f ', sell_price, sell_volume)
        tkinter.messagebox.showinfo("价差达到2%以上",
                                    'bit z buy price %.8f quantity %.8f \n all coin sell price %.8f quantity %.8f' %
                                    (buy_price, buy_volume, sell_price, sell_volume)
                                    )
        return True

    return False


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(['config.ini'])

    all_coin_market_url = config['allcoin']['market_url']
    all_coin_market = AllCoinMarket(all_coin_market_url)

    bit_z_market_url = config['bitz']['market_url']
    bit_z_market = BitZMarket(bit_z_market_url)

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
            print(e)
