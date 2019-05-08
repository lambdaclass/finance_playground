[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/lambdaclass/finance/ergodicity)

Finance Playground
==============================

> Exploratory analysis of historical stock and options data

In this project our aim is to explore and analyse financial instruments (stocks and options in particular) and to develop profitable trading strategies. To that end, we focused on the relation between price time series and factors such as market volatility, interest rates, and various economic indicators.  
You can browse our Jupyter notebooks [here](https://mybinder.org/v2/gh/lambdaclass/finance/ergodicity).

## Recommended reading

### Books

#### Introductory
- Option Volatility and Pricing 2nd Ed. - Natemberg, 2014
- Options, Futures, and Other Derivatives 10th Ed. - Hull 2017
- Trading Options Greeks: How Time, Volatility, and Other Pricing Factors Drive Profits 2nd Ed. - Passarelli 2012

#### Intermediate
- Trading Volatility - Bennet 2014
- Volatility Trading 2nd Ed. - Sinclair 2013

#### Advanced
- Dynamic Hedging - Taleb 1997
- The Volatility Surface: A Practitioner's Guide - Gatheral 2006
- The Volatility Smile - Derman & Miller 2016

### Papers
- [Everybody’s Doing It: Short Volatility Strategies and Shadow Financial Insurers](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3071457)
- [Volatility-of-Volatility Risk](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2497759)
- [The Distribution of Returns](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2828744)
- [Safe Haven Investing Part I - Not all risk mitigation is created equal](https://www.universa.net/UniversaResearch_SafeHavenPart1_RiskMitigation.pdf)
- [Safe Haven Investing Part II - Not all risk is created equal](https://www.universa.net/UniversaResearch_SafeHavenPart2_NotAllRisk.pdf)
- [Safe Haven Investing Part III - Those wonderful tenbaggers](https://www.universa.net/UniversaResearch_SafeHavenPart3_Tenbaggers.pdf)
- [Insurance makes wealth grow faster](https://arxiv.org/abs/1507.04655)
- [Ergodicity economics](https://ergodicityeconomics.files.wordpress.com/2018/06/ergodicity_economics.pdf)
- [The Rate of Return on Everything, 1870–2015](https://economics.harvard.edu/files/economics/files/ms28533.pdf)

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
