"""Validate repository structure for reproducible figure generation."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "figures" / "figure_manifest.json"

EXPECTED_DIRECTORIES = [
    "data/raw",
    "data/interim",
    "data/processed",
    "data/external",
    "data/figure_inputs",
    "docs",
    "figures",
    "latex/figures",
    "notebooks",
    "outputs/figures",
    "outputs/tables",
    "scripts",
    "src/tc_size_rainfall",
    "tests",
]

REQUIRED_FILES = [
    "README.md",
    "environment.yml",
    "pyproject.toml",
    "docs/data_inventory.md",
    "docs/figure_plan.md",
    "docs/repository_structure.md",
    "figures/figure_manifest.json",
    "latex/README.md",
    "latex/figures/fig01_structure_boxplots.tex",
    "latex/figures/fig02_radial_profiles.tex",
    "latex/figures/fig04_radius_precip_scatter.tex",
    "scripts/check_environment.py",
    "scripts/prepare_pgfplots_inputs.py",
    "scripts/run_all_figures.py",
]

GITKEEP_DIRECTORIES = [
    "data/raw",
    "data/interim",
    "data/processed",
    "data/external",
    "data/figure_inputs",
    "outputs/figures",
    "outputs/tables",
]

DISALLOWED_TRACKED_SUFFIXES = {
    ".csv",
    ".xlsx",
    ".xls",
    ".nc",
    ".grib",
    ".grb",
    ".tif",
    ".tiff",
    ".h5",
    ".hdf",
    ".gpkg",
    ".parquet",
}


def _load_manifest() -> dict:
    with MANIFEST_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_run_all_scripts() -> list[str]:
    module_path = ROOT / "scripts" / "run_all_figures.py"
    spec = importlib.util.spec_from_file_location("run_all_figures", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return list(module.FIGURE_SCRIPTS)


def _tracked_files() -> list[Path]:
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return []

    return [Path(line) for line in result.stdout.splitlines() if line.strip()]


def validate_repository() -> list[str]:
    """Return validation errors without printing."""
    errors: list[str] = []

    for directory in EXPECTED_DIRECTORIES:
        if not (ROOT / directory).is_dir():
            errors.append(f"Missing directory: {directory}")

    for path in REQUIRED_FILES:
        if not (ROOT / path).is_file():
            errors.append(f"Missing required file: {path}")

    for directory in GITKEEP_DIRECTORIES:
        if not (ROOT / directory / ".gitkeep").is_file():
            errors.append(f"Missing placeholder file: {directory}/.gitkeep")

    if MANIFEST_PATH.is_file():
        try:
            manifest = _load_manifest()
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON manifest: {exc}")
            manifest = {"figures": []}

        figures = manifest.get("figures", [])
        if not isinstance(figures, list) or not figures:
            errors.append("Manifest must contain a non-empty figures list")
            figures = []

        figure_ids = [item.get("id") for item in figures if isinstance(item, dict)]
        scripts = [item.get("script") for item in figures if isinstance(item, dict)]

        if len(figure_ids) != len(set(figure_ids)):
            errors.append("Manifest contains duplicate figure IDs")
        if len(scripts) != len(set(scripts)):
            errors.append("Manifest contains duplicate figure scripts")

        for item in figures:
            if not isinstance(item, dict):
                errors.append("Manifest figure entries must be objects")
                continue

            script = item.get("script")
            outputs = item.get("outputs", [])
            required_inputs = item.get("required_inputs", [])

            if not script or not (ROOT / script).is_file():
                errors.append(f"Manifest script does not exist: {script}")
            if not outputs:
                errors.append(f"Manifest entry has no outputs: {item.get('id')}")
            if not required_inputs:
                errors.append(f"Manifest entry has no required inputs: {item.get('id')}")

        try:
            run_all_scripts = _load_run_all_scripts()
        except RuntimeError as exc:
            errors.append(str(exc))
        else:
            if scripts != run_all_scripts:
                errors.append(
                    "scripts/run_all_figures.py FIGURE_SCRIPTS does not match "
                    "figures/figure_manifest.json order"
                )

    for path in _tracked_files():
        path_text = path.as_posix()
        if not path_text.startswith(("data/", "outputs/")):
            continue
        if path.name == ".gitkeep" or path.suffix == ".md":
            continue
        if path_text.startswith("data/figure_inputs/") and path.suffix.lower() == ".csv":
            continue
        if path.suffix.lower() in DISALLOWED_TRACKED_SUFFIXES:
            errors.append(f"Tracked data/output artifact should stay local: {path_text}")

    return errors


def main() -> int:
    errors = validate_repository()
    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Repository structure is valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
