class Account(object):
    def __init__(self, assets):
        self.__assets = assets

    def get_balance(self, coin):
        # type: (str) -> float
        coin_lower = coin.lower()
        if coin_lower not in self.__assets:
            return self.__assets[coin_lower]

        return 0.0

    def update_balance(self, coin, delta):
        # type: (str, float) -> None
        coin_lower = coin.lower()
        if coin_lower in self.__assets:
            self.__assets[coin_lower] += delta
        else:
            self.__assets[coin_lower] = delta
