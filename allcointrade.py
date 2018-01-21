import configparser

from allcoin.trade import AllCoinTrade

config = configparser.ConfigParser()
config.read(['config.ini', 'secret_config.ini'])
all_coin_trade_url = config['allcoin']['trade_url']
all_coin_api_key = config['allcoin']['api_key']
all_coin_secret_key = config['allcoin']['secret_key']

all_coin_trade = AllCoinTrade(all_coin_trade_url, all_coin_api_key, all_coin_secret_key)

print('### spc qtum balance ###')
print(all_coin_trade.get_fund_free(['spc', 'qtum']))
print()

print('### buy 2 spc_qtum at 0.00001 ###')
print(all_coin_trade.buy('spc_qtum', 0.00001, 2.0))
print()

print('### sell 2 spc_qtum at 0.8 ###')
print(all_coin_trade.sell('spc_qtum', 0.8, 2.0))
print()

print('### get spc_qtum open orders ###')
print(all_coin_trade.get_open_orders('spc_qtum'))
print()

# print('### cancel spc_qtum order 58667713 ###')
# print(all_coin_trade.cancel_order('scp_qtum', '58667713'))
# print()

print('### cancel all spc_qtum orders ###')
print(all_coin_trade.cancel_all_orders('spc_qtum'))
print()
