"""Event based backtester"""

from queue import Queue
from .datahandler import SPXDataHandler
from .strategy import Benchmark
from .portfolio import Portfolio


def run(data_path, data_handler=SPXDataHandler, strat=Benchmark):
    events = Queue()
    bars = SPXDataHandler(data_path, events)
    port = Portfolio(bars, events)
    strategy = strat(bars, events)

    while True:
        bars.update_bars()
        if not bars.continue_backtest:
            break

        while True:
            if events.empty():
                break
            event = events.get()
            if event.type == "MARKET":
                strategy.generate_signals(event)
                port.update_timeindex(event)
            elif event.type == "SIGNAL":
                port.update_signal(event)

    return port
