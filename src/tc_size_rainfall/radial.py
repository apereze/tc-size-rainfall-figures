import numpy as np
import pandas as pd


def assign_radial_bin(distance_km: pd.Series, width_km: int = 50) -> pd.Series:
    """Assign radial distance to fixed-width rings."""
    return (np.floor(distance_km / width_km) * width_km).astype(int)


def summarize_radial_profile(
    df: pd.DataFrame,
    *,
    distance_col: str = "distance_km",
    value_col: str = "precip",
    group_cols: list[str] | None = None,
    width_km: int = 50,
) -> pd.DataFrame:
    """Compute mean radial profiles by basin, quadrant, category, or other groups."""
    group_cols = group_cols or []
    out = df.copy()
    out["radius_bin_km"] = assign_radial_bin(out[distance_col], width_km=width_km)

    return (
        out.groupby(group_cols + ["radius_bin_km"], observed=True)[value_col]
        .agg(["mean", "median", "count"])
        .reset_index()
    )
