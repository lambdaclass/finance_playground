#!/usr/bin/env python3
"""Argentina ADR volatility analysis.

Explores the performance of Argentine ADRs with focus on the August 2019
crash, when the Merval index fell 48% in dollar terms in a single day.
Examines daily returns distributions, volatility, outlier frequency, and
the volatility smile in options markets during stress events.

Data: committed CSVs in data/ (adrs.csv, blue_chip.csv, adr_options*.csv)
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
import seaborn as sns

PROJECT_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts"))

from style import apply_style, savefig, FT_BLUE, FT_RED, FT_GREEN, FT_DARK

CHARTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(CHARTS, exist_ok=True)

apply_style()


# ── Data loading ───────────────────────────────────────────────────────

def load_adrs():
    df = pd.read_csv(
        os.path.join(DATA, "adrs.csv"), index_col="date", parse_dates=["date"]
    )
    df.index = pd.DatetimeIndex(df.index.date, name="date")
    return df


def load_blue_chip():
    df = pd.read_csv(
        os.path.join(DATA, "blue_chip.csv"),
        index_col=["date", "symbol"],
        parse_dates=["date"],
    )
    df["log_return"] = df.groupby("symbol")["adjClose"].apply(
        lambda x: np.log(x) - np.log(x.shift(1))
    )
    return df


def load_options(filename):
    return pd.read_csv(
        os.path.join(DATA, filename),
        index_col="quotedate",
        parse_dates=["quotedate", "expiration"],
    )


# ── Returns analysis ───────────────────────────────────────────────────

def compute_returns(adrs_df):
    adrs_df["return"] = adrs_df.groupby("symbol")["adjClose"].pct_change() * 100
    adrs_df["log_return"] = np.log(adrs_df["return"] / 100 + 1.0)
    return adrs_df


def plot_adjusted_close(adrs_df):
    """Adjusted close prices for all ADRs."""
    g = sns.relplot(
        x="date", y="adjClose", col="symbol", hue="symbol",
        facet_kws=dict(sharey=False, sharex=False), col_wrap=3, legend=False,
        kind="line", data=adrs_df.reset_index(),
    )
    g.fig.suptitle("Daily adjusted close prices for Argentina's ADRs (USD)", size=14)
    g.fig.subplots_adjust(top=0.96)
    savefig(g.fig, os.path.join(CHARTS, "adr_adjusted_close.png"))


def plot_2019_close(adrs_df):
    adrs_2019 = adrs_df.loc["2019"]
    g = sns.relplot(
        x="date", y="adjClose", col="symbol", hue="symbol",
        facet_kws=dict(sharey=False, sharex=False), col_wrap=3, legend=False,
        kind="line", data=adrs_2019.reset_index(),
    )
    g.fig.suptitle("ADR adjusted close prices (USD) — 2019", size=14)
    g.fig.subplots_adjust(top=0.96)
    savefig(g.fig, os.path.join(CHARTS, "adr_2019_close.png"))


def plot_return_histograms(adrs_df):
    g = sns.FacetGrid(adrs_df, col="symbol", col_wrap=5, hue="symbol", sharey=False, sharex=False)
    g.map(plt.hist, "return", bins=25, density=True)
    g.fig.suptitle("Histogram of daily returns", size=14)
    g.fig.subplots_adjust(top=0.93)
    savefig(g.fig, os.path.join(CHARTS, "return_histograms.png"))


def plot_return_boxen(adrs_df):
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.boxenplot(y="symbol", x="return", data=adrs_df, orient="h", ax=ax)
    ax.set_title("Daily returns per symbol", size=14)
    savefig(fig, os.path.join(CHARTS, "return_boxenplot.png"))


def plot_large_movements(adrs_df):
    large = adrs_df.loc[adrs_df["return"].abs() >= 30]
    if len(large) == 0:
        print("  No movements >= 30%, skipping plot")
        return
    fig, ax = plt.subplots()
    sns.scatterplot(x=large.index, y="return", hue="symbol", data=large, ax=ax)
    ax.set_title("Large daily returns (+/- 30%)", size=14)
    savefig(fig, os.path.join(CHARTS, "large_movements.png"))


def plot_filtered_histograms(adrs_df):
    g = sns.FacetGrid(adrs_df, col="symbol", col_wrap=5, hue="symbol", sharex=False)
    g.map(plt.hist, "return", bins=25, density=True, range=(-10, 10))
    g.fig.suptitle("Histogram of daily returns (between -10% / +10%)", size=14)
    g.fig.subplots_adjust(top=0.93)
    savefig(g.fig, os.path.join(CHARTS, "return_histograms_filtered.png"))


# ── Volatility analysis ───────────────────────────────────────────────

def plot_volatility(adrs_df, blue_chip):
    adr_vol = adrs_df.groupby("symbol")["log_return"].std()
    bc_vol = blue_chip.groupby("symbol")["log_return"].std()
    combined = pd.concat([adr_vol, bc_vol])

    fig, ax = plt.subplots()
    sns.barplot(x=combined.index, y=combined.values, ax=ax)
    ax.set_title(r"Daily volatility $\sigma$ (std of log returns)", size=14)
    ax.tick_params(axis="x", rotation=90)
    savefig(fig, os.path.join(CHARTS, "volatility_comparison.png"))


def plot_outliers(adrs_df):
    adr_vol = adrs_df.groupby("symbol")["log_return"].std()

    def outlier_filter(symbol_df):
        symbol = symbol_df["symbol"].iloc[0]
        return symbol_df.loc[
            (symbol_df["log_return"] - symbol_df["log_return"].mean()).abs()
            >= 3 * adr_vol[symbol]
        ]

    outliers = adrs_df.groupby("symbol").apply(outlier_filter).reset_index(level=0, drop=True)

    # Scatter plot
    fig, ax = plt.subplots()
    sns.scatterplot(x=outliers.index, y="log_return", hue="symbol", data=outliers, ax=ax)
    ax.set_title(r"$3\sigma$ outlier daily returns", size=14)
    savefig(fig, os.path.join(CHARTS, "outlier_returns.png"))

    # Outlier proportion
    outlier_count = outliers.groupby("symbol")["log_return"].count()
    ret_count = adrs_df.groupby("symbol")["log_return"].count()
    outlier_pct = 100 * outlier_count / ret_count

    fig, ax = plt.subplots()
    sns.barplot(x=outlier_pct.index, y=outlier_pct.values, ax=ax)
    ax.axhline(0.3, alpha=0.6, linestyle="--", color="r", label="Expected 0.3%")
    ax.legend()
    ax.set_title("Outlier proportion (%)", size=14)
    ax.tick_params(axis="x", rotation=90)
    savefig(fig, os.path.join(CHARTS, "outlier_proportion.png"))


def plot_cumulative_returns(adrs_df):
    pivoted = adrs_df.pivot(columns="symbol", values="log_return")
    fig, ax = plt.subplots()
    pivoted.cumsum().apply(np.exp).plot(ax=ax, colormap="Set1")
    ax.set_title("Cumulative log returns", size=14)
    savefig(fig, os.path.join(CHARTS, "cumulative_returns.png"))


# ── Options: volatility smile ─────────────────────────────────────────

def plot_vol_smile(options_df, date_str, title_suffix):
    day = options_df.loc[date_str]
    day = day.query(
        '((type == "put") & (strike <= underlying_last)) | '
        '((type == "call") & (strike > underlying_last))'
    )
    if len(day) == 0:
        print(f"  No data for {date_str}, skipping")
        return

    g = sns.relplot(
        x="strike", y="impliedvol", col="underlying",
        facet_kws=dict(sharey=False, sharex=False), col_wrap=3,
        kind="line", data=day, ci=None, color="coral",
    )
    for ax, symbol in zip(g.axes, g.col_names):
        subset = day.loc[day["underlying"] == symbol, "underlying_last"]
        if len(subset) > 0:
            ax.axvline(subset.iloc[0], alpha=0.4, linestyle="--")

    g.fig.suptitle(f"Volatility smiles — {title_suffix}", size=14)
    g.fig.subplots_adjust(top=0.94)
    safe_name = title_suffix.replace(" ", "_").lower()
    savefig(g.fig, os.path.join(CHARTS, f"vol_smile_{safe_name}.png"))


def plot_option_prices(options_df, month_str, title_month):
    """Plot most actively traded call/put prices through a month."""
    month_data = options_df.loc[month_str]
    if len(month_data) == 0:
        return

    def filter_active(symbol_df, option_type="call"):
        return symbol_df.loc[symbol_df["type"] == option_type].nlargest(n=10, columns="openinterest")

    start_date = month_data.index.min()
    first_day = month_data.loc[start_date]

    active_calls = first_day.groupby("underlying").apply(filter_active).reset_index(level=0, drop=True)
    active_puts = first_day.groupby("underlying").apply(
        lambda df: filter_active(df, "put")
    ).reset_index(level=0, drop=True)

    for label, contracts_df, option_type in [
        ("calls", active_calls, "call"),
        ("puts", active_puts, "put"),
    ]:
        contracts = contracts_df["optionroot"]
        active = month_data.loc[month_data["optionroot"].isin(contracts)]
        active = active.copy()
        active["day"] = active.index.strftime("%d")

        g = sns.relplot(
            x="day", y="ask", col="underlying", hue="optionroot",
            facet_kws=dict(sharey=False, sharex=False), col_wrap=3, legend=None,
            kind="line", data=active, ci=None,
        )
        g.fig.suptitle(f"Ask price for most actively traded {label} — {title_month}", size=14)
        g.fig.subplots_adjust(top=0.94)
        safe = title_month.replace(" ", "_").lower()
        savefig(g.fig, os.path.join(CHARTS, f"option_{label}_{safe}.png"))


# ── Yearly returns ─────────────────────────────────────────────────────

def plot_mean_yearly_returns(adrs_df, blue_chip):
    yearly = np.exp(
        adrs_df.groupby("symbol")["log_return"].resample("YE", label="right").sum()
    ) - 1
    yearly = yearly.reset_index()
    yearly["return %"] = yearly["log_return"] * 100

    bc = blue_chip.reset_index(level="symbol")
    bc_yearly = np.exp(
        bc.groupby("symbol")["log_return"].resample("YE", label="right").sum()
    ) - 1
    bc_yearly = bc_yearly.reset_index()
    bc_yearly["return %"] = bc_yearly["log_return"] * 100

    mean_rets = yearly.groupby("symbol")["return %"].mean()
    mean_rets = pd.concat([mean_rets, bc_yearly.groupby("symbol")["return %"].mean()])

    fig, ax = plt.subplots()
    sns.barplot(x=mean_rets.index, y=mean_rets.values, ax=ax)
    ax.set_title("Mean yearly returns — Argentina ADRs vs US blue chips", size=14)
    ax.tick_params(axis="x", rotation=90)
    savefig(fig, os.path.join(CHARTS, "mean_yearly_returns.png"))


# ── Main ───────────────────────────────────────────────────────────────

def main():
    print("Argentina ADR Volatility")
    print("=" * 40)

    adrs_df = load_adrs()
    adrs_df = compute_returns(adrs_df)
    blue_chip = load_blue_chip()

    # Price charts
    plot_adjusted_close(adrs_df)
    plot_2019_close(adrs_df)

    # Returns analysis
    plot_return_histograms(adrs_df)
    plot_return_boxen(adrs_df)
    plot_large_movements(adrs_df)
    plot_filtered_histograms(adrs_df)

    # Volatility
    plot_volatility(adrs_df, blue_chip)
    plot_outliers(adrs_df)
    plot_cumulative_returns(adrs_df)
    plot_mean_yearly_returns(adrs_df, blue_chip)

    # Options volatility smile
    adr_options = load_options("adr_options.csv")
    plot_vol_smile(adr_options, "2019-08-09", "August 9th 2019")
    plot_vol_smile(adr_options, "2019-08-12", "August 12th 2019")

    # Option price evolution
    plot_option_prices(adr_options, "2019-08", "August 2019")
    plot_option_prices(adr_options, "2019-06", "June 2019")

    # Historical options
    for filename, month_str, title in [
        ("adr_options_October_2015.csv", None, "October 2015"),
        ("adr_options_November_2015.csv", None, "November 2015"),
        ("adr_options_December_2015.csv", None, "December 2015"),
        ("adr_options_January_2008.csv", None, "January 2008"),
    ]:
        try:
            opts = load_options(filename)
            month_key = opts.index.min().strftime("%Y-%m")
            plot_option_prices(opts, month_key, title)
        except FileNotFoundError:
            print(f"  {filename} not found, skipping")

    print("Done.")


if __name__ == "__main__":
    main()
