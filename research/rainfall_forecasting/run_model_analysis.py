#!/usr/bin/env python3
"""Model analysis: comparing NCEP/NCAR reanalysis grid points with weather stations.

Computes Pearson correlations and mean percentage errors between grid-point
data and nearest weather stations, analyses the effect of distance, and
explores weighted multi-station correlations.

Based on the model_analysis.ipynb notebook from the 2020 Metadata competition.
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
from scipy.stats import pearsonr
import seaborn as sns

PROJECT_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts"))

from style import apply_style, savefig, FT_BLUE, FT_RED

CHARTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(CHARTS, exist_ok=True)

apply_style()


def load_all_data():
    stations_info = pd.read_excel(os.path.join(DATA, "Estaciones.xlsx"), sheet_name="INFO")
    stations_maxima = pd.read_excel(
        os.path.join(DATA, "Estaciones.xlsx"), sheet_name="Maximos", index_col=0, skiprows=1
    )
    stations_annual = pd.read_excel(
        os.path.join(DATA, "Estaciones.xlsx"), sheet_name="Anuales", index_col=0, skiprows=1
    )
    stations_np95 = pd.read_excel(
        os.path.join(DATA, "Estaciones.xlsx"), sheet_name="Np95", index_col=0, skiprows=1
    )

    reanalysis_info = pd.read_excel(os.path.join(DATA, "datos NCEP NCAR.xlsx"), sheet_name="INFO")
    reanalysis_info["LATITUD (°S)"] = reanalysis_info["LATITUD (°S)"].astype(np.float32)
    reanalysis_info["LONGITUD (°W)"] = reanalysis_info["LONGITUD (°W)"].astype(np.float32)
    reanalysis_info = reanalysis_info.set_index("INDICATIVO", drop=True)

    reanalysis_total = pd.read_excel(
        os.path.join(DATA, "datos NCEP NCAR.xlsx"), sheet_name="Total", index_col=0
    )
    reanalysis_maxima = pd.read_excel(
        os.path.join(DATA, "datos NCEP NCAR.xlsx"), sheet_name="Maximo", index_col=0
    )
    reanalysis_np95 = pd.read_excel(
        os.path.join(DATA, "datos NCEP NCAR.xlsx"), sheet_name="Np95", index_col=0
    )

    return (
        stations_info, stations_maxima, stations_annual, stations_np95,
        reanalysis_info, reanalysis_total, reanalysis_maxima, reanalysis_np95,
    )


def find_nearest_stations(reanalysis_info, stations_info):
    """Find nearest weather station for each grid point."""
    try:
        import geopy.distance
    except ImportError:
        print("  geopy not installed, skipping")
        return reanalysis_info

    station_coords = {}
    for _, row in stations_info.iterrows():
        lat, lon = row["LAT (S), LONG (W)(º)"].split(",")
        station_coords[row["Estacion"]] = (float(lat), float(lon))

    nearest = []
    distances = []
    for _, row in reanalysis_info.iterrows():
        coords1 = (row["LATITUD (°S)"], row["LONGITUD (°W)"])
        min_d, min_s = float("inf"), None
        for name, coords2 in station_coords.items():
            d = geopy.distance.geodesic(coords1, coords2).km
            if d < min_d:
                min_d, min_s = d, name
        nearest.append(min_s)
        distances.append(min_d)

    reanalysis_info["nearest_station"] = nearest
    reanalysis_info["distance"] = distances
    return reanalysis_info


def group_by_station(station_data, grid_data, reanalysis_info):
    grouped = {}
    for station in reanalysis_info["nearest_station"].unique():
        if station not in station_data.columns:
            continue
        df = pd.DataFrame(station_data[station])
        for idx, row in reanalysis_info.iterrows():
            if row["nearest_station"] == station and idx in grid_data.columns:
                df = df.join(pd.DataFrame(grid_data[idx]))
        grouped[station] = df
    return grouped


def compute_pearsons(grouped):
    p = {}
    for station, df in grouped.items():
        for col in df.columns:
            if col != station:
                combined = df[[station, col]].dropna()
                if len(combined) >= 10:
                    r, _ = pearsonr(combined[station], combined[col])
                    p[col] = r
    return p


def compute_mean_errors(grouped):
    errors = {}
    for station, df in grouped.items():
        clean = df.dropna()
        if len(clean) == 0:
            continue
        for col in clean.columns[1:]:
            pct_err = ((clean[col] - clean.iloc[:, 0]).abs() / clean.iloc[:, 0]).replace(
                [np.inf, -np.inf], np.nan
            ).dropna()
            if len(pct_err) > 0:
                errors[col] = pct_err.mean()
    return errors


def plot_scatter(x, y, title, xlabel, ylabel, filename):
    fig, ax = plt.subplots()
    ax.scatter(x, y, color=FT_BLUE, alpha=0.7)
    ax.set_title(title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    savefig(fig, os.path.join(CHARTS, filename))


def main():
    print("  Loading data...")
    (
        stations_info, stations_maxima, stations_annual, stations_np95,
        reanalysis_info, reanalysis_total, reanalysis_maxima, reanalysis_np95,
    ) = load_all_data()

    reanalysis_info = find_nearest_stations(reanalysis_info, stations_info)
    if "nearest_station" not in reanalysis_info.columns:
        return

    # Group by station
    df_max = group_by_station(stations_maxima, reanalysis_maxima, reanalysis_info)
    df_annual = group_by_station(stations_annual, reanalysis_total, reanalysis_info)
    df_np95 = group_by_station(stations_np95, reanalysis_np95, reanalysis_info)

    # Pearson correlations
    for name, grouped in [("max", df_max), ("annual", df_annual), ("np95", df_np95)]:
        pearsons = compute_pearsons(grouped)
        if not pearsons:
            continue

        # Histogram
        fig, ax = plt.subplots()
        ax.hist(list(pearsons.values()), bins=10, color=FT_RED, alpha=0.6, edgecolor="white")
        ax.set_title(f"Pearson coefficients — {name} data")
        savefig(fig, os.path.join(CHARTS, f"analysis_pearson_hist_{name}.png"))

        # vs distance
        dists = [reanalysis_info.loc[k, "distance"] for k in pearsons if k in reanalysis_info.index]
        vals = [pearsons[k] for k in pearsons if k in reanalysis_info.index]
        plot_scatter(
            dists, vals,
            f"Pearson r vs distance — {name}", "Distance (km)", "Pearson r",
            f"analysis_pearson_vs_dist_{name}.png",
        )

    # Mean percentage errors
    for name, grouped in [("max", df_max), ("annual", df_annual), ("np95", df_np95)]:
        errors = compute_mean_errors(grouped)
        if not errors:
            continue
        dists = [reanalysis_info.loc[k, "distance"] for k in errors if k in reanalysis_info.index]
        vals = [errors[k] for k in errors if k in reanalysis_info.index]
        plot_scatter(
            dists, vals,
            f"Mean % error vs distance — {name}", "Distance (km)", "Mean % error",
            f"analysis_error_vs_dist_{name}.png",
        )

    print("  Model analysis done.")


if __name__ == "__main__":
    main()
