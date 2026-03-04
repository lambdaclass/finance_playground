#!/usr/bin/env python3
"""Ergodicity explorations: non-ergodic dynamics and insurance contracts.

Based on:
- Peters & Adamou, "Insurance makes wealth grow faster" (arXiv:1507.04655)
- Peters, "Ergodicity Economics" lecture notes
- Peters & Gell-Mann, "Evaluating gambles using dynamics"

Demonstrates that a positive-EV multiplicative gamble drives wealth to zero
over time, and that insurance contracts benefit *both* parties when evaluated
under the time-average (growth-rate) paradigm.
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
np.random.seed(123456789)


# ── Multiplicative gamble ──────────────────────────────────────────────

def generate_factors(steps=100):
    """Heads => 1.6, Tails => 0.5."""
    draws = np.random.rand(steps)
    factors = np.where(draws > 0.5, 1.6, 0.5)
    factors[0] = 1
    return factors


def wealth_over_time(factors, initial_wealth):
    return factors.cumprod() * initial_wealth


def plot_single_trajectory():
    factors = generate_factors(100)
    wealth = wealth_over_time(factors, 1000)

    fig, ax = plt.subplots()
    ax.plot(wealth, color=FT_BLUE)
    ax.set_title("Wealth over time — single realisation")
    ax.set_xlabel("t")
    ax.set_ylabel("x(t)")
    savefig(fig, os.path.join(CHARTS, "single_trajectory.png"))


def plot_multiple_trajectories():
    fig, ax = plt.subplots()
    for _ in range(20):
        factors = generate_factors(100)
        ax.plot(wealth_over_time(factors, 1000), alpha=0.6)
    ax.set_title("Wealth over time — 20 realisations")
    ax.set_xlabel("t")
    ax.set_ylabel("x(t)")
    savefig(fig, os.path.join(CHARTS, "multiple_trajectories.png"))


# ── Insurance contract ─────────────────────────────────────────────────

W_MER = 100_000
W_INS = 1_000_000
G = 4_000
C = 30_000
L = G + C
P_LOSS = 0.05


def _plot_deltas(delta_mer_fn, delta_ins_fn, fee, title, ylabel, ylim):
    fees = np.linspace(1500, 2000, num=500)
    fig, ax = plt.subplots()
    ax.plot(fees, delta_mer_fn(fees), label="Merchant", color=FT_BLUE)
    ax.plot(fees, delta_ins_fn(fees), label="Insurer", color=FT_RED)
    ax.axhline(0, color=FT_DARK, linewidth=0.8)
    ax.axvline(fee, linestyle="--", color=FT_GREEN, label=f"Fee = ${fee}")

    for fn, offset in [(delta_mer_fn, 0.005), (delta_ins_fn, -0.008)]:
        y = fn(fee)
        ax.plot(fee, y, "kX", markersize=8)
        ax.annotate(f"{y:.3f}", (fee + 5, y + offset))

    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Insurance fee ($)")
    ax.set_ylim(*ylim)
    ax.legend()
    return fig


def plot_linear_utility():
    delta_mer = lambda f: P_LOSS * L - f
    delta_ins = lambda f: f - P_LOSS * L
    fig = _plot_deltas(
        delta_mer, delta_ins, 1800,
        "Change in rate — linear utility",
        r"$\delta \langle r \rangle$",
        (-150, 150),
    )
    savefig(fig, os.path.join(CHARTS, "insurance_linear.png"))


def plot_sqrt_utility():
    def delta_mer(fee):
        r_un = (1 - P_LOSS) * np.sqrt(W_MER + G) + P_LOSS * np.sqrt(W_MER - C) - np.sqrt(W_MER)
        r_in = np.sqrt(W_MER + G - fee) - np.sqrt(W_MER)
        return r_in - r_un

    def delta_ins(fee):
        r_in = (1 - P_LOSS) * np.sqrt(W_INS + fee) + P_LOSS * np.sqrt(W_INS + fee - L) - np.sqrt(W_INS)
        return r_in

    fig = _plot_deltas(
        delta_mer, delta_ins, 1800,
        "Change in rate — square root utility",
        r"$\delta \langle r_u \rangle$",
        (-0.1, 0.2),
    )
    savefig(fig, os.path.join(CHARTS, "insurance_sqrt_utility.png"))


def plot_growth_rate():
    def delta_g_mer(fee):
        g_un = (1 - P_LOSS) * np.log(W_MER + G) + P_LOSS * np.log(W_MER - C) - np.log(W_MER)
        g_in = np.log(W_MER + G - fee) - np.log(W_MER)
        return (g_in - g_un) * 100

    def delta_g_ins(fee):
        g_in = (1 - P_LOSS) * np.log((W_INS + fee) / W_INS) + P_LOSS * np.log((W_INS + fee - L) / W_INS)
        return g_in * 100

    fig = _plot_deltas(
        delta_g_mer, delta_g_ins, 1800,
        "Change in growth rate g",
        r"$\delta g$ (% change in wealth)",
        (-0.05, 0.3),
    )
    savefig(fig, os.path.join(CHARTS, "insurance_growth_rate.png"))


# ── Main ───────────────────────────────────────────────────────────────

def main():
    print("Ergodicity & Insurance explorations")
    print("=" * 40)
    plot_single_trajectory()
    plot_multiple_trajectories()
    plot_linear_utility()
    plot_sqrt_utility()
    plot_growth_rate()
    print("Done.")


if __name__ == "__main__":
    main()
