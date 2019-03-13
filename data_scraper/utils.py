import hashlib
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
