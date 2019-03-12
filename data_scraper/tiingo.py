import logging
import glob
import os
from datetime import date
import pandas_datareader as pdr
from data_scraper import utils

logger = logging.getLogger(__name__)

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
    api_key = utils.get_environment_var("TIINGO_API_KEY")

    symbols = [symbol.upper() for symbol in symbols]
    for symbol in symbols:
        try:
            symbol_data = pdr.get_data_tiingo(symbol, api_key=api_key)
            save_data(symbol, symbol_data)
        except ConnectionError as ce:
            logger.error(
                "Unable to connect to api.tiingo.com while fetching symbol %s",
                symbol,
                exc_info=True)
            raise ce
        except TypeError:
            # pandas_datareader raises TypeError when fetching invalid symbol
            logger.error("Invalid symbol %s", symbol, exc_info=True)
        except Exception:
            logger.error(
                "Could not save symbol %s data", symbol, exc_info=True)


def save_data(symbol, symbol_df):
    """Saves the contents of `symbol_df` to
    `$SAVE_DATA_PATH/tiingo/{symbol}_{%date}.csv`"""
    filename = date.today().strftime(symbol + "_%Y%m%d.csv")

    save_data_path = utils.get_save_data_path()
    scraper_dir = os.path.join(save_data_path, "tiingo")

    if not os.path.exists(scraper_dir):
        os.makedirs(scraper_dir)
    file_path = os.path.join(scraper_dir, filename)

    if os.path.exists(file_path) and utils.file_hash_matches_data(
            file_path, symbol_df.to_csv()):
        logger.debug("File %s already downloaded", file_path)
    else:
        remove_old_files(scraper_dir, symbol)
        symbol_df.to_csv(file_path)
        logger.debug("Saved symbol data as %s", file_path)


def remove_old_files(data_dir, symbol):
    pattern = symbol + "_*"
    for old_file in glob.glob(os.path.join(data_dir, pattern)):
        os.remove(old_file)
        logger.debug("Removed file %s", old_file)
