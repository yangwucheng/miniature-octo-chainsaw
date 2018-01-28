from bitz.settlement import BitZSettlement

bit_z_settlement = BitZSettlement()

print('### buy oc_btc price 0.00000197 quantity 10000 fee coin is btc ###')
print('%.8f' % bit_z_settlement.calculate_buy_fee('oc_btc', 0.00000197, 10000))
print()

print('### sell oc_btc price 0.00000197 quantity 10000 fee coin is btc ###')
print('%.8f' % bit_z_settlement.calculate_sell_fee('oc_btc', 0.00000197, 10000))
print()

print('### withdraw btc quantity 0.08710000 fee coin is btc ###')
print('%.8f' % bit_z_settlement.calculate_withdraw_fee('oc', 0.08710000))
print()
