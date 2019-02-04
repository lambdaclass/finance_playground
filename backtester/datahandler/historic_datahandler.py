import os
import pandas as pd
from .datahandler import DataHandler
from ..event import OptionsMarketEvent
from ..utils import get_file_path


class HistoricDataHandler(DataHandler):
    """Handler for Historical Option Data from 1990-2018"""

    def __init__(self, data_dir, events):
        self._data_generator = self._get_data_generator(data_dir)
        self.events = events
        self.continue_backtest = True

    def get_latest_bars(self, symbol, N=1):
        """Returns the latest options for the underlying `symbol`.
        Returns empty dataframe if `symbol` is not in self._data.
        """
        return self._data[self._data["symbol"] == symbol]

    def update_bars(self):
        """Add new data bar to `self._data`"""
        try:
            self.current_date, self._data = next(self._data_generator)
            self.events.put(OptionsMarketEvent())
        except StopIteration:
            self.continue_backtest = False

    def _get_data_generator(self, data_dir):
        """Creates a generator that yields a days worth of
        options data. Runs from 1990 to 2018.
        """
        for year in range(1990, 2000):
            filename = "SPX_{}.csv".format(year)
            file = get_file_path(os.path.join(data_dir, filename))

            df = pd.read_csv(file, parse_dates=["quotedate", "expiration"])
            columns = {"quotedate": "date", "underlying": "symbol"}
            df.rename(columns=columns, inplace=True)

            for day, df in df.groupby("date"):
                yield day, df
