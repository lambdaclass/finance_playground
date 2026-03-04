#!/usr/bin/env python3
"""Rain forecast data exploration.

Loads weather station and NCEP/NCAR reanalysis data, computes correlations
between station observations and model grid points, and visualises the
relationship between Pearson coefficients and distance.

Based on the rain-forecast.ipynb notebook from the 2020 Metadata competition.
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
np.random.seed(42)


def load_stations():
    info = pd.read_excel(os.path.join(DATA, "Estaciones.xlsx"), sheet_name="INFO")
    maxima = pd.read_excel(
        os.path.join(DATA, "Estaciones.xlsx"), sheet_name="Maximos", header=1, parse_dates=["Año hid"]
    )
    annual = pd.read_excel(
        os.path.join(DATA, "Estaciones.xlsx"), sheet_name="Anuales", index_col=0, skiprows=1
    )
    np95 = pd.read_excel(
        os.path.join(DATA, "Estaciones.xlsx"), sheet_name="Np95", index_col=0, skiprows=1
    )
    return info, maxima, annual, np95


def load_reanalysis():
    info = pd.read_excel(os.path.join(DATA, "datos NCEP NCAR.xlsx"), sheet_name="INFO")
    info["LATITUD (°S)"] = info["LATITUD (°S)"].astype(np.float32)
    info["LONGITUD (°W)"] = info["LONGITUD (°W)"].astype(np.float32)
    info = info.set_index("INDICATIVO", drop=True)

    total = pd.read_excel(os.path.join(DATA, "datos NCEP NCAR.xlsx"), sheet_name="Total", index_col=0)
    maxima = pd.read_excel(os.path.join(DATA, "datos NCEP NCAR.xlsx"), sheet_name="Maximo", index_col=0)
    np95 = pd.read_excel(os.path.join(DATA, "datos NCEP NCAR.xlsx"), sheet_name="Np95", index_col=0)
    return info, total, maxima, np95


def compute_pearson(df_stations, df_reanalysis, station_names, reanalysis_info):
    """Compute Pearson correlation between nearest station and grid point."""
    correlations = {}

    for v_name in df_reanalysis.columns:
        nearest = reanalysis_info.loc[v_name, "nearest_station"] if "nearest_station" in reanalysis_info.columns else None
        if nearest is None or nearest not in df_stations.columns:
            continue
        combined = pd.DataFrame({"station": df_stations[nearest], "grid": df_reanalysis[v_name]}).dropna()
        if len(combined) >= 10:
            r, _ = pearsonr(combined["station"], combined["grid"])
            correlations[v_name] = r

    return correlations


def plot_target_series(maxima):
    """Plot the San Luis Tucuman maximum rainfall series."""
    fig, ax = plt.subplots()
    series = maxima["San Luis Tucuman"].dropna()
    ax.plot(series.values, color=FT_BLUE)
    ax.set_title("San Luis Tucuman — yearly maximum daily rainfall")
    ax.set_xlabel("Year index")
    ax.set_ylabel("Rainfall (mm)")
    savefig(fig, os.path.join(CHARTS, "target_series.png"))


def plot_station_vs_model(df_grouped, variable_name):
    """Plot stations vs their nearest grid points."""
    stations = list(df_grouped.keys())[:8]
    if not stations:
        return

    n = min(len(stations), 8)
    rows = (n + 1) // 2
    fig, axes = plt.subplots(rows, 2, figsize=(16, 4 * rows))
    axes = axes.flat if n > 2 else [axes] if n == 1 else axes.flat

    for ax, station in zip(axes, stations):
        df_grouped[station].plot(ax=ax)
        ax.set_title(station, fontsize=10)

    fig.suptitle(f"{variable_name} — stations vs grid points", fontsize=14)
    fig.tight_layout()
    safe = variable_name.replace(" ", "_").lower()
    savefig(fig, os.path.join(CHARTS, f"station_vs_model_{safe}.png"))


def main():
    print("  Loading data...")
    stations_info, stations_maxima, stations_annual, stations_np95 = load_stations()
    reanalysis_info, reanalysis_total, reanalysis_maxima, reanalysis_np95 = load_reanalysis()

    # Target series
    plot_target_series(stations_maxima)

    # Find nearest station for each grid point
    try:
        import geopy.distance

        station_coords = {}
        for _, row in stations_info.iterrows():
            lat, lon = row["LAT (S), LONG (W)(º)"].split(",")
            station_coords[row["Estacion"]] = (float(lat), float(lon))

        nearest_stations = []
        nearest_distances = []
        for idx, row in reanalysis_info.iterrows():
            coords1 = (row["LATITUD (°S)"], row["LONGITUD (°W)"])
            min_dist = float("inf")
            min_station = None
            for name, coords2 in station_coords.items():
                d = geopy.distance.geodesic(coords1, coords2).km
                if d < min_dist:
                    min_dist = d
                    min_station = name
            nearest_stations.append(min_station)
            nearest_distances.append(min_dist)

        reanalysis_info["nearest_station"] = nearest_stations
        reanalysis_info["distance"] = nearest_distances
        print(f"  Computed nearest stations for {len(reanalysis_info)} grid points")
    except ImportError:
        print("  geopy not installed, skipping distance calculations")
        return

    # Group grid points by nearest station
    stations_unique = reanalysis_info["nearest_station"].unique()

    def group_by_station(station_data, grid_data):
        grouped = {}
        for station in stations_unique:
            if station not in station_data.columns:
                continue
            df = pd.DataFrame(station_data[station])
            for idx, row in reanalysis_info.iterrows():
                if row["nearest_station"] == station and idx in grid_data.columns:
                    df = df.join(pd.DataFrame(grid_data[idx]))
            grouped[station] = df
        return grouped

    df_max = group_by_station(
        pd.read_excel(os.path.join(DATA, "Estaciones.xlsx"), sheet_name="Maximos", index_col=0, skiprows=1),
        reanalysis_maxima,
    )
    df_annual = group_by_station(stations_annual, reanalysis_total)
    df_np95 = group_by_station(stations_np95, reanalysis_np95)

    plot_station_vs_model(df_max, "Yearly maximum daily rainfall")
    plot_station_vs_model(df_annual, "Total annual rainfall")
    plot_station_vs_model(df_np95, "NP95")

    # Pearson correlations
    def compute_all_pearsons(grouped_data):
        p = {}
        for station, df in grouped_data.items():
            for col in df.columns:
                if col != station:
                    combined = df[[station, col]].dropna()
                    if len(combined) >= 10:
                        r, _ = pearsonr(combined[station], combined[col])
                        p[col] = r
        return p

    pearsons_max = compute_all_pearsons(df_max)
    pearsons_annual = compute_all_pearsons(df_annual)
    pearsons_np95 = compute_all_pearsons(df_np95)

    # Pearson histograms
    for name, p_dict in [("maximum", pearsons_max), ("annual", pearsons_annual), ("np95", pearsons_np95)]:
        if not p_dict:
            continue
        fig, ax = plt.subplots()
        ax.hist(list(p_dict.values()), bins=10, color=FT_RED, alpha=0.6, edgecolor="white")
        ax.set_title(f"Pearson coefficients — {name} rainfall data")
        ax.set_xlabel("Pearson r")
        ax.set_ylabel("Count")
        savefig(fig, os.path.join(CHARTS, f"pearson_hist_{name}.png"))

    # Pearson vs distance
    for name, p_dict in [("maximum", pearsons_max), ("annual", pearsons_annual), ("np95", pearsons_np95)]:
        if not p_dict:
            continue
        distances = [reanalysis_info.loc[k, "distance"] for k in p_dict.keys() if k in reanalysis_info.index]
        values = [p_dict[k] for k in p_dict.keys() if k in reanalysis_info.index]
        fig, ax = plt.subplots()
        ax.scatter(distances, values, color=FT_BLUE, alpha=0.7)
        ax.set_title(f"Pearson r vs distance — {name}")
        ax.set_xlabel("Distance to nearest station (km)")
        ax.set_ylabel("Pearson r")
        savefig(fig, os.path.join(CHARTS, f"pearson_vs_distance_{name}.png"))

    print("  Exploration done.")


if __name__ == "__main__":
    main()
