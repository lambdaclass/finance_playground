import os
from datetime import date
import pandas as pd


def get_environment_var(variable):
    """Returns the value of a given environment variable.
    Raises `EnvironmentError` if not found.
    """
    if variable not in os.environ:
        raise EnvironmentError(
            "Environment variable {} not set".format(variable))

    return os.path.expanduser(os.environ[variable])


def get_save_data_path():
    """Reads data path from environment variable `$SAVE_DATA_PATH`.
    If it is not set, defaults to `data/scraped`.
    """
    try:
        data_dir = get_environment_var("SAVE_DATA_PATH")
    except EnvironmentError:
        data_dir = "data/scraped"
        os.makedirs(data_dir)

    return data_dir


def save_data(symbol, symbol_data, scraper):
    """Saves the contents of `symbol_data` to
    `$SAVE_DATA_PATH/{scraper}/{symbol}/{symbol}_{%date}.csv`"""
    filename = date.today().strftime(symbol + "_%Y%m%d.csv")
    save_data_path = get_save_data_path()
    symbol_path = os.path.join(save_data_path, scraper, symbol)

    if not os.path.exists(symbol_path):
        os.makedirs(symbol_path)
    file_path = os.path.join(symbol_path, filename)

    if isinstance(symbol_data, pd.DataFrame):
        symbol_data.to_csv(file_path)
    else:
        with open(file_path, "wb+") as file:
            file.write(symbol_data.content)
