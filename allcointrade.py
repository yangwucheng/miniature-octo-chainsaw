import configparser

from allcoin.trade import AllCoinTrade

config = configparser.ConfigParser()
config.read(['config.ini', 'secret_config.ini'])
all_coin_trade_url = config['allcoin']['trade_url']
all_coin_api_key = config['allcoin']['api_key']
all_coin_secret_key = config['allcoin']['secret_key']

all_coin_trade = AllCoinTrade(all_coin_trade_url, all_coin_api_key, all_coin_secret_key)

print('### oc btc balance ###')
print(all_coin_trade.get_fund_free(['oc', 'btc']))
print()

print('### buy 100 oc_btc at 0.00000021  ###')
print(all_coin_trade.buy('oc_btc', '0.00000021', '100.00'))
print()

print('### sell 100 oc_btc at 0.00021400  ###')
print(all_coin_trade.sell('oc_btc', '0.00021400', '100.00'))
print()

print('### get oc_btc open orders ###')
print(all_coin_trade.get_open_orders('oc_btc'))
print()

print('### cancel oc_btc order 59770120 ###')
print(all_coin_trade.cancel_order('oc_btc', '59770120'))
print()

print('### cancel all oc_btc orders ###')
print(all_coin_trade.cancel_all_orders('oc_btc'))
print()
