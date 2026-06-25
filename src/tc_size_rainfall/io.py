from pathlib import Path

import pandas as pd
import xarray as xr


def read_table(path: str | Path, **kwargs) -> pd.DataFrame:
    """Read a tabular file based on its extension."""
    path = Path(path)

    if path.suffix == ".csv":
        return pd.read_csv(path, **kwargs)
    if path.suffix in {".parquet", ".pq"}:
        return pd.read_parquet(path, **kwargs)
    if path.suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path, **kwargs)

    raise ValueError(f"Unsupported table format: {path.suffix}")


def open_dataset(path: str | Path, **kwargs) -> xr.Dataset:
    """Open a NetCDF/Zarr-compatible dataset with xarray."""
    path = Path(path)

    if path.suffix == ".zarr":
        return xr.open_zarr(path, **kwargs)

    return xr.open_dataset(path, **kwargs)
