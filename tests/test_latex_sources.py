"""Structural checks for LaTeX/PGFPlots figure sources."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LATEX_FIGURES = ROOT / "latex" / "figures"


def test_latex_figure_sources_exist() -> None:
    for filename in [
        "fig01_structure_boxplots.tex",
        "fig02_radial_profiles.tex",
        "fig04_radius_precip_scatter.tex",
    ]:
        assert (LATEX_FIGURES / filename).is_file()


def test_figure1_boxplot_source_has_expected_number_of_boxes() -> None:
    text = (LATEX_FIGURES / "fig01_structure_boxplots.tex").read_text(encoding="utf-8")

    assert text.count("boxplot prepared={") == 56
    assert "boxplot/whisker extend" in text
    assert "boxplot/box extend" in text


def test_latex_csv_references_resolve() -> None:
    for tex_path in LATEX_FIGURES.glob("fig*.tex"):
        text = tex_path.read_text(encoding="utf-8")
        data_dir_match = re.search(r"\\newcommand\{\\dataDir\}\{([^}]+)\}", text)
        if not data_dir_match:
            continue

        data_dir_value = Path(data_dir_match.group(1))
        data_dir = data_dir_value if data_dir_value.is_absolute() else ROOT / data_dir_value
        csv_names = re.findall(r"\\dataDir/([^}\s]+\.csv)", text)
        assert csv_names, f"{tex_path.name} should reference at least one CSV table"

        for csv_name in csv_names:
            assert (data_dir / csv_name).is_file(), f"{tex_path.name} references missing {csv_name}"
