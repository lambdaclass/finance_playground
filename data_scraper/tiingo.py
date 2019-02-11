import logging
import pandas_datareader as pdr
from .utils import get_environment_var, save_data

# Default symbols to fetch
assets = [
    "VTSMX", "VFINX", "VIVAX", "VIGRX", "VIMSX", "VMVIX", "VMGIX", "NAESX",
    "VISVX", "VISGX", "BRSIX", "VGTSX", "VTMGX", "VFSVX", "EFV", "VEURX",
    "VPACX", "VEIEX", "CASHX", "VFISX", "VFITX", "IEF", "VUSTX", "VBMFX",
    "VIPSX", "PIGLX", "PGBIX", "VFSTX", "LQD", "VWESX", "VWEHX", "VWSTX",
    "VWITX", "VWLTX", "VGSIX", "GLD", "PSAU", "GSG"
]


def fetch_data(symbols=assets):
    """Fetches historical data for given symbols from Tiingo"""
    api_key = get_environment_var("TIINGO_API_KEY")
    logger = logging.getLogger(__name__)

    symbols = [symbol.upper() for symbol in symbols]
    for symbol in symbols:
        try:
            symbol_data = pdr.get_data_tiingo(symbol, api_key=api_key)
            save_data(symbol, symbol_data, "tiingo")
        except Exception:
            logger.error(
                "Could not save symbol %s data", symbol, exc_info=True)
