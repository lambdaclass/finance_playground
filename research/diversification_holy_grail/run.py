#!/usr/bin/env python3
"""Ray Dalio's Holy Grail of Investing — diversification and correlation.

Shows that combining uncorrelated return streams dramatically reduces
portfolio risk, while highly correlated streams offer diminishing benefits
beyond 3-4 assets. Original notebook used Altair; rewritten as matplotlib.
"""

import os
import sys

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts"))

from style import apply_style, savefig, PALETTE, FT_BLUE, FT_RED

CHARTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
os.makedirs(CHARTS, exist_ok=True)

apply_style()
np.random.seed(42)


# ── Simulation ─────────────────────────────────────────────────────────

def correlated_streams(n, mean, risk, corr):
    """Generate n return streams with given mean, risk, and average correlation."""
    num_samples = 10_000
    means = np.full(n, mean)
    corr_mat = np.full((n, n), corr, dtype=np.float64)
    np.fill_diagonal(corr_mat, 1.0)
    cov_mat = corr_mat * risk**2
    streams = np.random.multivariate_normal(means, cov_mat, size=num_samples)
    return streams.T


def aggregate_risk(return_streams, n):
    """Pooled risk (std) of the first n streams."""
    aggregate_returns = np.sum(return_streams[:n], axis=0) / n
    return aggregate_returns.std()


def build_simulated_data():
    max_assets = 20
    assets = range(1, max_assets + 1)
    mean = 10
    risk_levels = range(1, 15)
    correlations = np.arange(0.0, 0.8, 0.1)

    index = pd.MultiIndex.from_product(
        [risk_levels, assets], names=["risk_level", "num_assets"]
    )
    data = pd.DataFrame(index=index)

    for risk in risk_levels:
        for corr in correlations:
            streams = correlated_streams(max_assets, mean, risk, corr)
            risk_level = np.array([aggregate_risk(streams, n) for n in assets])
            data.loc[(risk,), round(corr, 1)] = risk_level

    data.columns.names = ["correlation"]
    return data


# ── Plotting (matplotlib replacing Altair) ─────────────────────────────

CORR_COLORS = {
    0.0: "#1b9e77",
    0.1: "#d95f02",
    0.2: "#7570b3",
    0.3: "#e7298a",
    0.4: "#66a61e",
    0.5: "#e6ab02",
    0.6: "#a6761d",
    0.7: "#666666",
}


def plot_risk_level(data, risk_level, ax=None):
    subset = data.query("risk_level == @risk_level")

    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure

    for corr in subset.columns:
        values = subset[corr].values
        color = CORR_COLORS.get(float(corr), "#333333")
        ax.plot(range(1, len(values) + 1), values, label=f"{corr}", color=color, linewidth=1.5)

    ax.set_xlabel("Number of assets")
    ax.set_ylabel("Risk %")
    ax.set_title(f"Risk % by number of assets (risk level = {risk_level}%)")
    ax.legend(title="Correlation", fontsize=8, title_fontsize=9)
    return fig, ax


def main():
    print("Diversification — Holy Grail")
    print("=" * 40)

    data = build_simulated_data()

    # Risk level 10%
    fig, ax = plt.subplots()
    plot_risk_level(data, 10, ax=ax)
    savefig(fig, os.path.join(CHARTS, "holy_grail_risk10.png"))

    # Risk level 7%
    fig, ax = plt.subplots()
    plot_risk_level(data, 7, ax=ax)
    savefig(fig, os.path.join(CHARTS, "holy_grail_risk7.png"))

    # Combined view
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
    plot_risk_level(data, 10, ax=ax1)
    plot_risk_level(data, 7, ax=ax2)
    fig.suptitle("Ray Dalio's Holy Grail: diversification reduces risk", fontsize=14)
    fig.tight_layout()
    savefig(fig, os.path.join(CHARTS, "holy_grail_combined.png"))

    print("Done.")


if __name__ == "__main__":
    main()
