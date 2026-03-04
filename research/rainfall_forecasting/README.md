# Rainfall Forecasting

Entry to the 2020 Metadata competition organized by Fundacion Sadosky. The goal was to forecast yearly maximum rainfall for the San Luis Tucuman weather station.

## Analysis

1. **Data exploration** (`run_exploration.py`) — Loads station and NCEP/NCAR reanalysis data, computes correlations, and analyses the relationship between model grid points and weather stations.

2. **Neural networks** (`run_neural_networks.py`) — LSTM, Bidirectional LSTM, and Wavelet+ARIMA/LSTM hybrid models for time series forecasting.

3. **Model analysis** (`run_model_analysis.py`) — Detailed correlation analysis including weighted multi-station Pearson coefficients and mean percentage errors vs distance.

## Data

- `data/Estaciones.xlsx` — Weather station observations
- `data/datos NCEP NCAR.xlsx` — NCEP/NCAR reanalysis grid data
- `data/variables e indices NDEFM.xlsx` — Predictor variables and indices

## Run

```bash
python run.py                   # all analyses
python run.py exploration       # data exploration only
python run.py neural_networks   # LSTM models only
python run.py model_analysis    # correlation analysis only
```
