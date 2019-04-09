import unittest
from unittest.mock import patch
import os
import shutil

from requests import ConnectionError
import pandas as pd

from data_scraper import cboe


class TestCBOE(unittest.TestCase):
    """Tests CBOE data scraper"""

    test_dir = os.path.join(os.getcwd(), os.path.dirname(__file__))
    test_data_path = os.path.realpath(os.path.join(test_dir, "data"))
    cboe_data_path = os.path.join(test_data_path, "cboe")

    @classmethod
    def setUpClass(cls):
        cls.save_data_path = os.environ.get("SAVE_DATA_PATH", None)
        os.environ["SAVE_DATA_PATH"] = cls.test_data_path

    @classmethod
    def tearDownClass(cls):
        if cls.save_data_path:
            os.environ["SAVE_DATA_PATH"] = cls.save_data_path
        shutil.rmtree(cls.cboe_data_path)

    def test_fetch_spy(self):
        """Fetch todays SPY quote"""
        cboe.fetch_data(["SPY"])
        file_name = "SPY_" + pd.Timestamp.today().strftime("%Y%m%d") + ".csv"
        file_path = os.path.join(TestCBOE.cboe_data_path, "SPY_daily",
                                 file_name)
        spy_df = pd.read_csv(file_path, parse_dates=["quotedate"])
        self.assertTrue(all(spy_df["underlying"] == "SPX"))
        self.assertEqual(spy_df["quotedate"].nunique(), 1)
        counts = spy_df["type"].value_counts()
        self.assertEqual(counts["put"] + counts["call"], len(spy_df))

    @patch("data_scraper.cboe.slack_notification", return_value=None)
    def test_fetch_invalid_symbol(self, mocked_notification):
        """Fetching invalid symbol should send notification"""
        cboe.fetch_data(["FOOBAR"])
        self.assertTrue(mocked_notification.called)

    @patch("data_scraper.cboe.url", new="http://www.aldkfjaskldfjsa.com")
    @patch("data_scraper.cboe.slack_notification", return_value=None)
    def test_no_connection(self, mocked_notification):
        """Raise ConnectionError and send notification when host is unreachable"""
        with self.assertRaises(ConnectionError):
            cboe.fetch_data(["SPX"])
            self.assertTrue(mocked_notification.called)


if __name__ == "__main__":
    unittest.main()
