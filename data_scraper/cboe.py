import logging
import os
from datetime import date
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
            save_data(symbol, symbol_data.text)
        except Exception:
            logger.error(
                "Error fetching symbol %s data", symbol, exc_info=True)


def save_data(symbol, symbol_data):
    """Saves the contents of `symbol_data` to
    `$SAVE_DATA_PATH/cboe/{symbol}/{symbol}_{%date}.csv`
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
        with open(file_path, "w+") as file:
            file.write(symbol_data)
        logger.debug("Saved daily symbol data as %s", file_path)


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
        df_generator = (pd.read_csv(
            os.path.join(symbol_dir, file), skiprows=2) for file in filenames)
        symbol_df = pd.concat(df_generator, ignore_index=True)
        monthly_file = _monthly_filename(filenames)
        file_path = os.path.join(scraper_dir, monthly_file)
        symbol_df.to_csv(file_path)
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
