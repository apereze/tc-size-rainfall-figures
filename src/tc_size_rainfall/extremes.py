"""Extreme precipitation helpers."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import xarray as xr


def load_p95_thresholds(path: str | Path, *, variable: str = "precip_p95") -> pd.DataFrame:
    """Load gridded p95 thresholds as a rounded lat/lon table."""
    with xr.open_dataset(path) as ds:
        thresholds = ds[variable].to_dataframe().reset_index()

    thresholds["lat"] = thresholds["lat"].round(2)
    thresholds["lon"] = thresholds["lon"].round(2)
    return thresholds.rename(columns={variable: "p95_valor"})


def mark_extreme_points(
    points: pd.DataFrame,
    thresholds: pd.DataFrame,
    *,
    precip_col: str = "pcp",
) -> pd.DataFrame:
    """Merge point precipitation with thresholds and keep p95 exceedances."""
    left = points.copy()
    left["lat"] = left["lat"].round(2)
    left["lon"] = left["lon"].round(2)
    merged = left.merge(thresholds, on=["lat", "lon"], how="left")
    return merged.loc[merged[precip_col] > merged["p95_valor"]].copy()


def attach_storm_metadata(
    extreme_points: pd.DataFrame,
    track_row: pd.Series,
    *,
    precip_col: str = "pcp",
) -> pd.DataFrame:
    """Attach cyclone-position metadata and canonical output column names."""
    out = extreme_points.assign(
        CT=track_row["CT"],
        mm=track_row["mm"],
        dd=track_row["dd"],
        hh=track_row["hh"],
        lat_cyclone=track_row["lat"],
        lon_cyclone=track_row["lon"],
        MWS=track_row["MWS"],
    )
    out = out.rename(
        columns={
            "lat": "lat_p",
            "lon": "lon_p",
            precip_col: "precip",
        }
    )
    columns = [
        "CT",
        "mm",
        "dd",
        "hh",
        "lat_cyclone",
        "lon_cyclone",
        "lat_p",
        "lon_p",
        "precip",
        "p95_valor",
        "cuadrante",
        "r",
        "MWS",
    ]
    return out[[column for column in columns if column in out.columns]]
