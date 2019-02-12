from copy import copy
import pandas as pd
from .strategy import Strategy
from ..event import StockSignalEvent, OptionsSignalEvent


class TailHedge(Strategy):
    """Tail hedge strategy
    Allocate 97% of portfolio to SPX.
    With the remaining 3%, buy `percent_otm` OTM puts with 60-70 dte.
    Sell puts 30 days after buying them.
    """

    def __init__(self, spx_handler, options_handler, events, percent_otm=0.3):
        self.spx_handler = spx_handler
        self.options_handler = options_handler
        self.events = events
        self.percent_otm = percent_otm
        self._sell_put = (None, None)  # (sell_date, sell_signal)
        self._buy_put = True
        self._buy_spx = True

    def generate_signals(self, event):
        """Generates buy signals for `percent_otm` puts and sells them
        30 days after.
        """
        sell_date = self._sell_put[0]
        if sell_date and sell_date <= self.options_handler.current_date:
            # Sell puts and rebalance portfolio
            sell_signal = self._sell_put[1]
            self.events.put(sell_signal)
            self.events.put(
                StockSignalEvent(
                    symbol="SPX", direction="SELL", strength=(1.0, 100)))
            self._sell_put = (None, None)
            self._buy_put = True
            self._buy_spx = True

        if event.type == "MARKET" and self._buy_spx:
            self.events.put(
                StockSignalEvent(
                    symbol="SPX", direction="BUY", strength=(1.0, 100)))
            self._buy_spx = False

        if event.type == "OPTIONS" and self._buy_put:
            latest_options = self.options_handler.get_latest_bars("SPX")
            latest_puts = latest_options[latest_options["type"] == "put"]
            otm_puts = latest_puts[
                self._calculate_percent_otm(latest_puts) >= self.percent_otm]
            candidates = self._time_slice_options(otm_puts, 60, 80)

            if not candidates.empty:
                option = candidates.iloc[0]
                buy_signal = OptionsSignalEvent(
                    symbol="SPX",
                    optionroot=option["optionroot"],
                    option_type=option["type"],
                    direction="BUY")
                self.events.put(buy_signal)

                self._buy_put = False
                sell_signal = copy(buy_signal)
                sell_signal.direction = "SELL"
                self._sell_put = (option["date"] + pd.Timedelta(days=30),
                                  sell_signal)

    def _calculate_percent_otm(self, options):
        """Returns series of otm percentages"""
        return (options["underlying_last"] -
                options["strike"]) / options["underlying_last"]

    def _time_slice_options(self, options, window_start, window_end):
        """Returns dataframe of options with expiration between `window_start`
        and `window_end` days from the current date.
        """
        current_date = self.options_handler.current_date
        return options[(options["expiration"] >= current_date + pd.Timedelta(
            days=window_start)) & (options["expiration"] <= current_date +
                                   pd.Timedelta(days=window_end))]
