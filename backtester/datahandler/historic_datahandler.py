from datetime import timedelta
import pandas as pd
from .datahandler import DataHandler
from ..event import MarketEvent


class HistoricDataHandler(DataHandler):
    """Handler for Historical Option Data"""

    def __init__(self, data_path, events):
        self._data = pd.read_csv(
            data_path, parse_dates=["quotedate",
                                    "expiration"]).sort_values(by="date")

        columns = {"quotedate": "date", "optionroot": "symbol"}
        self._data.rename(columns=columns, inplace=True)
        self.current_date = self._data["date"].min() - timedelta(days=1)
        self._end_date = self._data["date"].max()
        self.events = events
        self.continue_backtest = True

    def get_latest_bars(self, symbol, N=1):
        """Returns the latest `N` bars for `symbol` if there are at least N
        rows, otherwise returns the all data.
        Returns empty dataframe if `symbol` is not in self._data.
        """
        return self._data[(self._data["symbol"] == symbol)
                          & (self._data["date"] <= self.current_date)][-N:]

    def update_bars(self):
        """Add new data bar to self.data"""
        if self.current_date < self._end_date:
            self.current_date += timedelta(days=1)
            self.events.put(MarketEvent())
        else:
            self.continue_backtest = False
