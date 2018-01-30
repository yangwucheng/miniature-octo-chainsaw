import configparser
import tkinter.messagebox

from allcoin.market import AllCoinMarket
from allcoin.trade import AllCoinTrade
from bitz.market import BitZMarket

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(['config.ini'])

    all_coin_market_url = config['allcoin']['market_url']
    all_coin_market = AllCoinMarket(all_coin_market_url)

    bit_z_market_url = config['bitz']['market_url']
    bit_z_market = BitZMarket(bit_z_market_url)

    while True:
        try:
            all_coin_asks = all_coin_market.oc_btc_asks()
            all_coin_ask_1_price_float = all_coin_asks[0][0]
            all_coin_ask_1_volume_float = all_coin_asks[0][1]

            bit_z_bids = bit_z_market.oc_btc_bids()
            bit_z_bid_1_price_str = bit_z_bids[0][0]
            bit_z_bid_1_volume_str = bit_z_bids[0][1]

            sell_price_str = bit_z_bid_1_price_str
            sell_price_float = float(sell_price_str)

            buy_price_float = all_coin_ask_1_price_float
            buy_price_str = '%.8f' % buy_price_float

            bit_z_bid_1_volume_float = float(bit_z_bid_1_volume_str)
            amount_float = all_coin_ask_1_volume_float
            if amount_float > bit_z_bid_1_volume_float:
                amount_float = bit_z_bid_1_volume_float
            amount_str = '%.2f' % amount_float

            if sell_price_float / buy_price_float > 1.08:
                print(buy_price_str, amount_str)
                print(sell_price_str, amount_str)
                tkinter.messagebox.showinfo("价差达到8%以上",
                                            'buy price %s buy volume %s \nsell price %s sell volume %s' %
                                            (buy_price_str, amount_str, sell_price_str, amount_str)
                                            )
        except Exception as e:
            print(e)
