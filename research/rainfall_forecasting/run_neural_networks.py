#!/usr/bin/env python3
"""Neural network models for rainfall maxima forecasting.

Implements LSTM, Bidirectional LSTM, and Wavelet+ARIMA/LSTM hybrid
approaches to predict the yearly maximum rainfall for San Luis Tucuman.

Based on the neural_networks.ipynb notebook from the 2020 Metadata competition.
"""

import os
import sys
import warnings

warnings.filterwarnings("ignore")

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts"))

from style import apply_style, savefig, FT_BLUE, FT_RED, FT_GREEN

CHARTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(CHARTS, exist_ok=True)

apply_style()


def load_data():
    maxima = pd.read_excel(
        os.path.join(DATA, "Estaciones.xlsx"), sheet_name="Maximos", header=1, parse_dates=["Año hid"]
    )
    return maxima["San Luis Tucuman"].dropna().values


def split_sequence(sequence, n_steps):
    X, y = [], []
    for i in range(len(sequence)):
        end_ix = i + n_steps
        if end_ix > len(sequence) - 1:
            break
        X.append(sequence[i:end_ix])
        y.append(sequence[end_ix])
    return np.array(X), np.array(y)


def lstm_forecast(dataset, n_models=5, n_steps=10, epochs=200):
    """Train multiple LSTM models and average predictions."""
    try:
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Dense, LSTM
    except ImportError:
        print("  tensorflow not installed, skipping LSTM")
        return None

    n_features = 1
    X, y = split_sequence(dataset, n_steps)
    X = X.reshape((X.shape[0], X.shape[1], n_features))

    solutions = {}
    for i in range(n_models):
        model = Sequential([
            LSTM(50, activation="relu", return_sequences=True, input_shape=(n_steps, n_features)),
            LSTM(50, activation="relu"),
            Dense(1),
        ])
        model.compile(optimizer="adam", loss="mse")
        model.fit(X, y, epochs=epochs, verbose=0)

        x_ = np.array(dataset[-n_steps:])
        preds = []
        for _ in range(10):
            x_input = x_.reshape((1, n_steps, n_features))
            yhat = model.predict(x_input, verbose=0)
            x_ = np.append(x_[1:], yhat)
            preds.append(yhat[0][0])
        solutions[i] = preds

    # Average across models
    final = []
    for i in range(10):
        final.append(np.mean([solutions[k][i] for k in solutions]))
    return final


def wavelet_arima_forecast(dataset):
    """Wavelet decomposition + ARIMA forecast."""
    try:
        import pywt
        import pmdarima as pm
    except ImportError:
        print("  pywt/pmdarima not installed, skipping wavelet+ARIMA")
        return None

    cA, cD = pywt.dwt(np.array(dataset, copy=True), "db2")
    long_trend = pywt.idwt(None, cD, "db2", "smooth")
    seasonal = pywt.idwt(cA, None, "db2", "smooth")

    # Fit ARIMA on each component
    model_trend = pm.auto_arima(
        long_trend, start_p=0, start_q=0, max_p=0, max_q=1, m=7,
        start_P=0, seasonal=True, d=1, D=1,
        error_action="ignore", suppress_warnings=True, stepwise=True,
    )
    forecast_trend = model_trend.predict(n_periods=10)

    model_seasonal = pm.auto_arima(
        seasonal, start_p=0, start_q=0, max_p=3, max_q=3,
        start_P=0, seasonal=True, d=2, D=2,
        error_action="ignore", suppress_warnings=True, stepwise=True,
    )
    forecast_seasonal = model_seasonal.predict(n_periods=10)

    return forecast_trend + forecast_seasonal


def plot_forecast(dataset, forecast, label, filename):
    if forecast is None:
        return
    combined = np.append(dataset, forecast)
    fig, ax = plt.subplots()
    ax.plot(combined, label=f"{label} forecast", color=FT_RED)
    ax.plot(dataset, label="San Luis Tucuman dataset", color=FT_BLUE)
    ax.legend()
    ax.set_title(f"Rainfall maxima — {label}")
    ax.set_xlabel("Year index")
    ax.set_ylabel("Rainfall (mm)")
    savefig(fig, os.path.join(CHARTS, filename))


def plot_wavelet_decomposition(dataset):
    """Show wavelet decomposition of the series."""
    try:
        import pywt
    except ImportError:
        return

    cA, cD = pywt.dwt(np.array(dataset, copy=True), "db2")
    long_trend = pywt.idwt(None, cD, "db2", "smooth")
    seasonal = pywt.idwt(cA, None, "db2", "smooth")

    fig, ax = plt.subplots()
    ax.plot(dataset, "-b", label="San Luis Tucuman", color=FT_BLUE)
    ax.plot(long_trend, "-r", label="Long trend", color=FT_RED)
    ax.plot(seasonal, "-g", label="Seasonal", color=FT_GREEN)
    ax.legend()
    ax.set_title("Wavelet decomposition (db2)")
    savefig(fig, os.path.join(CHARTS, "wavelet_decomposition.png"))


def main():
    print("  Loading data...")
    dataset = load_data()
    dataset_trimmed = dataset[1:]  # Skip first value as in original notebook

    # Wavelet decomposition
    plot_wavelet_decomposition(dataset_trimmed)

    # LSTM
    print("  Training LSTM ensemble (5 models)...")
    lstm_preds = lstm_forecast(dataset_trimmed, n_models=5, epochs=200)
    plot_forecast(dataset_trimmed, lstm_preds, "LSTM", "lstm_forecast.png")

    # Wavelet + ARIMA
    print("  Running wavelet + ARIMA...")
    wavelet_preds = wavelet_arima_forecast(dataset_trimmed)
    plot_forecast(dataset_trimmed, wavelet_preds, "Wavelet+ARIMA", "wavelet_arima_forecast.png")

    print("  Neural networks done.")


if __name__ == "__main__":
    main()
