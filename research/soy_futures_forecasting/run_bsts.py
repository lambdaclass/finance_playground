#!/usr/bin/env python3
"""Bayesian Structural Time Series (BSTS) for soy futures forecasting.

Uses TensorFlow Probability's structural time series module to decompose
the closing price into trend + seasonality components.

Based on Scott & Varian, "Predicting the Present with Bayesian Structural
Time Series" (2014).
"""

import os
import sys
import warnings
from datetime import datetime

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
    date_parser = lambda x: datetime.strptime(x, "%d/%m/%Y 12:00:00 a.m.")
    df = pd.read_csv(
        os.path.join(DATA, "datasetRofex2.csv"),
        parse_dates=["Fecha"],
        index_col="Fecha",
        date_parser=date_parser,
    )
    return df


def plot_bsts_forecast(df, price_mean, price_scale, price_samples, forecast_period, title, filename):
    forecasts = pd.DataFrame({"forecast": price_mean}, index=forecast_period)
    forecast_df = pd.concat([df, forecasts])

    fig, ax = plt.subplots()
    ax.plot(forecast_df.index, forecast_df["Cierre"], label="Closing price", color=FT_BLUE)
    ax.plot(forecast_df.index, forecast_df["forecast"], label="BSTS prediction", color=FT_RED)
    if price_samples is not None:
        ax.plot(forecast_period, price_samples.T, lw=0.5, color=FT_RED, alpha=0.1)
    ax.fill_between(
        forecast_period,
        price_mean - 2 * price_scale,
        price_mean + 2 * price_scale,
        color=FT_RED,
        alpha=0.2,
    )
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    ax.figure.autofmt_xdate()
    savefig(fig, os.path.join(CHARTS, filename))


def main():
    try:
        import tensorflow as tf
        import tensorflow_probability as tfp
        from tensorflow_probability import sts
    except ImportError:
        print("  tensorflow/tensorflow-probability not installed, skipping")
        return

    print("  Loading data...")
    df = load_data()
    steps = 200
    last_day = df.index[-1]
    forecast_period = pd.date_range(start=last_day + pd.DateOffset(1), periods=steps, freq="B")

    # Model 1: Local linear trend + seasonal
    print("  Fitting BSTS model 1 (trend + seasonal)...")
    trend = sts.LocalLinearTrend(observed_time_series=df["Cierre"])
    seasonal = tfp.sts.Seasonal(
        num_seasons=33, num_steps_per_season=123, observed_time_series=df["Cierre"]
    )
    model = sts.Sum([trend, seasonal], observed_time_series=df["Cierre"])

    surrogate = tfp.sts.build_factored_surrogate_posterior(model=model)
    tfp.vi.fit_surrogate_posterior(
        target_log_prob_fn=model.joint_distribution(observed_time_series=df["Cierre"]).log_prob,
        surrogate_posterior=surrogate,
        optimizer=tf.optimizers.Adam(learning_rate=0.1),
        num_steps=200,
    )
    samples = surrogate.sample(50)

    dist = tfp.sts.forecast(
        model, observed_time_series=df["Cierre"], parameter_samples=samples, num_steps_forecast=steps
    )
    price_mean = dist.mean().numpy()[..., 0]
    price_scale = dist.stddev().numpy()[..., 0]
    price_samples = dist.sample(10).numpy()[..., 0]

    plot_bsts_forecast(df, price_mean, price_scale, price_samples, forecast_period,
                       "BSTS Model 1 (trend + seasonal)", "bsts_model1.png")

    # Model 2: Monthly + weekly seasonality + trend
    print("  Fitting BSTS model 2 (monthly + weekly + trend)...")
    monthly = sts.Seasonal(num_seasons=12, num_steps_per_season=246, observed_time_series=df["Cierre"],
                           name="monthly")
    weekly = sts.Seasonal(num_seasons=52, num_steps_per_season=7, observed_time_series=df["Cierre"],
                          name="weekly")
    trend2 = sts.LocalLinearTrend(observed_time_series=df["Cierre"])
    model2 = sts.Sum([monthly, weekly, trend2], observed_time_series=df["Cierre"])

    surrogate2 = tfp.sts.build_factored_surrogate_posterior(model=model2)
    tfp.vi.fit_surrogate_posterior(
        target_log_prob_fn=model2.joint_distribution(observed_time_series=df["Cierre"]).log_prob,
        surrogate_posterior=surrogate2,
        optimizer=tf.optimizers.Adam(learning_rate=0.1),
        num_steps=200,
    )
    samples2 = surrogate2.sample(50)

    dist2 = tfp.sts.forecast(
        model2, observed_time_series=df["Cierre"], parameter_samples=samples2, num_steps_forecast=steps
    )
    price_mean2 = dist2.mean().numpy()[..., 0]
    price_scale2 = dist2.stddev().numpy()[..., 0]
    price_samples2 = dist2.sample(10).numpy()[..., 0]

    plot_bsts_forecast(df, price_mean2, price_scale2, price_samples2, forecast_period,
                       "BSTS Model 2 (monthly + weekly + trend)", "bsts_model2.png")

    print("  BSTS done.")


if __name__ == "__main__":
    main()
