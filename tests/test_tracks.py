import pandas as pd

from tc_size_rainfall.tracks import (
    add_storm_datetime,
    filter_synoptic_hours,
    normalize_track_columns,
    require_quadrant_radii,
)


def test_normalize_track_columns_accepts_legacy_quadrant_names():
    df = pd.DataFrame(
        {
            "RNE": ["100"],
            "RNO": ["90"],
            "RSO": ["80"],
            "RSE": ["70"],
            "CT": ["AL012000"],
        }
    )

    out = normalize_track_columns(df)

    assert list(out[["RNE", "RNW", "RSW", "RSE"]].iloc[0]) == [100, 90, 80, 70]


def test_filter_synoptic_hours_and_datetime():
    df = pd.DataFrame(
        {
            "yy": [0, 24, 2024],
            "mm": [6, 9, 9],
            "dd": [1, 23, 23],
            "hh": [0, 3, 18],
        }
    )

    out = add_storm_datetime(filter_synoptic_hours(df))

    assert list(out["hh"]) == [0, 18]
    assert list(out["datetime"].dt.year) == [2000, 2024]


def test_require_quadrant_radii_adds_max_radius():
    df = pd.DataFrame(
        {
            "RNE": [100, None],
            "RNW": [120, 1],
            "RSW": [90, 1],
            "RSE": [80, 1],
        }
    )

    out = require_quadrant_radii(df)

    assert len(out) == 1
    assert out.loc[0, "R_max"] == 120
