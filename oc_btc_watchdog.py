import configparser
import tkinter.messagebox

from allcoin.market import AllCoinMarket
from allcoin.trade import AllCoinTrade
from bitz.market import BitZMarket

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
    remain_amount = 40000.0

    while True:
        try:
            if remain_amount <= 1.0:
                tkinter.messagebox.showinfo("Arbitrage Finished", 'Transfer Coin')
                break

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
            if amount_float > 10000:
                amount_float = 10000
            if amount_float > remain_amount:
                amount_float = remain_amount
            amount_str = '%.2f' % amount_float

            symbol = 'oc_btc'
            if sell_price_float / buy_price_float > 0.8:
                # all_coin_trade.buy(symbol, buy_price_str, amount_str)
                remain_amount -= amount_float
                print(buy_price_str, amount_str)
                print(sell_price_str, amount_str)
                tkinter.messagebox.showinfo("价差达到10%以上",
                                            'buy price %s buy volume %s \nsell price %s sell volume %s' %
                                            (buy_price_str, amount_str, sell_price_str, amount_str)
                                            )
        except Exception as e:
            print(e)
