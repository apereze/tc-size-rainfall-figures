"""Track-table helpers used across the figure reproduction workflow."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


TRACK_COLUMNS = [
    "dd",
    "mm",
    "yy",
    "hh",
    "lat",
    "lon",
    "MWS",
    "CPSL",
    "RNE",
    "RNW",
    "RSW",
    "RSE",
    "Rp",
    "A",
    "D",
    "S",
    "CT",
]

LEGACY_TRACK_RENAMES = {
    "RNO": "RNW",
    "RSO": "RSW",
}


def read_track_table(path: str | Path, *, names: list[str] | None = None) -> pd.DataFrame:
    """Read a legacy track table and normalize quadrant radius column names."""
    df = pd.read_csv(path, names=names or TRACK_COLUMNS, index_col=False)
    return normalize_track_columns(df)


def normalize_track_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with canonical quadrant names and numeric date/radius fields."""
    out = df.rename(columns=LEGACY_TRACK_RENAMES).copy()

    for column in ["dd", "mm", "yy", "hh", "lat", "lon", "MWS", "CPSL", "Rp", "A", "D", "S"]:
        if column in out.columns:
            out[column] = pd.to_numeric(out[column], errors="coerce")

    for column in ["RNE", "RNW", "RSW", "RSE"]:
        if column in out.columns:
            out[column] = pd.to_numeric(out[column], errors="coerce")

    if "CT" in out.columns:
        out["CT"] = out["CT"].astype(str)

    return out


def filter_synoptic_hours(
    df: pd.DataFrame, hours: tuple[int, ...] = (0, 6, 12, 18)
) -> pd.DataFrame:
    """Keep only the standard 6-hourly synoptic positions."""
    return df.loc[df["hh"].isin(hours)].reset_index(drop=True)


def add_storm_datetime(df: pd.DataFrame, *, two_digit_year_base: int = 2000) -> pd.DataFrame:
    """Add a datetime column from dd/mm/yy/hh fields.

    The legacy files use two-digit years for the 2000-2024 study period. Values
    below 100 are shifted by ``two_digit_year_base``; four-digit years are kept.
    """
    out = df.copy()
    years = out["yy"].astype("Int64")
    years = np.where(years < 100, years + two_digit_year_base, years)
    out["datetime"] = pd.to_datetime(
        {
            "year": years,
            "month": out["mm"].astype("Int64"),
            "day": out["dd"].astype("Int64"),
            "hour": out["hh"].astype("Int64"),
        },
        errors="coerce",
    )
    return out


def require_quadrant_radii(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows missing any quadrant radius and add ``R_max``."""
    out = normalize_track_columns(df)
    quadrants = ["RNE", "RNW", "RSW", "RSE"]
    out = out.dropna(subset=quadrants).copy()
    out["R_max"] = out[quadrants].max(axis=1)
    return out.reset_index(drop=True)
