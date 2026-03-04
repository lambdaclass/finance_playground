#!/usr/bin/env python3
"""Re-allocating GBM (RGBM) wealth distribution model.

Based on Adamou, Berman & Peters (2019), "Wealth Inequality and the
Ergodic Hypothesis: Evidence from the United States".

Simulates wealth trajectories where individuals grow via GBM and
redistribute a fraction tau of their wealth each period.

The ipywidgets slider from the original notebook is replaced by a
``--tau`` CLI argument.
"""

import argparse
import os
import sys

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts"))

from style import apply_style, savefig, FT_BLUE, FT_RED, FT_GREEN, PALETTE

CHARTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
os.makedirs(CHARTS, exist_ok=True)

apply_style()


# ── Simulation ─────────────────────────────────────────────────────────

def generate_wealth_trajectories(tau=0.01):
    np.random.seed(42)
    N = 100
    T = 100
    dt = 0.1
    mu = 0.08
    sigma = 0.08
    time_steps = int(T / dt)
    sdt = np.sqrt(dt)

    x = np.zeros((time_steps, N))
    x[0, :] = 1

    xi = np.random.normal(loc=0, scale=1, size=(time_steps, N))

    for t in range(1, time_steps):
        x[t] = (
            x[t - 1] * (1 + mu * dt + sigma * xi[t] * sdt)
            - tau * (x[t - 1] - np.mean(x[t - 1])) * dt
        )

    return pd.DataFrame(x)


# ── Plotting (static composites replacing animation) ───────────────────

def plot_snapshots(tau):
    """Show wealth distribution at key time slices."""
    trajectories = generate_wealth_trajectories(tau)
    N = trajectories.shape[1]
    step_size = 10

    # Pick 6 evenly spaced time slices
    frames = [0, 20, 40, 60, 80, 99]
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    for ax, frame in zip(axes.flat, frames):
        i_day = frame * step_size
        year = i_day // 10 + 1
        values = trajectories.iloc[i_day].values
        colors = [FT_BLUE if v >= 1 else FT_RED for v in values]
        ax.bar(range(N), values, color=colors, width=1.0)
        ax.set_title(f"Year {year}")
        ax.set_xlabel("Individual")
        ax.set_ylabel("Wealth")

    fig.suptitle(f"RGBM wealth distribution (tau = {tau:.2f})", fontsize=14)
    fig.tight_layout()
    savefig(fig, os.path.join(CHARTS, f"rgbm_tau_{tau:.2f}.png"))


def plot_tau_comparison():
    """Compare final wealth distributions for different tau values."""
    taus = [-0.5, 0.0, 0.01, 0.1, 0.5, 1.0]
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    for ax, tau in zip(axes.flat, taus):
        trajectories = generate_wealth_trajectories(tau)
        final = trajectories.iloc[-1].sort_values(ascending=False).values
        colors = [FT_BLUE if v >= 1 else FT_RED for v in final]
        ax.bar(range(len(final)), final, color=colors, width=1.0)
        ax.set_title(f"tau = {tau:.2f}")
        ax.set_xlabel("Individual (ranked)")
        ax.set_ylabel("Final wealth")

    fig.suptitle("Final wealth distributions for various tau", fontsize=14)
    fig.tight_layout()
    savefig(fig, os.path.join(CHARTS, "rgbm_tau_comparison.png"))


# ── Main ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="RGBM wealth redistribution simulation")
    parser.add_argument("--tau", type=float, default=0.01, help="Redistribution parameter (default: 0.01)")
    args = parser.parse_args()

    print("RGBM Wealth Redistribution")
    print("=" * 40)
    plot_snapshots(args.tau)
    plot_tau_comparison()
    print("Done.")


if __name__ == "__main__":
    main()
