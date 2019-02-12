import math
from .portfolio import Portfolio


class WeightedPortfolio(Portfolio):
    """Allocates portfolio according to given weights.
    Defaults to 97% SPX, 3% SPX puts 60-70 dte.
    Sells puts with 30 dte.
    """

    def __init__(self,
                 spx_handler,
                 option_handler,
                 events,
                 weights={
                     "SIGNAL_STOCK": 0.97,
                     "SIGNAL_OPTIONS": 0.03
                 },
                 capital=1000000):
        self.spx_handler = spx_handler
        self.option_handler = option_handler
        self.events = events
        self.weights = weights
        self.initial_capital = capital
        self.current_position = {"Cash": self.initial_capital}
        self.all_positions = {}
        self.current_balance = {"Cash": self.initial_capital}
        self.all_balances = {}

    def update_signal(self, signal):
        """Processes signal event and updates the current position"""
        date = self.spx_handler.current_date
        if date not in self.all_positions:
            self.all_positions[date] = self.current_position.copy()
        self.current_position = self.all_positions[date]

        if signal.type == "SIGNAL_STOCK":
            self._process_stock_signal(signal)
        else:
            self._process_options_signal(signal)

    def update_timeindex(self):
        """Calculates new balance for the current date.
        Adds `current_position` to the `all_positions` dictionary."""
        date = self.spx_handler.current_date

        self.all_balances[date] = self.current_balance.copy()
        self.current_balance["Total Exposure"] = 0

        for item_name, values in self.current_position.items():
            if item_name == "Cash":
                self.current_balance["Cash"] = values
                continue

            (amount, open_price) = values
            if item_name == "SPX":
                current_bar = self.spx_handler.get_latest_bars(
                    item_name).iloc[0]
            else:
                all_options = self.option_handler.get_latest_bars("SPX")
                current_bar = all_options[all_options["optionroot"] ==
                                          item_name]
                if current_bar.empty:
                    continue
                else:
                    current_bar = current_bar.iloc[0]

            if amount < 0:
                price = current_bar["ask"]
            else:
                price = current_bar["bid"]

            market_value = amount * price
            self.current_balance[item_name + " Amount"] = amount
            self.current_balance[item_name + " Open"] = open_price
            self.current_balance[item_name + " Exposure"] = market_value
            self.current_balance["Total Exposure"] += market_value

        self.all_positions[date] = self.current_position
        self.all_balances[date] = self.current_balance.copy()

    def _process_stock_signal(self, signal):
        item_name = signal.symbol
        price, direction = self._get_price(signal)

        current_amount, current_open_price = self.current_position.get(
            item_name, (0, 0))
        if signal.direction == "SELL":
            qty = current_amount
        else:
            qty = self._get_allocation(signal, price)

        self.current_position[item_name] = (current_amount + direction * qty,
                                            price)
        self.current_position["Cash"] -= direction * price * qty

    def _process_options_signal(self, signal):
        item_name = signal.optionroot

        price, direction = self._get_price(signal)
        if signal.direction == "SELL":
            qty = self.current_position[item_name][0]
            self.current_position[item_name] = (0, 0)
        else:
            qty = self._get_allocation(signal, price)
            self.current_position[item_name] = (qty, direction * qty * price)

        self.current_position["Cash"] -= direction * price * qty

    def _get_price(self, signal):
        """Returns price and direction indicator for given symbol.
        Ask price if `signal.direction == BUY`,
        bid price if `signal.direction == SELL`.
        Also returns 1 or -1 for directions BUY, SELL respectively"""
        if signal.type == "SIGNAL_STOCK":
            current_bar = self.spx_handler.get_latest_bars(signal.symbol)
        else:
            all_options = self.option_handler.get_latest_bars(signal.symbol)
            current_bar = all_options[all_options["optionroot"] == signal.
                                      optionroot]
            if current_bar.empty:
                return (0, 0)

        current_bar = current_bar.iloc[0]

        if signal.direction == "BUY":
            direction = 1
            price = current_bar["ask"]
        else:
            direction = -1
            price = current_bar["bid"]

        if signal.type == "SIGNAL_OPTIONS":
            price = price * 100
        return (price, direction)

    def _get_allocation(self, signal, price):
        """Calculates allocation for given signal"""
        if price == 0.0:
            return 0

        if signal.type == "SIGNAL_STOCK":
            cash_amount = self.current_position["Cash"] * self.weights.get(
                signal.type, 0)
        else:
            cash_amount = self.current_position["Cash"]
        return math.floor(cash_amount / price)
