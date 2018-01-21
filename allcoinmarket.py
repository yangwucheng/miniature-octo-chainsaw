from allcoin.market import AllCoinMarket
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
all_coin_market_url = config['allcoin']['market_url']
all_coin_market = AllCoinMarket(all_coin_market_url)

print('### spc_qtum depth ###')
print(all_coin_market.depth('spc_qtum'))
print()

print('### spc_qtum bids ###')
print(all_coin_market.spc_qtum_bids())
print()
