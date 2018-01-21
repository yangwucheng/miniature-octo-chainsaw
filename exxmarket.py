"""
exx market data tester
"""
import configparser

from exx.market import ExxMarket

config = configparser.ConfigParser()
config.read('config.ini')
exx_market_url = config['exx']['market_url']
exx_market = ExxMarket(exx_market_url)

print('### spc_qtum depth ###')
print(exx_market.depth('spc_qtum'))
print()

print('### spc_qtum depth ###')
print(exx_market.spc_qtum_depth())
print()

print('### spc_qtum bids ###')
print(exx_market.spc_qtum_bids())
print()

print('### spc_qtum asks ###')
print(exx_market.spc_qtum_asks())
print()
