import os
import pandas as pd


def get_spx_data_dir():
    if "OPTIONS_DATA_PATH" in os.environ:
        data_dir = os.path.expanduser(os.environ["OPTIONS_DATA_PATH"])
    else:
        data_dir = "data"
        os.mkdir(data_dir)

    return data_dir


def create_test_data(data_dir):
    """Create test data set with 10 years of SPX"""

    spx_dir = os.path.join(data_dir, "allspx")
    test_file = os.path.join(data_dir, "SPX_2008-2018.csv")

    with open(test_file, "w+") as f:
        f.write("date,price\n")

    for year in range(2008, 2019):
        filename = "SPX_{}.csv".format(year)
        year_df = pd.read_csv(os.path.join(spx_dir, filename))
        grouped = year_df.groupby("quotedate").first()
        grouped.to_csv(
            test_file, mode="a", columns=["underlying_last"], header=False)


if __name__ == "__main__":
    data_dir = get_spx_data_dir()
    create_test_data(data_dir)
