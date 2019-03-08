Algorithmic Trading
==============================

> Exploratory analysis of historical options data

## Requirements

- Python >= 3.6
- pipenv

For backtesting, set `$OPTIONS_DATA_PATH` to the appropriate data dir.
To use the data scraper, set `$SAVE_DATA_PATH`. By default, it will save data to `./data/scraped`.

**HINT**: store environment variables in an `.env` file and pipenv will load them automatically when using `make env`.

## Usage

### Create environment and download dependencies

```shell
$> make init
```

### Activate environment

```shell
$> make env
```

### Run tests

```shell
$> make test
```

### Scrape data (supported scrapers: CBOE, Tiingo)

```shell
$> make scrape symbols=msft,goog scraper=cboe

$> make scrape symbols=voo scraper=tiingo
```

### Run backtester with benchmark strategy

```shell
$> make bench
```

## Data sources

### Exchanges

- [IEX](https://iextrading.com/developer/)
- [Tiingo](https://api.tiingo.com/)
- [CBOE Options Data](http://www.cboe.com/delayedquote/quote-table-download)

### Historical Data

- [Shiller's US Stocks, Dividends, Earnings, Inflation (CPI), and long term interest rates](http://www.econ.yale.edu/~shiller/data.htm)
- [Fama/French US Stock Index Data](http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html)
- [FRED CPI, Interest Rates, Trade Data](https://fred.stlouisfed.org)
- [REIT Data](https://www.reit.com/data-research/reit-market-data/reit-industry-financial-snapshot)
