Algorithmic Trading
==============================

> Exploratory analysis of historical options data

## Requirements

- Python >= 3.6
- pipenv

Set the environment variable `$OPTIONS_DATA_PATH` to the appropriate data dir.

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

### Scrape daily options data from CBOE (pass symbols through SYM)

```shell
$> make scrape SYM="spy msft"
```

### Run backtester with benchmark strategy

```shell
$> make bench
```
