import configparser

from bitz.market import BitZMarket

config = configparser.ConfigParser()
config.read('config.ini')
bit_z_market_url = config['bitz']['market_url']
bit_z_market = BitZMarket(bit_z_market_url)

print('### oc_btc k line ###')
print(bit_z_market.oc_btc_1m_k_line())
print()

print('### oc_btc depth ###')
print(bit_z_market.depth('oc_btc'))
print()

print('### oc_btc bids ###')
print(bit_z_market.oc_btc_bids())
print()
