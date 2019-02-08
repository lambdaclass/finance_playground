import logging
import requests
from bs4 import BeautifulSoup
from .utils import save_data

url = "http://www.cboe.com/delayedquote/quote-table-download"

symbols = ["SPX", "SPY"]


def fetch_data(symbols=symbols):
    """Fetches options data for a given list of symbols"""
    logger = logging.getLogger(__name__)
    try:
        form_data = _get_form_data()
    except requests.ConnectionError as ce:
        logger.critical(
            "Connection error trying to reach %s", url, exc_info=True)
        raise (ce)
    except Exception as e:
        logger.critical("Error parsing response", exc_info=True)
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
            save_data(symbol, symbol_data, "cboe")
        except Exception:
            logger.error(
                "Error fetching symbol %s data", symbol, exc_info=True)


def _get_form_data():
    """Return validation form data"""
    homepage = requests.get(url)
    soup = BeautifulSoup(homepage.content, "lxml")
    data = {
        "__VIEWSTATE": soup.select_one("#__VIEWSTATE")["value"],
        "__EVENTVALIDATION": soup.select_one("#__EVENTVALIDATION")["value"]
    }
    return data
