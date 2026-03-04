# Wealth Redistribution — RGBM Model

Simulation of the Re-allocating Geometric Brownian Motion model from Adamou, Berman & Peters (2019).

Individuals start at wealth 1. Each period, wealth grows via GBM and a fraction tau is redistributed. The parameter tau controls inequality: positive tau reduces it, negative tau increases it.

## References

- [Wealth Inequality and the Ergodic Hypothesis](http://ssrn.com/abstract=2794830) — Adamou, Berman & Peters
- [Blog post on RGBM](https://ergodicityeconomics.com/2017/08/14/wealth-redistribution-and-interest-rates/)

## Run

```bash
python run.py              # default tau=0.01
python run.py --tau 0.1    # higher redistribution
python run.py --tau -0.5   # negative redistribution
```

Self-contained, no external data needed.
