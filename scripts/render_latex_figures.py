"""Render PGFPlots figure sources when a TeX engine is available."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LATEX_DIR = ROOT / "latex" / "figures"
OUTPUT_DIR = ROOT / "outputs" / "figures"

DEFAULT_FIGURES = [
    "fig01_structure_boxplots.tex",
    "fig02_radial_profiles.tex",
    "fig04_radius_precip_scatter.tex",
]


def find_engine() -> str | None:
    for engine in ["tectonic", "lualatex", "pdflatex"]:
        if shutil.which(engine):
            return engine
    return None


def command_for(engine: str, tex_path: Path, output_dir: Path) -> list[str]:
    if engine == "tectonic":
        return [engine, "--outdir", str(output_dir), str(tex_path)]
    return [
        engine,
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-output-directory",
        str(output_dir),
        str(tex_path),
    ]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render LaTeX/PGFPlots figures.")
    parser.add_argument(
        "figures",
        nargs="*",
        default=DEFAULT_FIGURES,
        help="TeX filenames under latex/figures.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    engine = find_engine()
    if engine is None:
        raise SystemExit(
            "No TeX engine found. Install tectonic, lualatex, or pdflatex."
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for figure in args.figures:
        tex_path = LATEX_DIR / figure
        if not tex_path.exists():
            raise SystemExit(f"Missing LaTeX source: {tex_path}")
        subprocess.run(command_for(engine, tex_path, OUTPUT_DIR), cwd=ROOT, check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
