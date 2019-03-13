import logging
import os
from datetime import date
from io import StringIO
from itertools import groupby
from bs4 import BeautifulSoup
import requests
import pandas as pd
from data_scraper import utils

logger = logging.getLogger(__name__)

url = "http://www.cboe.com/delayedquote/quote-table-download"
symbols = ["SPX", "SPY"]


def fetch_data(symbols=symbols):
    """Fetches options data for a given list of symbols"""
    try:
        form_data = _form_data()
    except requests.ConnectionError as ce:
        logger.error("Connection error trying to reach %s", url, exc_info=True)
        raise (ce)
    except Exception as e:
        logger.error("Error parsing response", exc_info=True)
        raise (e)

    headers = {"Referer": url}
    file_url = "http://www.cboe.com/delayedquote/quotedata.dat"

    symbols = [symbol.upper() for symbol in symbols]
    for symbol in symbols:
        form_data["ctl00$ContentTop$C005$txtTicker"] = symbol
        try:
            response = requests.post(
                url, data=form_data, headers=headers, allow_redirects=False)
            symbol_data = requests.get(
                file_url, cookies=response.cookies, headers=headers)
            _save_data(symbol, symbol_data.text)
        except Exception:
            logger.error(
                "Error fetching symbol %s data", symbol, exc_info=True)


def collate_monthly_data(symbol):
    """Aggregate daily snapshots into month long csv"""
    save_data_path = utils.get_save_data_path()
    scraper_dir = os.path.join(save_data_path, "cboe")
    symbol_dir = os.path.join(scraper_dir, symbol + "_daily")

    if not os.path.exists(symbol_dir):
        logger.error("Symbol dir %s does not exist", symbol_dir)
        raise FileNotFoundError()

    for month, files in groupby(os.listdir(symbol_dir), _monthly_grouper):
        filenames = list(files)
        df_generator = (pd.read_csv(os.path.join(symbol_dir, file))
                        for file in filenames)
        symbol_df = pd.concat(df_generator)
        monthly_file = _monthly_filename(filenames)
        file_path = os.path.join(scraper_dir, monthly_file)
        symbol_df.to_csv(file_path, index=False)
        logger.debug("Saved monthly data %s", monthly_file)


def _form_data():
    """Return validation form data"""
    homepage = requests.get(url)
    soup = BeautifulSoup(homepage.content, "lxml")
    data = {
        "__VIEWSTATE": soup.select_one("#__VIEWSTATE")["value"],
        "__EVENTVALIDATION": soup.select_one("#__EVENTVALIDATION")["value"]
    }
    return data


def _save_data(symbol, symbol_data):
    """Saves the contents of `symbol_data` to
    `$SAVE_DATA_PATH/cboe/{symbol}_daily/{symbol}_{%date}.csv`
    """
    filename = date.today().strftime(symbol + "_%Y%m%d.csv")

    save_data_path = utils.get_save_data_path()
    symbol_dir = os.path.join(save_data_path, "cboe", symbol + "_daily")

    if not os.path.exists(symbol_dir):
        os.makedirs(symbol_dir)
    file_path = os.path.join(symbol_dir, filename)

    if os.path.exists(file_path) and utils.file_hash_matches_data(
            file_path, symbol_data):
        logger.debug("File %s already downloaded", file_path)
    else:
        daily_df = _wrangle_data(symbol_data)
        daily_df.to_csv(file_path, index=False)
        logger.debug("Saved daily symbol data as %s", file_path)


def _wrangle_data(symbol_data):
    """Returns a properly formated (_tidy_) dataframe"""
    string_data = StringIO(symbol_data)
    first_line = string_data.readline()
    spot_price = float(first_line.split(",")[1])
    quote_date = date.today().strftime("%m/%d/%Y")

    data = pd.read_csv(string_data, skiprows=1)
    call_columns = [
        "Calls", "Expiration Date", "Strike", "Last Sale", "Net", "Bid", "Ask",
        "Vol", "Open Int", "IV", "Delta", "Gamma"
    ]
    calls = data[call_columns]

    put_columns = [
        "Puts", "Expiration Date", "Strike", "Last Sale.1", "Net.1", "Bid.1",
        "Ask.1", "Vol.1", "Open Int.1", "IV.1", "Delta.1", "Gamma.1"
    ]
    puts = data[put_columns]

    renamed_columns = [
        "optionroot", "expiration", "strike", "last", "net", "bid", "ask",
        "volume", "openinterest", "impliedvol", "delta", "gamma"
    ]
    calls.columns = renamed_columns
    calls.insert(loc=1, column="type", value="call")
    puts.columns = renamed_columns
    puts.insert(loc=1, column="type", value="put")

    merged = pd.concat([calls, puts])
    merged.insert(loc=0, column="underlying", value="SPX")
    merged.insert(loc=1, column="underlying_last", value=spot_price)
    merged.insert(loc=2, column="exchange", value="CBOE")
    merged.insert(loc=6, column="quotedate", value=quote_date)

    return merged


def _monthly_grouper(filename):
    """Returns `{year}{month}` string. Used to group files by month."""
    basename = filename.split(".")[0]
    file_date = basename.split("_")[1]
    return file_date[:-2]


def _monthly_filename(filenames):
    """Returns filename of monthly aggregate file in the form
    `{symbol}_{start_date}_to_{end_date}.csv`
    """
    sorted_files = list(sorted(filenames))
    first_file = sorted_files[0]
    last_file = sorted_files[-1]
    last_day = last_file.split(".")[0][-8:]  # Get only the date
    file_name = first_file.split(".")[0] + "_to_" + last_day + ".csv"
    return file_name
