import os


def get_data_dir():
    """Reads data path from environment variable $OPTIONS_DATA_PATH.
    If it is not set, defaults to `data/`
    """

    if "OPTIONS_DATA_PATH" in os.environ:
        data_dir = os.path.expanduser(os.environ["OPTIONS_DATA_PATH"])
    else:
        data_dir = "data"
        os.mkdir(data_dir)

    return data_dir


def get_file_path(data_file):
    """Returns path to `data_file`. Raises FileNotFound in case of error"""

    data_dir = get_data_dir()
    file_path = os.path.join(data_dir, data_file)

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            "No such file or directory {}".format(file_path))

    return file_path
