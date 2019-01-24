#   CBOE data scraper

import os
from datetime import date
import requests
from bs4 import BeautifulSoup


class CBOE():
    """CBOE data downloader."""
    url = "http://www.cboe.com/delayedquote/quote-table-download"

    def __init__(self):
        self.data_path = self._get_data_path()

    def _get_data_path(self):
        path = os.getenv("OPTIONS_DATA_PATH")
        if not path:
            raise EnvironmentError("Environment variable $OPTIONS_DATA_PATH not set")
        return os.path.expanduser(path)

    def fetch_data(self, symbols):
        """Fetches options data for a given list of symbols"""
        form_data = self._get_form_data()
        headers = {"Referer": CBOE.url}
        file_url = "http://www.cboe.com/delayedquote/quotedata.dat"
        for symbol in symbols:
            form_data["ctl00$ContentTop$C005$txtTicker"] = symbol
            response = requests.post(CBOE.url,
                                     data=form_data,
                                     headers=headers,
                                     allow_redirects=False)
            symbol_data = requests.get(file_url,
                                       cookies=response.cookies,
                                       headers=headers)
            self._save_data(symbol, symbol_data)

    def _get_form_data(self):
        """Return validation form data"""
        homepage = requests.get(CBOE.url)
        soup = BeautifulSoup(homepage.content, "lxml")
        data = {
            "__VIEWSTATE": soup.select_one("#__VIEWSTATE")["value"],
            "__EVENTVALIDATION": soup.select_one("#__EVENTVALIDATION")["value"]      
        }
        return data

    def _save_data(self, symbol, symbol_data):
        """Saves the contents of `symbol_data` to 
        $OPTIONS_DATA_PATH/{symbol}/{symbol}_{%date}.csv""" 
        filename = date.today().strftime(symbol + "_%Y%m%d.csv")
        symbol_path = os.path.join(self.data_path, symbol)
        if not os.path.exists(symbol_path):
            os.makedirs(symbol_path)
        with open(os.path.join(symbol_path, filename), "wb+") as file:
            file.write(symbol_data.content)
