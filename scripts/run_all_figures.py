import argparse
import subprocess
import sys
from pathlib import Path

FIGURE_SCRIPTS = [
    "figures/fig01_structure_boxplots.py",
    "figures/fig02_radial_profiles.py",
    "figures/fig03_seasonal_maps.py",
    "figures/fig04_radius_precip_scatter.py",
    "figures/fig05_extreme_radial_quadrants.py",
    "figures/fig06_extreme_distance_histograms.py",
    "figures/fig07_structure_trends.py",
    "figures/fig08_environment_composites_r1_r2.py",
    "figures/fig09_environment_composites_r3_r4.py",
    "figures/fig10_mld_anomalies.py",
]


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Run manuscript figure scripts in publication order."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print scripts in execution order without running them.",
    )
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Run remaining scripts even if one script fails.",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    failures = []

    for script in FIGURE_SCRIPTS:
        script_path = root / script
        if args.dry_run:
            print(script)
            continue

        print(f"Running {script}")
        try:
            subprocess.run([sys.executable, str(script_path)], cwd=root, check=True)
        except subprocess.CalledProcessError as exc:
            failures.append((script, exc.returncode))
            if not args.continue_on_error:
                raise

    if failures:
        failed = ", ".join(f"{script}({code})" for script, code in failures)
        raise SystemExit(f"Figure generation failed: {failed}")


if __name__ == "__main__":
    main()
