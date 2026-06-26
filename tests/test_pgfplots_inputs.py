"""Checks for committed lightweight PGFPlots input tables."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIGURE_INPUTS = ROOT / "data" / "figure_inputs"


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def test_figure1_boxplot_stats_are_complete() -> None:
    columns, rows = read_csv(FIGURE_INPUTS / "fig01_boxplot_stats.csv")

    assert len(rows) == 56
    assert {
        "category",
        "category_label",
        "metric_group",
        "metric",
        "basin_code",
        "basin",
        "n",
        "mean",
        "lower_whisker",
        "q1",
        "median",
        "q3",
        "upper_whisker",
        "outlier_count",
    }.issubset(columns)
    assert {row["basin_code"] for row in rows} == {"NA", "EP"}
    assert {row["category"] for row in rows} == {"TD", "TS", "MIN_HUR", "MAJ_HUR"}
    assert {row["metric"] for row in rows} == {"RNE", "RNW", "RSW", "RSE", "A", "D", "S"}


def test_figure4_scatter_tables_are_partitioned() -> None:
    columns, combined_rows = read_csv(FIGURE_INPUTS / "fig04_radius_precip_scatter.csv")

    assert len(combined_rows) == 13582
    assert {
        "basin_code",
        "basin",
        "category",
        "category_label",
        "CT",
        "yy",
        "mm",
        "dd",
        "hh",
        "MWS",
        "Rp",
        "accumulated_precipitation_mm",
    }.issubset(columns)

    subset_dir = FIGURE_INPUTS / "fig04_scatter"
    subset_files = sorted(subset_dir.glob("*.csv"))
    assert [path.name for path in subset_files] == [
        "EP_MAJ_HUR.csv",
        "EP_MIN_HUR.csv",
        "EP_TD.csv",
        "EP_TS.csv",
        "NA_MAJ_HUR.csv",
        "NA_MIN_HUR.csv",
        "NA_TD.csv",
        "NA_TS.csv",
    ]

    subset_row_count = 0
    for path in subset_files:
        subset_columns, subset_rows = read_csv(path)
        subset_row_count += len(subset_rows)
        assert {
            "Rp",
            "accumulated_precipitation_mm",
            "category",
            "basin_code",
        }.issubset(subset_columns)

    assert subset_row_count == len(combined_rows)
