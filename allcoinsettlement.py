from allcoin.settlement import AllCoinSettlement

all_coin_settlement = AllCoinSettlement()

print('### buy oc_btc price 0.00000197 quantity 10000 fee coin is btc ###')
print('%.8f' % all_coin_settlement.calculate_buy_fee('oc_btc', 0.00000197, 10000))
print()

print('### buy oc_btc price 0.00000214 quantity 200000 fee coin is btc ###')
print('%.8f' % all_coin_settlement.calculate_buy_fee('oc_btc', 0.00000214, 200000))
print()

print('### sell oc_btc price 0.00000197 quantity 10000 fee coin is btc ###')
print('%.8f' % all_coin_settlement.calculate_sell_fee('oc_btc', 0.00000197, 10000))
print()

print('### sell oc_btc price 0.00000214 quantity 20000 fee coin is btc ###')
print('%.8f' % all_coin_settlement.calculate_sell_fee('oc_btc', 0.00000214, 20000))
print()

print('### withdraw oc quantity 42721.86 fee coin is oc ###')
print('%.8f' % all_coin_settlement.calculate_withdraw_fee('oc', 42721.86))
print()

print('### withdraw oc quantity 200000.00 fee coin is oc ###')
print('%.8f' % all_coin_settlement.calculate_withdraw_fee('oc', 200000.00))
print()
