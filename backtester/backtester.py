"""Event based backtester"""

from queue import Queue
from .datahandler import SPXDataHandler
from .strategy import Benchmark
from .portfolio import SimplePortfolio


def run(data_path,
        data_handler=SPXDataHandler,
        port_class=SimplePortfolio,
        strat_class=Benchmark,
        **strat_args):
    events = Queue()
    bars = data_handler(data_path, events)
    port = port_class(bars, events)
    strat = strat_class(bars, events, **strat_args)

    while True:
        bars.update_bars()
        if not bars.continue_backtest:
            break

        while True:
            if events.empty():
                break
            event = events.get()
            if event.type == "MARKET":
                strat.generate_signals(event)
                port.update_timeindex(event)
            elif event.type == "SIGNAL":
                port.update_signal(event)

    return port
