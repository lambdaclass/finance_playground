class Event():
    """
    Event is base class providing an interface for all subsequent
    (inherited) events, that will trigger further events in the
    trading infrastructure.
    """
    pass


class MarketEvent(Event):
    """
    Handles the event of receiving a new market update with
    corresponding bars.
    """

    def __init__(self):
        self.type = "MARKET"


class OptionsMarketEvent(Event):
    """
    Handles the event of receiving a new options market update with
    corresponding bars.
    """

    def __init__(self):
        self.type = "OPTIONS"


class StockSignalEvent(Event):
    """
    Handles the event of receiving a stock signal from the Strategy
    object.
    Portfolio object processes buy/sell orders.
    """

    def __init__(self, symbol, direction, strength):
        """symbol: ticker symbol
        direction: BUY | SELL
        strength: (%Win chance, Win/Loss ratio)"""
        self.type = "SIGNAL_STOCK"
        self.symbol = symbol
        self.direction = direction
        self.strength = strength


class OptionsSignalEvent(Event):
    """
    Handles the event of receiving a new options signal from the Strategy
    object.
    """

    def __init__(self, symbol, optionroot, option_type, direction):
        """symbol: underlying symbol
        optionroot: option name
        direction: BUY | SELL
        option_type: CALL | PUT
        strength: (%Win chance, Win/Loss ratio)"""
        self.type = "SIGNAL_OPTIONS"
        self.symbol = symbol
        self.optionroot = optionroot
        self.option_type = option_type
        self.direction = direction
