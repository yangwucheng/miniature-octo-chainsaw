import configparser

from bitz.trade import BitZTrade

config = configparser.ConfigParser()
config.read(['config.ini', 'secret_config.ini'])
bit_z_trade_url = config['bitz']['trade_url']
bit_z_api_key = config['bitz']['api_key']
bit_z_secret_key = config['bitz']['secret_key']
bit_z_trade_pwd = config['bitz']['trade_pwd']

bit_z_trade = BitZTrade(bit_z_trade_url, bit_z_api_key, bit_z_secret_key, bit_z_trade_pwd)

print('### buy 100.00 oc_btc at 0.00000001 ###')
print(bit_z_trade.buy('oc_btc', '0.00000001', '100.00'))
print()

print('### sell 100.00 oc_btc at 1.0 ###')
print(bit_z_trade.sell('oc_btc', '1.0', '100.00'))
print()

print('### get oc_btc open orders ###')
print(bit_z_trade.get_open_orders('oc_btc'))
print()

# print('### cancel spc_qtum order 58667713 ###')
# print(bit_z_trade.cancel_order('scp_qtum', '58667713'))
# print()
#
print('### cancel all oc_btc orders ###')
print(bit_z_trade.cancel_all_orders('oc_btc'))
print()
