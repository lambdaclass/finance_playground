Algorithmic Trading
==============================

> Exploratory analysis of historical options data

## Requirements

- Python >= 3.6
- pipenv

For backtesting, set `$OPTIONS_DATA_PATH` to the appropriate data dir.
To use the data scraper the following environment variables need to be set:
- `$SAVE_DATA_PATH`: where the data will be saved to (default is `./data/scraped`)
- `$TIINGO_API_KEY`: used to fetch data from [Tiingo](https://api.tiingo.com)
- `$S3_BUCKET`: name of the S3 bucket to backup data
- `$AWS_ACCESS_KEY_ID`: AWS acces key id
- `$AWS_SECRET_ACCESS_KEY`: AWS secret key

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
$> make scrape scraper=cboe

$> make scrape scraper=tiingo
```

### Run backtester with benchmark strategy

```shell
$> make bench
```

## Deployment

### Create Docker images

```shell
$> make image
```

### Start scraper

```shell
$> make ops
```

### Stop scraper

```shell
$> make stop
```
