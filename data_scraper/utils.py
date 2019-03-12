import hashlib
import os
from datetime import date


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
    If it is not set, defaults to `./data/scraped`.
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
    symbol_dir = os.path.join(save_data_path, scraper, symbol)

    if not os.path.exists(symbol_dir):
        os.makedirs(symbol_dir)
    file_path = os.path.join(symbol_dir, filename)

    with open(file_path, "w+") as file:
        file.write(symbol_data.content)


def file_hash_matches_data(file_path, data):
    file_md5 = get_file_md5(file_path)
    data_md5 = hashlib.md5(data.encode()).hexdigest()
    return file_md5 == data_md5


def get_file_md5(file, chunk_size=4096):
    md5 = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            md5.update(chunk)

    return md5.hexdigest()
