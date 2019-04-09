import logging
import hashlib

import pandas as pd
import pandas_market_calendars as mcal

from data_scraper import cboe
from data_scraper.notifications import slack_notification

logger = logging.getLogger(__name__)


def file_hash_matches_data(file_path, data):
    file_hash = file_md5(file_path)
    data_md5 = hashlib.md5(data.encode()).hexdigest()
    return file_hash == data_md5


def file_md5(file, chunk_size=4096):
    md5 = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            md5.update(chunk)

    return md5.hexdigest()


def validate_dates(symbol, date_range):
    """Compares `date_range` with NYSE trading calendar and
    returns `True` if there are no missing days.
    """
    # NYSE and CBOE have the same trading calendar
    # https://www.nyse.com/markets/hours-calendars
    # http://cfe.cboe.com/about-cfe/holiday-calendar
    nyse = mcal.get_calendar("NYSE")
    start_date = date_range.min()
    end_date = date_range.max()
    trading_days = nyse.valid_days(start_date=start_date, end_date=end_date)

    # Remove timezone info
    trading_days = trading_days.tz_convert(None)

    missing_days = trading_days.difference(date_range)
    if not missing_days.empty:
        msg = "Some trading dates where missing for symbol {}".format(symbol)
        logger.error("%s\nMissing: %s", msg, missing_days)
        slack_notification(msg, __name__)

    return missing_days.empty


def validate_aggregate_file(aggregate_file, daily_files):
    """Compares `aggregate_file` with the data from `daily_files`."""
    aggregate_df = pd.read_csv(aggregate_file)
    recreated_df = cboe.aggregate_data(daily_files)

    is_valid = aggregate_df.equals(recreated_df)
    if not is_valid:
        msg = "Data in {} differs from the daily files".format(aggregate_file)
        logger.error(msg)
        slack_notification(msg, __name__)

    return is_valid
