import argparse
from .cboe import CBOE


parser = argparse.ArgumentParser(prog="data_scraper.py")
parser.add_argument("-t", "--symbols", nargs="+", 
                    help="Symbols to fetch", required=True)
parser.add_argument("-s", "--scraper", choices=["cboe"])
args = parser.parse_args()

symbols = [symbol.upper() for symbol in args.symbols]
scraper = CBOE()
scraper.fetch_data(symbols)
