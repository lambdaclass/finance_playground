#!/usr/bin/env python3
"""Options strategies: straddle and iron butterfly.

Merged from two notebooks:
- 0.2-exploring-options-strategies (straddle)
- 0.5-iron-butterfly

Implements and backtests:
1. Long straddle: buy ATM call + put, profit from volatility
2. Iron butterfly: sell ATM straddle + buy OTM wings, profit from low vol

NOTE: The full backtest requires a private HDF5 dataset
(options_data_v2.h5) with SPX options from 1990-2018. The script
demonstrates the strategy logic on a sample CSV (SPX_2010.csv) if
available, and fails gracefully if data is missing.
"""

import os
import sys
import warnings
from math import floor

warnings.filterwarnings("ignore")

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

PROJECT_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts"))

from style import apply_style, savefig, FT_BLUE, FT_RED, FT_GREEN

CHARTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(CHARTS, exist_ok=True)

apply_style()


# ── Shared helpers ─────────────────────────────────────────────────────

def dte_filter(data, dte, tolerance=0.0):
    upper = pd.Timedelta(days=floor(dte + dte * tolerance))
    lower = pd.Timedelta(days=floor(dte - dte * tolerance))
    return data[
        (data["expiration"] <= data["quotedate"] + upper)
        & (data["expiration"] >= data["quotedate"] + lower)
    ]


def exit_price_long(data, option):
    if option in data["optionroot"].array:
        return data[data["optionroot"] == option]["bid"].iloc[0]
    return 0.0


def exit_price_dir(data, option, direction="long"):
    price = "bid" if direction == "long" else "ask"
    if option in data["optionroot"].array:
        return data[data["optionroot"] == option][price].iloc[0]
    return 0.0


# ── Straddle ───────────────────────────────────────────────────────────

def straddle(data, entry_dte=36, exit_dte=2, tolerance=0.1, qty=10):
    calls = data[data["type"] == "call"]
    call_candidates = dte_filter(calls, entry_dte, tolerance)
    call_candidates = call_candidates.copy()
    call_candidates["difference"] = np.abs(
        call_candidates["strike"] - call_candidates["underlying_last"]
    )
    idx_calls = call_candidates.groupby("quotedate")["difference"].idxmin()
    straddle_call_enter = call_candidates.loc[idx_calls]
    call_exits = calls[calls["optionroot"].isin(straddle_call_enter["optionroot"])]
    straddle_call_exit = dte_filter(call_exits, exit_dte)

    puts = data[data["type"] == "put"]
    put_candidates = dte_filter(puts, entry_dte, tolerance)
    put_candidates = put_candidates.copy()
    put_candidates["difference"] = np.abs(
        put_candidates["strike"] - put_candidates["underlying_last"]
    )
    idx_puts = put_candidates.groupby("quotedate")["difference"].idxmin()
    straddle_put_enter = put_candidates.loc[idx_puts]
    put_exits = puts[puts["optionroot"].isin(straddle_put_enter["optionroot"])]
    straddle_put_exit = dte_filter(put_exits, exit_dte)

    index = pd.Index(straddle_call_enter["quotedate"], name="date")
    results = pd.DataFrame(
        {
            "call": straddle_call_enter["optionroot"].array,
            "call_enter": straddle_call_enter["ask"].array * 100 * qty,
            "put": straddle_put_enter["optionroot"].array,
            "put_enter": straddle_put_enter["ask"].array * 100 * qty,
        },
        index=index,
    )
    results["call_exit"] = results["call"].map(
        lambda opt: exit_price_long(straddle_call_exit, opt)
    ) * 100 * qty
    results["put_exit"] = results["put"].map(
        lambda opt: exit_price_long(straddle_put_exit, opt)
    ) * 100 * qty
    results["profit"] = (
        results["call_exit"] - results["call_enter"]
        + results["put_exit"] - results["put_enter"]
    )
    results["roi"] = (
        (results["call_exit"] + results["put_exit"])
        / (results["call_enter"] + results["put_enter"])
        - 1.0
    )
    results["win/loss"] = results["profit"].ge(0).map({True: "win", False: "loss"}).astype("category")
    results["total"] = results["profit"].cumsum()
    return results


# ── Iron butterfly ─────────────────────────────────────────────────────

def otm_call_filter(data, otm_pct, tolerance=0.0):
    upper = otm_pct * (1 + tolerance)
    lower = otm_pct * (1 - tolerance)
    return data.query(
        "(strike - underlying_last >= underlying_last * @lower) & "
        "(strike - underlying_last <= underlying_last * @upper) & "
        "ask > 0.0"
    )


def otm_put_filter(data, otm_pct, tolerance=0.0):
    upper = otm_pct * (1 + tolerance)
    lower = otm_pct * (1 - tolerance)
    return data.query(
        "(underlying_last - strike >= underlying_last * @lower) & "
        "(underlying_last - strike <= underlying_last * @upper) & "
        "ask > 0.0"
    )


def iron_butterfly(data, otm_pct=0.15, otm_tolerance=0.1, entry_dte=30, exit_dte=2, dte_tolerance=0.1, qty=1):
    calls = data.query("type=='call'")
    call_candidates = dte_filter(calls, entry_dte, dte_tolerance)
    otm_calls = otm_call_filter(call_candidates, otm_pct, otm_tolerance)
    otm_calls = otm_calls.groupby("quotedate").first().reset_index()

    puts = data.query("type=='put'")
    put_candidates = dte_filter(puts, entry_dte, dte_tolerance)
    otm_puts = otm_put_filter(put_candidates, otm_pct, otm_tolerance)
    otm_puts = otm_puts.groupby("quotedate").first().reset_index()

    valid_dates = otm_calls[otm_calls["quotedate"].isin(otm_puts["quotedate"])]["quotedate"]
    otm_calls = otm_calls[otm_calls["quotedate"].isin(valid_dates)]
    otm_puts = otm_puts[otm_puts["quotedate"].isin(valid_dates)]

    call_dates = calls[calls["quotedate"].isin(valid_dates)].copy()
    call_dates["difference"] = np.abs(call_dates["strike"] - call_dates["underlying_last"])
    idx_sc = call_dates.groupby("quotedate")["difference"].idxmin()
    short_calls = call_dates.loc[idx_sc]

    call_exits = dte_filter(calls, exit_dte)
    short_call_exits = short_calls["optionroot"].map(
        lambda opt: exit_price_dir(call_exits, opt, "short")
    )
    otm_call_exits = otm_calls["optionroot"].map(
        lambda opt: exit_price_dir(call_exits, opt, "long")
    )

    put_dates = puts[puts["quotedate"].isin(valid_dates)].copy()
    put_dates["difference"] = np.abs(put_dates["strike"] - put_dates["underlying_last"])
    idx_sp = put_dates.groupby("quotedate")["difference"].idxmin()
    short_puts = put_dates.loc[idx_sp]

    put_exits = dte_filter(puts, exit_dte)
    short_put_exits = short_puts["optionroot"].map(
        lambda opt: exit_price_dir(put_exits, opt, "short")
    )
    otm_put_exits = otm_puts["optionroot"].map(
        lambda opt: exit_price_dir(put_exits, opt, "long")
    )

    index = pd.Index(short_calls["quotedate"], name="date")
    results = pd.DataFrame(
        {
            "short_call_enter": short_calls["bid"].array * 100 * qty,
            "short_call_exit": short_call_exits.array * 100 * qty,
            "long_call_enter": otm_calls["ask"].array * 100 * qty,
            "long_call_exit": otm_call_exits.array * 100 * qty,
            "short_put_enter": short_puts["bid"].array * 100 * qty,
            "short_put_exit": short_put_exits.array * 100 * qty,
            "long_put_enter": otm_puts["ask"].array * 100 * qty,
            "long_put_exit": otm_put_exits.array * 100 * qty,
        },
        index=index,
    )
    results["profit"] = results.eval(
        "short_call_enter + short_put_enter + long_call_exit + long_put_exit "
        "- short_call_exit - short_put_exit - long_call_enter - long_put_enter"
    )
    results["roi"] = results.eval(
        "profit / (short_call_exit + short_put_exit + long_call_enter + long_put_enter)"
    )
    results["win/loss"] = results["profit"].ge(0).map({True: "win", False: "loss"}).astype("category")
    results["total"] = results["profit"].cumsum()
    return results


# ── Plotting ───────────────────────────────────────────────────────────

def plot_straddle_results(results, label):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    sns.scatterplot(x=results.index, y="roi", hue="win/loss", data=results, ax=ax1)
    ax1.set_title(f"Straddle ROI — {label}")
    ax1.tick_params(axis="x", rotation=45)

    ax2.plot(results.index, results["total"], color=FT_BLUE)
    ax2.set_title(f"Cumulative P&L — {label}")
    ax2.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    safe = label.replace(" ", "_").lower()
    savefig(fig, os.path.join(CHARTS, f"straddle_{safe}.png"))


def plot_iron_butterfly_results(results, label):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    sns.scatterplot(x=results.index, y="profit", hue="win/loss", data=results, ax=ax1)
    ax1.set_title(f"Iron butterfly profit — {label}")
    ax1.tick_params(axis="x", rotation=45)

    sns.scatterplot(x=results.index, y="roi", hue="win/loss", data=results, ax=ax2)
    ax2.set_title(f"Iron butterfly ROI — {label}")
    ax2.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    safe = label.replace(" ", "_").lower()
    savefig(fig, os.path.join(CHARTS, f"iron_butterfly_{safe}.png"))


# ── Main ───────────────────────────────────────────────────────────────

def main():
    print("Options Strategies (straddle + iron butterfly)")
    print("=" * 50)

    # Try loading sample SPX 2010 data
    spx_path = os.path.join(DATA, "SPX_2010.csv")
    if not os.path.exists(spx_path):
        print(f"  {spx_path} not found.")
        print("  This analysis requires SPX options data (private HDF5 dataset).")
        print("  Place SPX_2010.csv in data/ to run the sample analysis.")
        return

    spx_data = pd.read_csv(spx_path, parse_dates=["quotedate", "expiration"])

    # Straddle on 2010 data
    results = straddle(spx_data, tolerance=0)
    print(f"  Straddle trades: {len(results)}")
    print(f"  Win/Loss: {results['win/loss'].value_counts().to_dict()}")
    plot_straddle_results(results, "SPX 2010")

    # Straddle with different DTEs
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.set_xlim([pd.Timestamp(2010, 1, 1), pd.Timestamp(2010, 12, 31)])
    for entry_dte in range(36, 71, 6):
        r = straddle(spx_data, entry_dte=entry_dte, tolerance=0)
        sns.scatterplot(x=r.index, y="roi", data=r, ax=ax, label=str(entry_dte))
    ax.set_title("Straddle ROI by entry DTE — SPX 2010")
    savefig(fig, os.path.join(CHARTS, "straddle_dte_comparison.png"))

    # Iron butterfly on 2010
    ib_results = iron_butterfly(spx_data)
    print(f"  Iron butterfly trades: {len(ib_results)}")
    plot_iron_butterfly_results(ib_results, "SPX 2010")

    print("Done.")


if __name__ == "__main__":
    main()
