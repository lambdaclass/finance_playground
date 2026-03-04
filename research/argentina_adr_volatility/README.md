# Argentina ADR Volatility

Exploration of Argentine ADRs and their options during the August 2019 market crash, when the Merval index fell 48% in dollar terms in a single day.

Examines:
- Daily return distributions and whether log returns are normal
- Volatility comparison with US blue chip stocks
- Frequency of 3-sigma outlier events
- Volatility smile behaviour during stress (Aug 2019) and calm (Jun 2019) periods
- Options price evolution across crisis months

## Data

Requires CSV files in `data/`:
- `adrs.csv` — Daily EOD data for Argentine ADRs
- `blue_chip.csv` — US blue chip comparison (KO, GS, IBM, WMT)
- `adr_options.csv` — Options EOD data for ADRs
- `adr_options_October_2015.csv`, `adr_options_November_2015.csv`, `adr_options_December_2015.csv`, `adr_options_January_2008.csv`

## References

- [FT: Argentina's market crash](https://www.ft.com/content/29764546-c821-11e9-a1f4-3669401ba76f)

## Run

```bash
python run.py
```
