import math
import pandas as pd


class Portfolio:
    """Processes signals from the Strategy object"""

    def __init__(self, data_handler, events, capital=1000000):
        self.data_handler = data_handler
        self.events = events
        self.initial_capital = capital
        self.current_position = {"cash": self.initial_capital}
        self.all_positions = {}
        self.current_balance = {
            "cash": self.initial_capital,
            "total": self.initial_capital
        }
        self.all_balances = {}

    def update_signal(self, signal):
        """Processes signal event and updates the current position"""
        date = self.data_handler.current_date
        if date not in self.all_positions:
            self.all_positions[date] = self.current_position.copy()
        self.current_position = self.all_positions[date]

        (price, direction) = self._get_price(signal)
        quantity = self._get_allocation(signal.strength, price)
        self.current_position[signal.symbol] = self.current_position.get(
            signal.symbol, 0) + direction * quantity
        self.current_position["cash"] -= direction * price * quantity

    def update_timeindex(self, event):
        """Calculates new balance for the current timeindex.
        Appends current position to all_positions list."""
        date = self.data_handler.current_date
        self.all_balances[date] = self.current_balance.copy()
        self.current_balance = self.all_balances[date]
        self.current_balance["total"] = self.current_position["cash"]

        for symbol, qty in self.current_position.items():
            if symbol == "cash":
                self.current_balance["cash"] = qty
                continue

            current_bar = self.data_handler.get_latest_bars(symbol)
            if qty < 0:
                price = current_bar["ask"].values[0]
            else:
                price = current_bar["bid"].values[0]
            market_value = qty * price
            self.current_balance[symbol] = market_value
            self.current_balance["total"] += market_value

        self.all_positions[date] = self.current_position
        self.all_balances[date] = self.current_balance

    def _get_price(self, signal):
        """Returns price and direction for given symbol.
        Ask price if signal.type == BUY, bid price if signal.type == SELL.
        Also returns 1 or -1 for types BUY, SELL respectively"""
        current_bar = self.data_handler.get_latest_bars(signal.symbol)
        if signal.direction == "BUY":
            direction = 1
            price = current_bar["ask"].values[0]
        else:
            direction = -1
            price = current_bar["bid"].values[0]
        return (price, direction)

    def _get_allocation(self, strength, price):
        """Calculates allocation using Kelly's criterion"""
        (win_percent, win_loss_ratio) = strength
        kelly = max(0, win_percent - (1 - win_percent) / win_loss_ratio)
        total_allocation = self.current_position["cash"] * kelly
        return math.floor(total_allocation / price)

    def create_equity_curve_dataframe(self):
        """
        Creates a pandas DataFrame from the all_balances
        list of dictionaries.
        """
        curve = pd.DataFrame(self.all_balances)
        curve = curve.transpose()
        curve["returns"] = curve["total"].pct_change()
        curve["equity_curve"] = (1.0 + curve["returns"]).cumprod()
        return curve
