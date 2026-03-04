#!/usr/bin/env python3
"""Emergence of cooperation in evolutionary systems.

Based on Peters & Adamou, "An evolutionary advantage of cooperation"
(arXiv:1506.03414).

Demonstrates that cooperating entities grow faster than non-cooperators
in the time-average sense, even though ensemble averages are identical.
Animations from the original notebook are replaced with static composite
figures showing key time slices.
"""

import os
import sys

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts"))

from style import apply_style, savefig, FT_BLUE, FT_RED, FT_GREEN, FT_DARK, FT_PINK, FT_TEAL

CHARTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
os.makedirs(CHARTS, exist_ok=True)

apply_style()
np.random.seed(5)


# ── Parameters ─────────────────────────────────────────────────────────

MU = 0.15
SIGMA = np.sqrt(0.2)
T = 10_000
DT = 0.1
SDT = np.sqrt(DT)


# ── Cooperation vs non-cooperation (paper Fig. 2) ─────────────────────

def plot_growth_comparison():
    """Reproduce Fig. 2 from Peters & Adamou."""
    t = np.arange(0, (T + 1) * DT, DT)

    # Analytical slopes
    expectation = np.exp(MU * t)
    g_individual = np.exp((MU - SIGMA**2 / 2) * t)
    g_coop = np.exp((MU - SIGMA**2 / 4) * t)

    # Simulate individual 1
    noise_1 = np.random.normal(loc=1 + MU * DT, scale=SIGMA * SDT, size=T)
    wealth_1 = np.cumprod(noise_1)
    wealth_1 = np.insert(wealth_1, 0, 1)

    # Simulate individual 2
    noise_2 = np.random.normal(loc=1 + MU * DT, scale=SIGMA * SDT, size=T)
    wealth_2 = np.cumprod(noise_2)
    wealth_2 = np.insert(wealth_2, 0, 1)

    # Cooperating wealth
    noise_co = (noise_1 + noise_2) / 2
    wealth_co = np.cumprod(noise_co)
    wealth_co = np.insert(wealth_co, 0, 1)

    wealth_ave = (wealth_1 + wealth_2) / 2

    fig, ax = plt.subplots()
    ax.plot(t, expectation, "m--", label=r"slope $g(\langle x \rangle)$")
    ax.plot(t, g_coop, "--", color=FT_BLUE, label=r"slope $\bar{g}(y^{(2)})$")
    ax.plot(t, g_individual, "--", color=FT_GREEN, label=r"slope $\bar{g}(x_i)$")
    ax.plot(t, wealth_co, color=FT_BLUE, linewidth=2, label=r"$y^{(2)}(t)/2$")
    ax.plot(t, wealth_1, color="#00aa00", linewidth=2, label=r"$x_1(t)$")
    ax.plot(t, wealth_2, color="#55bb55", linewidth=2, label=r"$x_2(t)$")
    ax.plot(t, wealth_ave, "k-", linewidth=0.8, label=r"$(x_1+x_2)/2$")
    ax.set_yscale("log")
    ax.legend(fontsize=9)
    ax.set_xlabel("Time $t$")
    ax.set_ylabel("Biomass")
    ax.set_title("Cooperation vs non-cooperation (N=2)")
    savefig(fig, os.path.join(CHARTS, "cooperation_vs_individual.png"))


# ── Biomass bar chart (static composite replacing animation) ───────────

def increase_biomass(initial_biomasses, steps):
    """Simulate growth for cooperators and non-cooperators."""
    mu, sigma, dt, sdt = MU, SIGMA, 1, 1.0
    N = len(initial_biomasses)
    non_coop = initial_biomasses.copy()
    coop = initial_biomasses.copy()

    non_coop_history = [non_coop.sum()]
    coop_history = [coop.sum()]

    for _ in range(steps):
        xi = np.random.normal(size=N)
        non_coop = non_coop + non_coop * (mu * dt + sigma * xi * sdt)
        delta_y = np.sum(coop * (mu * dt + sigma * xi * sdt)) / N
        coop = coop + delta_y
        non_coop_history.append(non_coop.sum())
        coop_history.append(coop.sum())

    return np.array(non_coop_history), np.array(coop_history)


def plot_biomass_snapshots():
    """Static 2x2 bar chart at key time slices (replaces animation)."""
    time_slices = [0, 50, 150, 299]
    populations = [2, 3, 4, 5]
    initial_biomass = 10.0
    total_steps = 300

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    for idx, N in enumerate(populations):
        ax = axes[idx // 2, idx % 2]
        initial = np.full(N, initial_biomass, dtype=np.float64)
        non_coop_hist, coop_hist = increase_biomass(initial, total_steps)

        t_vals = np.arange(total_steps + 1)
        ax.plot(t_vals, non_coop_hist, color=FT_GREEN, label=r"$\sum x_i(t)$", linewidth=2)
        ax.plot(t_vals, coop_hist, color=FT_RED, label=r"$\sum y_i(t)$", linewidth=2)
        ax.set_yscale("log")
        ax.set_title(f"N = {N}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Total biomass")
        ax.legend(fontsize=9)

    fig.suptitle("Total biomass: non-cooperators vs cooperators", fontsize=14)
    fig.tight_layout()
    savefig(fig, os.path.join(CHARTS, "biomass_growth.png"))


# ── Main ───────────────────────────────────────────────────────────────

def main():
    print("Cooperation and Ergodicity")
    print("=" * 40)
    plot_growth_comparison()
    plot_biomass_snapshots()
    print("Done.")


if __name__ == "__main__":
    main()
