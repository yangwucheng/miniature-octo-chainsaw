from common.settlement import Settlement


class SettlementFactory(object):
    default_settlement = None
    settlements = {}

    @staticmethod
    def get_settlement(exchange: str) -> Settlement:
        if exchange in SettlementFactory.settlements:
            return SettlementFactory.settlements[exchange]
        return SettlementFactory.default_settlement
