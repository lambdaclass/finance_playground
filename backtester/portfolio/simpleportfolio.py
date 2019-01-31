import logging
import math
from .portfolio import Portfolio

logging.basicConfig(level=logging.DEBUG)


class SimplePortfolio(Portfolio):
    """Allocates all capital to the first signal processed.
    Takes only long positions.
    Only sells if it has the given symbol in portfolio.
    """

    def __init__(self, *args):
        super().__init__(*args)

    def _get_allocation(self, signal, price):
        """Allocates all capital to the given signal"""
        if signal.direction == "SELL":
            amount, open_price = self.current_position.get(
                signal.symbol, (0, 0))
            if amount > 0:
                logging.debug("%s - SELL amount: %d",
                              self.data_handler.current_date, amount)
            return amount
        else:
            amount = math.floor(self.current_position["Cash"] / price)
            if amount > 0:
                logging.debug("%s - BUY amount: %d",
                              self.data_handler.current_date, amount)
            return amount
