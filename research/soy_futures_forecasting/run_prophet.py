#!/usr/bin/env python3
"""Facebook Prophet model for soy futures forecasting."""

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

from style import apply_style, savefig, FT_BLUE, FT_RED

CHARTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(CHARTS, exist_ok=True)

apply_style()


def load_data():
    df = pd.read_csv(os.path.join(DATA, "datasetRofex2.csv"))
    df["Fecha"] = pd.to_datetime(df["Fecha"].str.replace(r" 12:00:00 a\.m\.", "", regex=True), format="%d/%m/%Y")
    df = df.set_index("Fecha")
    df["retorno"] = df["Cierre"].pct_change()
    return df


def load_futures():
    df = pd.read_csv(os.path.join(DATA, "Futuros.csv"))
    df["Fecha"] = pd.to_datetime(df["Fecha"].str.replace(r" 12:00:00 a\.m\.", "", regex=True), format="%d/%m/%Y")
    df = df.set_index("Fecha")
    return df


def AIC(ts, forecast, k):
    sse = ((ts - forecast) ** 2).sum()
    T = len(ts)
    return T * np.log(sse / T) + 2 * (k + 2)


def main():
    try:
        from prophet import Prophet
    except ImportError:
        print("  prophet not installed, skipping (install with: pip install prophet)")
        return

    print("  Loading data...")
    df = load_data()

    data = pd.DataFrame({"ds": df.index, "y": df["Cierre"]})
    model = Prophet(weekly_seasonality=False)
    model.add_seasonality(name="bianual", period=182, fourier_order=5)
    model.fit(data)

    forecast = model.predict(data)

    # Components plot
    fig = model.plot_components(forecast)
    savefig(fig, os.path.join(CHARTS, "prophet_components.png"))

    # Forecast vs actual
    fig, ax = plt.subplots()
    ax.plot(df.index, df["Cierre"], label="Closing price", color=FT_BLUE)
    ax.plot(forecast["ds"], forecast["yhat"], label="Prophet forecast", color=FT_RED, alpha=0.8)
    ax.set_title("Soy closing price — Prophet forecast")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    savefig(fig, os.path.join(CHARTS, "prophet_forecast.png"))

    aic = AIC(df["Cierre"].values, forecast["yhat"].values, 3)
    print(f"  Prophet AIC = {aic:.2f}")

    # Compare with actuals
    try:
        futuros = load_futures()
        test_periods = pd.DataFrame({"ds": futuros.index})
        predictions = model.predict(test_periods).set_index("ds")
        predictions["retorno"] = predictions["yhat"].pct_change()

        last_price = df.iloc[-1]["Cierre"]
        predictions.iloc[0, predictions.columns.get_loc("retorno")] = (
            predictions["yhat"].iloc[0] - last_price
        ) / last_price

        futuros["retorno"] = futuros["Cierre"].pct_change()
        mae = (predictions["retorno"] - futuros["retorno"]).abs().sum() / (len(futuros) - 1)
        print(f"  Prophet MAE = {mae:.6f}")

        fig, ax = plt.subplots()
        ax.plot(futuros.index, futuros["Cierre"], label="Actual", color=FT_BLUE)
        ax.plot(predictions.index, predictions["yhat"], label="Prophet", color=FT_RED)
        ax.set_title("Soy closing price — Prophet prediction vs actual")
        ax.legend()
        ax.figure.autofmt_xdate()
        savefig(fig, os.path.join(CHARTS, "prophet_vs_actual.png"))
    except Exception as e:
        print(f"  Could not compare with futures: {e}")

    print("  Prophet done.")


if __name__ == "__main__":
    main()
