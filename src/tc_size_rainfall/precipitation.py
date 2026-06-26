"""Precipitation extraction helpers adapted from the original figure scripts."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

from tc_size_rainfall.tracks import require_quadrant_radii


def day_of_year(day: int, month: int, year: int) -> int:
    """Return day of year for a track record."""
    return int(pd.Timestamp(year=int(year), month=int(month), day=int(day)).day_of_year)


def mswep_3hourly_path(
    root: str | Path,
    *,
    year: int,
    month: int,
    day: int,
    hour: int,
) -> Path:
    """Build the MSWEP 3-hourly filename used by the legacy scripts."""
    doy = day_of_year(day, month, year)
    return Path(root) / f"{int(year):02d}{doy:03d}.{int(hour):02d}.nc"


def open_mswep_precipitation(
    path: str | Path,
    *,
    lon_bounds: tuple[float, float] = (-140, -60),
    lat_bounds: tuple[float, float] = (5, 35),
    variable: str = "precipitation",
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Open a precipitation field and return ``precip, lat, lon`` arrays."""
    with xr.open_dataset(path) as ds:
        lat = ds["lat"]
        lon = ds["lon"]
        lat_slice = slice(lat_bounds[1], lat_bounds[0]) if lat[0] > lat[-1] else slice(*lat_bounds)
        lon_slice = slice(*lon_bounds) if lon[0] < lon[-1] else slice(lon_bounds[1], lon_bounds[0])
        subset = ds.sel(lat=lat_slice, lon=lon_slice)
        precip = subset[variable].isel(time=0).values
        return precip, subset["lat"].values, subset["lon"].values


def precipitation_points(
    precip: np.ndarray,
    lat: np.ndarray,
    lon: np.ndarray,
    *,
    center_lat: float,
    center_lon: float,
) -> pd.DataFrame:
    """Convert a gridded precipitation field into points with distance/quadrant."""
    x, y = np.meshgrid(lon, lat)
    df = pd.DataFrame({"lon": x.ravel(), "lat": y.ravel(), "pcp": precip.ravel()})
    df = df[df["pcp"] >= 0].copy()
    df["dx_km"] = (df["lon"] - center_lon) * 111.1
    df["dy_km"] = (df["lat"] - center_lat) * 111.1
    df["r"] = np.sqrt(df["dx_km"] ** 2 + df["dy_km"] ** 2)
    theta = np.degrees(np.arctan2(df["dy_km"], df["dx_km"])) % 360
    df["theta"] = theta
    df["cuadrante"] = np.select(
        [
            (theta >= 0) & (theta < 90),
            (theta >= 90) & (theta < 180),
            (theta >= 180) & (theta < 270),
            (theta >= 270) & (theta < 360),
        ],
        [1, 2, 3, 4],
    )
    return df


def clip_points_to_quadrant_radii(points: pd.DataFrame, track_row: pd.Series) -> pd.DataFrame:
    """Keep only points inside the corresponding quadrant radius."""
    radius_by_quadrant = {
        1: track_row["RNE"],
        2: track_row["RNW"],
        3: track_row["RSW"],
        4: track_row["RSE"],
    }
    max_radius = points["cuadrante"].map(radius_by_quadrant)
    return points.loc[points["r"] <= max_radius].copy()


def radial_profile_from_points(
    points: pd.DataFrame,
    *,
    value_col: str = "pcp",
    distance_col: str = "r",
    max_radius_km: int = 2000,
    width_km: int = 50,
) -> pd.Series:
    """Return mean precipitation by fixed-width radial bins."""
    bins = np.arange(0, max_radius_km + width_km, width_km)
    labels = np.arange(len(bins) - 1)
    binned = pd.cut(points[distance_col], bins, labels=labels)
    profile = points.groupby(binned, observed=False)[value_col].mean()
    return profile.reindex(labels, fill_value=0.0)


def prepare_track_rows_for_precipitation(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize tracks and keep rows with complete quadrant radii."""
    return require_quadrant_radii(df)
