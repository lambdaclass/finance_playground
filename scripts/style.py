"""Shared matplotlib styling for finance_playground.

FT-inspired warm palette for consistent, publication-quality charts.
Import and call ``apply_style()`` at the top of every run.py.
"""

import matplotlib
import matplotlib.pyplot as plt

# ── colour palette (FT-inspired) ──────────────────────────────────────
FT_BG = "#FFF1E5"
FT_DARK = "#33302E"
FT_BLUE = "#0D7680"
FT_RED = "#CC0000"
FT_GREEN = "#09814A"
FT_ORANGE = "#F2DFCE"
FT_TEAL = "#0F5499"
FT_PINK = "#C91D6B"
FT_GREY = "#A0998A"

PALETTE = [FT_BLUE, FT_RED, FT_GREEN, FT_TEAL, FT_PINK, FT_GREY, FT_DARK]


def apply_style():
    """Apply project-wide matplotlib style."""
    plt.rcParams.update(
        {
            "figure.figsize": (14, 7),
            "figure.facecolor": FT_BG,
            "axes.facecolor": FT_BG,
            "axes.edgecolor": FT_GREY,
            "axes.labelcolor": FT_DARK,
            "axes.prop_cycle": plt.cycler(color=PALETTE),
            "axes.grid": True,
            "grid.color": FT_ORANGE,
            "grid.linewidth": 0.6,
            "text.color": FT_DARK,
            "xtick.color": FT_DARK,
            "ytick.color": FT_DARK,
            "font.family": "serif",
            "font.size": 12,
            "legend.frameon": False,
            "savefig.dpi": 150,
            "savefig.bbox": "tight",
            "savefig.facecolor": FT_BG,
        }
    )


def savefig(fig, path, **kwargs):
    """Save figure with project defaults."""
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=FT_BG, **kwargs)
    plt.close(fig)
    print(f"  saved {path}")
