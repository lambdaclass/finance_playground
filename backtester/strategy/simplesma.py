from .strategy import Strategy
from ..event import SignalEvent


class SimpleSMA(Strategy):
    """Simple moving average strategy.
    We buy/hold the symbol when the moving average in a given period
    is higher than the spot price, we sell otherwise."""

    def __init__(self, data_handler, events, symbol, period):
        self.data_handler = data_handler
        self.symbol = symbol
        self.period = period
        self.events = events

    def generate_signals(self, event):
        period_bars = self.data_handler.get_latest_bars(
            self.symbol, N=self.period)
        is_greater = period_bars["ask"].iloc[-1] >= period_bars["ask"].mean()
        if is_greater:
            signal = SignalEvent(
                symbol=self.symbol, direction="BUY", strength=(1.0, 100))
        else:
            signal = SignalEvent(
                symbol=self.symbol, direction="SELL", strength=(1.0, 100))
        self.events.put(signal)
