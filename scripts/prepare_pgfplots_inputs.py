"""Prepare lightweight PGFPlots inputs from the original figure workspace."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tc_size_rainfall.tracks import normalize_track_columns

FIGURE_INPUT_DIR = ROOT / "data" / "figure_inputs"
LATEX_FIGURE_DIR = ROOT / "latex" / "figures"

LEGACY_TRACK_COLUMNS = [
    "dd",
    "mm",
    "yy",
    "hh",
    "lat",
    "lon",
    "MWS",
    "CPSL",
    "RNE",
    "RNO",
    "RSO",
    "RSE",
    "Rp",
    "A",
    "D",
    "S",
    "CT",
]

BASINS = [
    ("NA", "North Atlantic"),
    ("EP", "Eastern Pacific"),
]

CATEGORIES = [
    ("TD", "Tropical Depression"),
    ("TS", "Tropical Storm"),
    ("MIN_HUR", "Minor Hurricane"),
    ("MAJ_HUR", "Major Hurricane"),
]

RADII = ["RNE", "RNW", "RSW", "RSE"]
STRUCTURE_METRICS = ["A", "D", "S"]


def classify_intensity(mws: float) -> str:
    """Classify intensity using the thresholds from the original notebooks."""
    if mws <= 63:
        return "TD"
    if mws <= 119:
        return "TS"
    if mws <= 178:
        return "MIN_HUR"
    return "MAJ_HUR"


def read_tracks(source_dir: Path) -> pd.DataFrame:
    frames = []
    for basin_code, basin_name in BASINS:
        filename = "dfna.csv" if basin_code == "NA" else "dfep.csv"
        path = source_dir / "db" / filename
        df = pd.read_csv(path, names=LEGACY_TRACK_COLUMNS, index_col=False)
        df = normalize_track_columns(df)
        df["basin_code"] = basin_code
        df["basin"] = basin_name
        frames.append(df)

    tracks = pd.concat(frames, ignore_index=True)
    tracks["category"] = tracks["MWS"].apply(classify_intensity)
    tracks["category_label"] = tracks["category"].map(dict(CATEGORIES))
    return tracks


def prepared_boxplot(values: pd.Series) -> dict[str, float | int]:
    clean = pd.to_numeric(values, errors="coerce").dropna()
    q1 = clean.quantile(0.25)
    median = clean.quantile(0.50)
    q3 = clean.quantile(0.75)
    iqr = q3 - q1
    lower_limit = q1 - 1.5 * iqr
    upper_limit = q3 + 1.5 * iqr
    inliers = clean[(clean >= lower_limit) & (clean <= upper_limit)]

    return {
        "n": int(clean.size),
        "mean": float(clean.mean()),
        "lower_whisker": float(inliers.min()),
        "q1": float(q1),
        "median": float(median),
        "q3": float(q3),
        "upper_whisker": float(inliers.max()),
        "outlier_count": int(clean.size - inliers.size),
    }


def write_boxplot_inputs(tracks: pd.DataFrame, output_dir: Path) -> pd.DataFrame:
    rows = []
    for category, category_label in CATEGORIES:
        for metric_group, metrics in [
            ("radius", RADII),
            ("structure", STRUCTURE_METRICS),
        ]:
            for metric in metrics:
                for basin_code, basin_name in BASINS:
                    subset = tracks[
                        (tracks["category"] == category)
                        & (tracks["basin_code"] == basin_code)
                    ]
                    stats = prepared_boxplot(subset[metric])
                    rows.append(
                        {
                            "category": category,
                            "category_label": category_label,
                            "metric_group": metric_group,
                            "metric": metric,
                            "basin_code": basin_code,
                            "basin": basin_name,
                            **stats,
                        }
                    )

    stats_df = pd.DataFrame(rows)
    output_dir.mkdir(parents=True, exist_ok=True)
    stats_df.to_csv(output_dir / "fig01_boxplot_stats.csv", index=False)

    counts = (
        tracks.groupby(["category", "category_label"], observed=True)
        .size()
        .rename("n")
        .reset_index()
    )
    counts.to_csv(output_dir / "fig01_category_counts.csv", index=False)
    return stats_df


def parse_position_filename(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    extracted = out["nombre_archivo"].str.extract(r"(?P<CT>\w{8})_(?P<mm>\d{2})(?P<dd>\d{2})_(?P<hh>\d{2})")
    return pd.concat([out, extracted], axis=1)


def normalized_merge_keys(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["CT"] = out["CT"].astype(str)
    for col in ["dd", "mm", "hh"]:
        out[col] = pd.to_numeric(out[col], errors="coerce").astype("Int64").astype(str).str.zfill(2)
    return out


def write_scatter_inputs(source_dir: Path, tracks: pd.DataFrame, output_dir: Path) -> pd.DataFrame:
    frames = []
    for basin_code, basin_name in BASINS:
        suffix = "na" if basin_code == "NA" else "ep"
        accum_path = (
            source_dir
            / "acumulado_total_por_posicion"
            / f"acumulado_total_{suffix}.csv"
        )
        accum = parse_position_filename(pd.read_csv(accum_path))
        accum = normalized_merge_keys(accum)

        basin_tracks = normalized_merge_keys(
            tracks[tracks["basin_code"] == basin_code].copy()
        )
        basin_tracks = basin_tracks.drop_duplicates(
            subset=["CT", "dd", "mm", "hh"], keep="first"
        )
        merged = accum.merge(
            basin_tracks,
            on=["CT", "dd", "mm", "hh"],
            how="left",
            validate="many_to_one",
        )
        merged["basin_code"] = basin_code
        merged["basin"] = basin_name
        frames.append(merged)

    scatter = pd.concat(frames, ignore_index=True)
    scatter = scatter[
        [
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
            "acumulado_total_pcp",
        ]
    ].rename(columns={"acumulado_total_pcp": "accumulated_precipitation_mm"})
    scatter = scatter.dropna(subset=["category", "Rp", "accumulated_precipitation_mm"])

    output_dir.mkdir(parents=True, exist_ok=True)
    scatter.to_csv(output_dir / "fig04_radius_precip_scatter.csv", index=False)

    subset_dir = output_dir / "fig04_scatter"
    subset_dir.mkdir(parents=True, exist_ok=True)
    for basin_code, _ in BASINS:
        for category, _ in CATEGORIES:
            subset = scatter[
                (scatter["basin_code"] == basin_code)
                & (scatter["category"] == category)
            ]
            subset.to_csv(subset_dir / f"{basin_code}_{category}.csv", index=False)

    return scatter


def tex_number(value: float) -> str:
    if not np.isfinite(value):
        return "nan"
    return f"{value:.6g}"


def write_fig01_tex(stats: pd.DataFrame, output_path: Path) -> None:
    colors = {"NA": "naBlue", "EP": "epRed"}
    offsets = {"NA": -0.16, "EP": 0.16}
    lines = [
        "% Generated by scripts/prepare_pgfplots_inputs.py",
        "\\documentclass[tikz,border=2mm]{standalone}",
        "\\usepackage{pgfplots}",
        "\\usepgfplotslibrary{groupplots,statistics}",
        "\\pgfplotsset{compat=1.18}",
        "\\definecolor{naBlue}{HTML}{2A6FBB}",
        "\\definecolor{epRed}{HTML}{B23A48}",
        "\\begin{document}",
        "\\begin{tikzpicture}",
        "\\begin{groupplot}[",
        "  group style={group size=4 by 2, horizontal sep=1.1cm, vertical sep=1.25cm},",
        "  width=5.2cm,",
        "  height=4.2cm,",
        "  boxplot/draw direction=y,",
        "  tick align=outside,",
        "  ymajorgrids=true,",
        "  grid style={gray!20},",
        "  legend style={draw=none, at={(0.5,-0.28)}, anchor=north, legend columns=2},",
        "]",
    ]

    panel_letters = list("ABCDEFGH")
    panel = 0
    for row_name, metrics, ylabel, ymin, ymax in [
        ("radius", RADII, "Radius (km)", 0, 2500),
        ("structure", STRUCTURE_METRICS, "Metric value", 0, 1.05),
    ]:
        for category, category_label in CATEGORIES:
            xticks = ",".join(str(i) for i in range(1, len(metrics) + 1))
            xticklabels = ",".join(metrics)
            lines.extend(
                [
                    (
                        "\\nextgroupplot["
                        f"title={{\\textbf{{{panel_letters[panel]}.}} {category_label}}}, "
                        f"ylabel={{{ylabel}}}, ymin={ymin}, ymax={ymax}, "
                        f"xtick={{{xticks}}}, xticklabels={{{xticklabels}}}, "
                        "x tick label style={font=\\small}, y tick label style={font=\\small}]"
                    )
                ]
            )
            for x_idx, metric in enumerate(metrics, start=1):
                for basin_code, basin_name in BASINS:
                    row = stats[
                        (stats["category"] == category)
                        & (stats["metric"] == metric)
                        & (stats["basin_code"] == basin_code)
                    ].iloc[0]
                    draw_position = x_idx + offsets[basin_code]
                    color = colors[basin_code]
                    lines.extend(
                        [
                            "\\addplot+[",
                            "  boxplot prepared={",
                            f"    draw position={draw_position:.2f},",
                            f"    lower whisker={tex_number(row['lower_whisker'])},",
                            f"    lower quartile={tex_number(row['q1'])},",
                            f"    median={tex_number(row['median'])},",
                            f"    upper quartile={tex_number(row['q3'])},",
                            f"    upper whisker={tex_number(row['upper_whisker'])},",
                            f"    average={tex_number(row['mean'])}",
                            "  },",
                            f"  draw={color}, fill={color}!12, mark=*, mark options={{draw=black, fill=white}},",
                            "  boxplot/whisker extend=0.12, boxplot/box extend=0.20",
                            "] coordinates {};",
                        ]
                    )
                    if panel == 0 and metric == metrics[0]:
                        lines.append(f"\\addlegendentry{{{basin_name}}}")
            panel += 1

    lines.extend(
        [
            "\\end{groupplot}",
            "\\end{tikzpicture}",
            "\\end{document}",
            "",
        ]
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")


def resolve_source_dir(value: str | None) -> Path:
    if value:
        return Path(value).expanduser().resolve()
    env_value = os.environ.get("TC_SIZE_RAINFALL_ORIGINAL_DIR")
    if env_value:
        return Path(env_value).expanduser().resolve()
    raise SystemExit(
        "Pass --source-dir or set TC_SIZE_RAINFALL_ORIGINAL_DIR to the original "
        "Figures_Article_Size_Pcp folder."
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate lightweight PGFPlots inputs from original figure code outputs."
    )
    parser.add_argument("--source-dir", help="Original Figures_Article_Size_Pcp folder.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=FIGURE_INPUT_DIR,
        help="Directory where CSV inputs will be written.",
    )
    parser.add_argument(
        "--latex-dir",
        type=Path,
        default=LATEX_FIGURE_DIR,
        help="Directory where generated LaTeX sources will be written.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    source_dir = resolve_source_dir(args.source_dir)
    if not source_dir.exists():
        raise SystemExit(f"Source directory does not exist: {source_dir}")

    tracks = read_tracks(source_dir)
    stats = write_boxplot_inputs(tracks, args.output_dir)
    scatter = write_scatter_inputs(source_dir, tracks, args.output_dir)
    write_fig01_tex(stats, args.latex_dir / "fig01_structure_boxplots.tex")

    print(f"Wrote Figure 1 boxplot stats: {len(stats)} rows")
    print(f"Wrote Figure 4 scatter data: {len(scatter)} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
