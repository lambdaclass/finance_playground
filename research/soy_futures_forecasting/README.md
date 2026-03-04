# Soy Futures Forecasting

Entry to the 2019 Metadata soybean futures forecasting competition organized by Fundacion Sadosky and MATBA ROFEX (ranked 3rd).

## Models

1. **ARIMA** (`run_arima.py`) — ARIMA(1,0,1) on daily returns with GARCH residual analysis
2. **Prophet** (`run_prophet.py`) — Facebook's additive decomposition model with biannual seasonality
3. **Bayesian AR** (`run_bayesian.py`) — AR(1) and AR(2) via PyMC MCMC inference
4. **BSTS** (`run_bsts.py`) — Bayesian Structural Time Series via TensorFlow Probability

## Conclusion

All models converge on the same insight: the best predictor of tomorrow's closing price is today's closing price. The final submission used ARIMA(1,0,1) as the simplest interpretable model (Ockham's razor).

## Data

- `data/datasetRofex2.csv` — Historical soy futures (ROFEX)
- `data/Futuros.csv` — Actuals for the prediction period
- `data/forecast.csv` — Competition submission

## Run

```bash
python run.py              # all models
python run.py arima        # ARIMA only
python run.py prophet      # Prophet only
python run.py bayesian     # Bayesian AR only
python run.py bsts         # BSTS only
```
