#!/usr/bin/env python3
"""Bayesian autoregressive models for soy futures forecasting.

Fits AR(1) and AR(2) models on closing prices, and AR(1) on returns,
using PyMC for MCMC inference.
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


def plot_forecast(forecast_df, steps, title, filename):
    fig, ax = plt.subplots()
    ax.plot(
        forecast_df.index[-2 * steps : -steps],
        forecast_df["Cierre"][-2 * steps : -steps],
        label="Closing price",
        color=FT_BLUE,
    )
    ax.plot(
        forecast_df.index[-steps:],
        forecast_df["forecast"][-steps:],
        label="Prediction",
        color=FT_RED,
    )
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    ax.figure.autofmt_xdate()
    savefig(fig, os.path.join(CHARTS, filename))


def main():
    try:
        import pymc as pm
        import arviz as az
    except ImportError:
        print("  pymc/arviz not installed, skipping (install with: pip install pymc arviz)")
        return

    print("  Loading data...")
    df = load_data()
    steps = 100
    last_day = df.index[-1]
    last_price = df.loc[last_day, "Cierre"]
    forecast_period = pd.date_range(start=last_day + pd.DateOffset(1), periods=steps, freq="B")

    sigma_prior = 1.0

    # AR(1) on closing price
    print("  Fitting AR(1) on prices...")
    with pm.Model() as ar1:
        phi1 = pm.Normal("phi_1", mu=0, sigma=sigma_prior)
        data = pm.AR("p", rho=[phi1], constant=False, observed=df["Cierre"])
        trace = pm.sample(10000, tune=4000, progressbar=False)
        map_ar1 = pm.find_MAP(progressbar=False)

    fig = az.plot_trace(trace).ravel()[0].figure
    savefig(fig, os.path.join(CHARTS, "bayesian_ar1_trace.png"))

    phi1_hat = map_ar1["phi_1"]
    forecast = np.repeat(phi1_hat, steps).cumprod()
    forecasts = pd.DataFrame({"forecast": last_price * forecast}, index=forecast_period)
    forecast_df = pd.concat([df, forecasts])
    plot_forecast(forecast_df, steps, "AR(1) on closing price", "bayesian_ar1_forecast.png")

    # AR(2) on closing price
    print("  Fitting AR(2) on prices...")
    with pm.Model() as ar2:
        phi1 = pm.Normal("phi_1", mu=0, sigma=sigma_prior)
        phi2 = pm.Normal("phi_2", mu=0, sigma=sigma_prior)
        data = pm.AR("p", rho=[phi1, phi2], constant=False, observed=df["Cierre"])
        trace = pm.sample(10000, tune=4000, progressbar=False)
        map_ar2 = pm.find_MAP(progressbar=False)

    phi1_hat = map_ar2["phi_1"]
    phi2_hat = map_ar2["phi_2"]

    prices = [last_price, df["Cierre"].iloc[-2]]
    for _ in range(steps):
        next_p = phi1_hat * prices[0] + phi2_hat * prices[1]
        prices = [next_p] + prices
    ar2_forecast = np.array(prices[:-2])[::-1]
    forecasts = pd.DataFrame({"forecast": ar2_forecast}, index=forecast_period)
    forecast_df = pd.concat([df, forecasts])
    plot_forecast(forecast_df, steps, "AR(2) on closing price", "bayesian_ar2_forecast.png")

    # AR(1) on returns
    print("  Fitting AR(1) on returns...")
    with pm.Model() as ar1_ret:
        phi1 = pm.Normal("phi_1", mu=0, sigma=sigma_prior)
        data = pm.AR("r", rho=[phi1], constant=False, observed=df["retorno"].dropna())
        trace = pm.sample(10000, tune=4000, progressbar=False)
        map_ar1_ret = pm.find_MAP(progressbar=False)

    phi1_hat_ret = map_ar1_ret["phi_1"]
    last_return = df["retorno"].iloc[-1]
    forecast = (np.repeat(phi1_hat_ret, steps) * last_return + 1).cumprod()
    forecasts = pd.DataFrame({"forecast": last_price * forecast}, index=forecast_period)
    forecast_df = pd.concat([df, forecasts])
    plot_forecast(forecast_df, steps, "AR(1) on returns", "bayesian_ar1_returns_forecast.png")

    print("  Bayesian done.")


if __name__ == "__main__":
    main()
