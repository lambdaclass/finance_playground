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
