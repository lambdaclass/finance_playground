#!/usr/bin/env python3
"""ARIMA model for soy futures forecasting.

Fits ARIMA(1,0,1) on daily returns, uses GARCH to check residual
volatility. Also tests restricted 7-month window (Feb-Aug).
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
import statsmodels.api as sm
from arch import arch_model

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


def hurst(ts):
    """Hurst exponent to characterise mean-reversion/trending."""
    lags = range(2, 100)
    tau = [np.sqrt(np.std(np.subtract(ts[lag:], ts[:-lag]))) for lag in lags]
    poly = np.polyfit(np.log(lags), np.log(tau), 1)
    return poly[0] * 2.0


def main():
    print("  Loading data...")
    df = load_data()
    retornos = df["retorno"].dropna()

    # Hurst exponents
    print(f"  Hurst (price): {hurst(df['Cierre']):.4f}")
    print(f"  Hurst (returns): {hurst(retornos):.4f}")

    # Autocorrelation plots
    fig, (ax1, ax2) = plt.subplots(2, figsize=(14, 8))
    sm.graphics.tsa.plot_acf(df["Cierre"], ax=ax1)
    sm.graphics.tsa.plot_pacf(df["Cierre"], ax=ax2)
    fig.suptitle("Autocorrelation — closing price")
    savefig(fig, os.path.join(CHARTS, "arima_acf_price.png"))

    fig, (ax1, ax2) = plt.subplots(2, figsize=(14, 8))
    sm.graphics.tsa.plot_acf(retornos, ax=ax1)
    sm.graphics.tsa.plot_pacf(retornos, ax=ax2)
    fig.suptitle("Autocorrelation — daily returns")
    savefig(fig, os.path.join(CHARTS, "arima_acf_returns.png"))

    # Return histogram
    fig, ax = plt.subplots()
    retornos.plot(kind="hist", bins=50, density=True, ax=ax, color=FT_BLUE)
    ax.set_title("Distribution of daily simple returns")
    savefig(fig, os.path.join(CHARTS, "arima_return_hist.png"))

    # ARIMA(1,0,1) — full series
    p, q = 1, 1
    n = 13
    model = sm.tsa.statespace.SARIMAX(retornos.values, order=(p, 0, q), seasonal=False)
    fit = model.fit(disp=False)
    mean_pred = fit.forecast(n)

    fig, ax = plt.subplots()
    pd.Series((1 + mean_pred).cumprod() * df["Cierre"].iloc[-1]).plot(ax=ax, color=FT_BLUE)
    ax.set_title("ARIMA(1,0,1) — predicted closing price")
    ax.set_ylabel("Price")
    savefig(fig, os.path.join(CHARTS, "arima_forecast_price.png"))

    # GARCH on residuals
    residuals = fit.resid
    garch = arch_model(residuals, vol="GARCH", p=1, q=1)
    garch_fit = garch.fit(disp="off")

    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(garch_fit.conditional_volatility, color=FT_RED)
    ax.set_title("GARCH in-sample conditional volatility")
    savefig(fig, os.path.join(CHARTS, "arima_garch_volatility.png"))

    # ARIMA on 7-month window
    retornos_7m = df.loc[df.index >= df.index.max() - pd.DateOffset(months=7), "retorno"].dropna()
    model_7m = sm.tsa.statespace.SARIMAX(retornos_7m.values, order=(p, 0, q), seasonal=False)
    fit_7m = model_7m.fit(disp=False)
    mean_pred_7m = fit_7m.forecast(n)

    fig, ax = plt.subplots()
    pd.Series((1 + mean_pred_7m).cumprod() * df["Cierre"].iloc[-1]).plot(ax=ax, color=FT_BLUE)
    ax.set_title("ARIMA(1,0,1) — 7 month window forecast")
    ax.set_ylabel("Price")
    savefig(fig, os.path.join(CHARTS, "arima_7m_forecast.png"))

    # Error comparison with actual futures
    try:
        futuros = load_futures()
        futuros = pd.concat([futuros, df.loc[["2019-08-29"]]])
        futuros = futuros.sort_index()
        futuros["retorno"] = futuros["Cierre"].pct_change()
        daily_ret_fut = futuros["Cierre"].pct_change().dropna()

        mae_arima = np.abs(daily_ret_fut.reset_index()["Cierre"].values - mean_pred[:13]).sum() / 13
        mae_last = daily_ret_fut.abs().sum() / 13
        print(f"  MAE (ARIMA full): {mae_arima:.6f}")
        print(f"  MAE (last value): {mae_last:.6f}")

        mae_7m = np.abs(daily_ret_fut.reset_index()["Cierre"].values - mean_pred_7m[:13]).sum() / 13
        print(f"  MAE (ARIMA 7M):   {mae_7m:.6f}")
    except Exception as e:
        print(f"  Could not compare with futures: {e}")

    # Seasonal Feb-Aug plot
    df_seasonal = df.loc[(df.index.month > 1) & (df.index.month < 9)].copy()
    df_seasonal["year"] = df_seasonal.index.year
    fig, axes = plt.subplots(4, 4, figsize=(18, 14))
    years = sorted(df_seasonal["year"].unique())
    for ax, year in zip(axes.flat, years[:16]):
        subset = df_seasonal[df_seasonal["year"] == year]
        ax.plot(subset.index, subset["Cierre"], color=FT_BLUE)
        ax.set_title(str(year), fontsize=9)
        ax.tick_params(axis="x", rotation=45, labelsize=7)
    fig.suptitle("Closing price by year — Feb to Aug cycle", fontsize=14)
    fig.tight_layout()
    savefig(fig, os.path.join(CHARTS, "arima_seasonal.png"))

    print("  ARIMA done.")


if __name__ == "__main__":
    main()
