"""
exx trade tester
"""

import configparser

from exx.trade import ExxTrade

config = configparser.ConfigParser()
config.read(['config.ini', 'secret_config.ini'])
exx_trade_url = config['exx']['trade_url']
exx_access_key = config['exx']['access_key']
exx_secret_key = config['exx']['secret_key']
exx_trade = ExxTrade(exx_trade_url, exx_access_key, exx_secret_key)

print('### account balance ###')
print(exx_trade.get_balance())
print()

print('### spc qtum balance ###')
print(exx_trade.get_spc_qtum_balance())
print()

print('### buy spc_qtum 0.000001 1 ###')
print(exx_trade.buy('spc_qtum', '0.000001', '1'))
print()

print('### sell spc_qtum 1.0 1 ###')
print(exx_trade.sell('spc_qtum', '1.0', '1'))
print()

print('### get spc_qtum buy open orders ###')
print(exx_trade.get_open_orders('spc_qtum', 'buy'))
print()

print('### get spc_qtum sell open orders ###')
print(exx_trade.get_open_orders('spc_qtum', 'sell'))
print()

print('### cancel spc_qtum order 50540 ###')
print(exx_trade.cancel_order('spc_qtum', '50540'))
print()

print('### cancel all spc_qtum orders ###')
print(exx_trade.cancel_all_orders('spc_qtum'))
print()
