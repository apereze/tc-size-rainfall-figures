from pathlib import Path

import pandas as pd


FIGURE_INPUTS = Path(__file__).resolve().parents[1] / "data" / "figure_inputs"


def test_radial_profile_figure_inputs_have_expected_schema():
    for name in ["NAQ.csv", "EPQ.csv", "NAcat.csv", "EPcat.csv"]:
        df = pd.read_csv(FIGURE_INPUTS / name)
        assert list(df.columns) == ["x", "rain", "basin"]
        assert df["x"].min() == 0
        assert df["x"].max() == 1950
        assert not df["rain"].isna().any()
