import numpy as np
import pandas as pd

from tc_size_rainfall.extremes import attach_storm_metadata, mark_extreme_points
from tc_size_rainfall.precipitation import (
    clip_points_to_quadrant_radii,
    day_of_year,
    mswep_3hourly_path,
    precipitation_points,
    radial_profile_from_points,
)


def test_mswep_path_uses_legacy_year_day_hour_format():
    path = mswep_3hourly_path("root", year=2024, month=9, day=23, hour=18)

    assert path.as_posix() == "root/2024267.18.nc"
    assert day_of_year(23, 9, 2024) == 267


def test_precipitation_points_quadrants_and_radius_clip():
    precip = np.ones((3, 3))
    lat = np.array([1.0, 0.0, -1.0])
    lon = np.array([-1.0, 0.0, 1.0])

    points = precipitation_points(precip, lat, lon, center_lat=0.0, center_lon=0.0)
    track = pd.Series({"RNE": 200, "RNW": 200, "RSW": 50, "RSE": 200})
    clipped = clip_points_to_quadrant_radii(points, track)

    assert set(points["cuadrante"]) == {1, 2, 3, 4}
    assert len(clipped) < len(points)


def test_radial_profile_and_extreme_metadata():
    points = pd.DataFrame(
        {
            "lat": [10.001, 10.006],
            "lon": [-90.001, -90.006],
            "pcp": [5.0, 20.0],
            "r": [25.0, 75.0],
            "cuadrante": [1, 2],
        }
    )
    thresholds = pd.DataFrame(
        {
            "lat": [10.0, 10.01],
            "lon": [-90.0, -90.01],
            "p95_valor": [10.0, 10.0],
        }
    )

    profile = radial_profile_from_points(points, max_radius_km=100, width_km=50)
    extremes = mark_extreme_points(points, thresholds)
    out = attach_storm_metadata(
        extremes,
        pd.Series({"CT": "AL012000", "mm": 6, "dd": 1, "hh": 0, "lat": 10, "lon": -90, "MWS": 35}),
    )

    assert profile.loc[0] == 5.0
    assert profile.loc[1] == 20.0
    assert list(out["CT"]) == ["AL012000"]
    assert list(out["precip"]) == [20.0]
