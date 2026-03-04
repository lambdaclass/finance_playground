#!/usr/bin/env python3
"""Evaluating gambles: expected values, time averages, and Kelly criterion.

Explores:
1. Expected value as an ensemble average
2. The St. Petersburg paradox and utility functions
3. Non-ergodic multiplicative dynamics
4. Kelly criterion for optimal bet sizing
"""

import os
import sys

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts"))

from style import apply_style, savefig, FT_BLUE, FT_RED, FT_GREEN, FT_DARK

CHARTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
os.makedirs(CHARTS, exist_ok=True)

apply_style()
np.random.seed(42)


# ── Expected value convergence ─────────────────────────────────────────

def plot_ev_histogram():
    """Histogram of average payouts over many 1M-flip trials."""
    n = 1_000_000
    many_payouts = [
        np.where(np.random.rand(n) > 0.5, 3, -1).mean() for _ in range(1000)
    ]
    fig, ax = plt.subplots()
    ax.hist(many_payouts, bins=40, color=FT_BLUE, edgecolor="white")
    ax.axvline(1.0, color=FT_RED, linestyle="--", label="EV = $1")
    ax.set_title("Distribution of average payouts (n=1M per trial)")
    ax.set_xlabel("Average payout ($)")
    ax.set_ylabel("Frequency")
    ax.legend()
    savefig(fig, os.path.join(CHARTS, "ev_convergence.png"))


# ── Utility functions ──────────────────────────────────────────────────

def plot_utility_functions():
    points = np.linspace(0.0001, 50, num=300)
    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    ax1.plot(points, np.sqrt(points), color=FT_BLUE)
    ax1.set_title(r"$\sqrt{x}$")
    ax1.set_xlabel("Wealth")
    ax2.plot(points, np.log(points), color=FT_RED)
    ax2.set_title(r"$\ln{x}$")
    ax2.set_xlabel("Wealth")
    fig.suptitle("Common utility functions")
    savefig(fig, os.path.join(CHARTS, "utility_functions.png"))


# ── Non-ergodic multiplicative game ────────────────────────────────────

def play_game(initial_wealth, steps):
    draws = np.random.rand(steps)
    factors = np.where(draws > 0.5, 1.6, 0.5)
    factors[0] = 1
    return factors.cumprod() * initial_wealth


def plot_multiplicative_trajectories():
    fig, ax = plt.subplots()
    for _ in range(20):
        ax.plot(play_game(1000, 100), alpha=0.6)
    ax.set_title("Non-ergodic multiplicative game — 20 realisations")
    ax.set_xlabel("t")
    ax.set_ylabel("x(t)")
    savefig(fig, os.path.join(CHARTS, "multiplicative_trajectories.png"))


# ── Kelly criterion ────────────────────────────────────────────────────

def wealth_over_time_kelly(p, initial_wealth, t, stake):
    coin_flips = np.random.rand(t)
    factors = np.where(coin_flips > p, 1 - stake, 1 + stake)
    factors[0] = 1
    return factors.cumprod() * initial_wealth


def plot_kelly():
    p, q = 0.6, 0.4
    x_0 = 1000

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # g(f) curve
    fs = np.linspace(0, 1, endpoint=False, num=200)
    g_star = p * np.log(1 + fs) + q * np.log(1 - fs)
    axes[0, 0].plot(fs, g_star, color=FT_BLUE)
    axes[0, 0].axvline(p - q, linestyle="--", color=FT_RED, linewidth=1, label=f"f* = {p-q:.1f}")
    axes[0, 0].set_title("Growth rate g(f)")
    axes[0, 0].set_xlabel("Fraction f")
    axes[0, 0].set_ylabel("g(f)")
    axes[0, 0].legend()

    # Bet everything
    axes[0, 1].plot(wealth_over_time_kelly(p, x_0, 500, 1.0), color=FT_RED)
    axes[0, 1].set_title("f = 1.0 (bet everything)")
    axes[0, 1].set_ylabel("x(t)")

    # Bet minimum
    axes[1, 0].plot(wealth_over_time_kelly(p, x_0, 500, 0.001), color=FT_GREEN)
    axes[1, 0].set_title("f = 0.001 (tiny bets)")
    axes[1, 0].set_xlabel("t")
    axes[1, 0].set_ylabel("x(t)")

    # Kelly optimal
    wealth = wealth_over_time_kelly(p, x_0, 500, p - q)
    axes[1, 1].plot(wealth, color=FT_BLUE)
    axes[1, 1].set_title(f"f = {p-q:.1f} (Kelly optimal)")
    axes[1, 1].set_xlabel("t")
    axes[1, 1].set_ylabel("x(t)")
    axes[1, 1].ticklabel_format(style="plain")

    fig.suptitle("Kelly criterion: optimal bet sizing", fontsize=14)
    fig.tight_layout()
    savefig(fig, os.path.join(CHARTS, "kelly_criterion.png"))


# ── Main ───────────────────────────────────────────────────────────────

def main():
    print("Evaluating Gambles")
    print("=" * 40)
    plot_ev_histogram()
    plot_utility_functions()
    plot_multiplicative_trajectories()
    plot_kelly()
    print("Done.")


if __name__ == "__main__":
    main()
