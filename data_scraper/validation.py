import logging
import hashlib

import pandas as pd
import pandas_market_calendars as mcal

import utils
from notifications import slack_notification

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


def aggregate_data(files):
    """Returns a dataframe of the aggregated data from `files`.
    IMPORTANT: Concatenates data in the order found in `files`.
    """
    df_generator = (pd.read_csv(file) for file in files)
    return pd.concat(df_generator)


def validate_dates(date_range):
    """Raises exception if there are trading days NOT present in `date_range`"""
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
        msg = "Some trading dates where not found in the data"
        logger.critical("%s\nMissing: %s", msg, missing_days)
        slack_notification(msg, __name__)
        raise Exception("Trading dates missing")


def validate_aggregate_file(aggregate_file, daily_files):
    """Raises exception and DELETES `aggregate_file` if it contains different
    data from that in `daily_files`.
    """
    aggregate_df = pd.read_csv(aggregate_file)
    recreated_df = aggregate_data(daily_files)

    if not aggregate_df.equals(recreated_df):
        utils.remove_file(aggregate_file)
        msg = "Data in {} differs from the daily files".format(aggregate_file)
        logger.error(msg)
        slack_notification(msg, __name__)
