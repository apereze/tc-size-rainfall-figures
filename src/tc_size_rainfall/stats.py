import numpy as np
import pandas as pd


def empirical_percentile_threshold(
    data: pd.DataFrame,
    *,
    value_col: str = "precip",
    group_cols: list[str],
    percentile: float = 0.95,
) -> pd.DataFrame:
    """Compute empirical percentile thresholds by grid cell or group."""
    return (
        data.groupby(group_cols, observed=True)[value_col]
        .quantile(percentile)
        .rename(f"p{int(percentile * 100)}")
        .reset_index()
    )


def bootstrap_ols_slope(x, y, n_boot: int = 3000, random_state: int = 42):
    """Placeholder for bootstrap OLS trend estimation."""
    rng = np.random.default_rng(random_state)
    x = np.asarray(x)
    y = np.asarray(y)
    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]
    y = y[mask]

    if len(x) < 3:
        return np.nan, np.nan

    slopes = []
    for _ in range(n_boot):
        idx = rng.integers(0, len(x), len(x))
        slope = np.polyfit(x[idx], y[idx], deg=1)[0]
        slopes.append(slope)

    slopes = np.asarray(slopes)
    return np.nanmean(slopes), np.mean(np.sign(slopes) == np.sign(np.nanmean(slopes)))
