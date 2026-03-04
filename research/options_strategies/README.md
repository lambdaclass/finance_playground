# Options Strategies

Implementation and backtest of two options strategies:

1. **Long Straddle** — Buy ATM call + put, profit from volatility increases. Bounded risk (premium paid), unbounded profit potential.
2. **Iron Butterfly** — Sell ATM straddle + buy OTM wings, profit from low volatility. Limited risk and limited profit.

Merged from two original notebooks (0.2-exploring-options-strategies and 0.5-iron-butterfly).

## Data

Requires SPX options data in `data/`. The full backtest used a private HDF5 dataset with SPX options from 1990-2018. A sample CSV (`SPX_2010.csv`) can be used for demonstration.

## References

- [Investopedia: Straddle](https://www.investopedia.com/terms/s/straddle.asp)
- [Investopedia: Iron Butterfly](https://www.investopedia.com/terms/i/ironbutterfly.asp)
- [CBOE: VIX Index](https://www.investopedia.com/articles/active-trading/070213/tracking-volatility-how-vix-calculated.asp)

## Run

```bash
python run.py
```
