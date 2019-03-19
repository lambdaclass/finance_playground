import logging
import os

from datetime import date
import pandas_datareader as pdr

import utils
import validation
from notifications import slack_notification

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
            msg = "Unable to connect to api.tiingo.com when fetching symbol {}".format(
                symbol)
            logger.error(msg, exc_info=True)
            slack_notification(msg, __name__)
            raise ce
        except TypeError:
            # pandas_datareader raises TypeError when fetching invalid symbol
            msg = "Attempted to fetch invalid symbol {}".format(symbol)
            logger.error(msg, exc_info=True)
            slack_notification(msg, __name__)
        except Exception:
            msg = "Error fetching symbol {}".format(symbol)
            logger.error(msg, exc_info=True)
            slack_notification(msg, __name__)


def save_data(symbol, symbol_df):
    """Saves the contents of `symbol_df` to
    `$SAVE_DATA_PATH/tiingo/{symbol}_{%date}.csv`"""
    filename = date.today().strftime(symbol + "_%Y%m%d.csv")

    save_data_path = utils.get_save_data_path()
    scraper_dir = os.path.join(save_data_path, "tiingo")

    if not os.path.exists(scraper_dir):
        os.makedirs(scraper_dir)
        logger.debug("Scraper dir %s created", scraper_dir)
    file_path = os.path.join(scraper_dir, filename)

    if os.path.exists(file_path) and validation.file_hash_matches_data(
            file_path, symbol_df.to_csv()):
        logger.debug("File %s already downloaded", file_path)
    else:
        validation.validate_dates(symbol_df["date"])

        pattern = symbol + "_*"
        utils.remove_files(scraper_dir, pattern, logger)

        symbol_df.to_csv(file_path)
        logger.debug("Saved symbol data as %s", file_path)
