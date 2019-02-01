import os
from datetime import date, timedelta
import pandas as pd
from backtester.utils import get_data_dir


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


def create_synthetic_data(data_dir):
    """Create an synthetic data set with known statistics.
    Price goes from 1 to 2000.
    Mean = 1000.5
    % Price = 1999"""

    synth_file = os.path.join(data_dir, "synthetic_data.csv")

    day = date(1970, 1, 1)
    with open(synth_file, "w+") as f:
        f.write("date,price\n")
        for i in range(1, 2001):
            line = "{},{}\n".format(day.strftime("%m/%d/%Y"), i)
            f.write(line)
            day += timedelta(days=1)


if __name__ == "__main__":
    data_dir = get_data_dir()
    create_test_data(data_dir)
    create_synthetic_data(data_dir)
