import glob
import os


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


def remove_files(data_dir, pattern, logger=None):
    """Removes files in `data_dir` that match `pattern`"""
    for file in glob.glob(os.path.join(data_dir, pattern)):
        remove_file(file, logger)


def remove_file(file, logger=None):
    os.remove(file)
    if logger:
        logger.debug("Removed file %s", file)
