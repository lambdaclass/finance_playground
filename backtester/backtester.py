"""Event based backtester"""

from queue import Queue
from .datahandler import SPXDataHandler, HistoricDataHandler
from .strategy import TailHedge
from .portfolio import WeightedPortfolio
from .utils import get_file_path


def run(option_dir="allspx",
        spx_file="SPX_1990-2018.csv",
        spx_handler=SPXDataHandler,
        options_handler=HistoricDataHandler,
        port_class=WeightedPortfolio,
        strat_class=TailHedge,
        **strat_args):

    events = Queue()

    option_bars = options_handler(option_dir, events)

    spx_path = get_file_path(spx_file)
    spx_bars = spx_handler(spx_path, events)

    port = port_class(spx_bars, option_bars, events)
    strat = strat_class(spx_bars, option_bars, events, **strat_args)

    while True:
        spx_bars.update_bars()
        option_bars.update_bars()
        if not (option_bars.continue_backtest and spx_bars.continue_backtest):
            break

        while True:
            if events.empty():
                port.update_timeindex()
                break
            event = events.get()
            if event.type == "MARKET" or event.type == "OPTIONS":
                strat.generate_signals(event)
            elif event.type == "SIGNAL_STOCK" or event.type == "SIGNAL_OPTIONS":
                port.update_signal(event)

    return port
