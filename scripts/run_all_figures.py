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


def main():
    root = Path(__file__).resolve().parents[1]
    for script in FIGURE_SCRIPTS:
        print(f"Running {script}")
        subprocess.run([sys.executable, str(root / script)], check=True)


if __name__ == "__main__":
    main()
