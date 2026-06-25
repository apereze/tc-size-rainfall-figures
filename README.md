# TC Size–Rainfall Figures

Reproducible repository to recreate the figures for the manuscript:

**Influence of Tropical Cyclone Size on Rainfall Distribution and Extremes in Middle Americas**

The repository is organized to separate:

- raw data
- intermediate products
- processed analysis-ready tables/grids
- figure scripts
- reusable plotting and geospatial utilities
- final exported figures

## Scientific scope

The manuscript evaluates how tropical cyclone size, using the ROCLOUD metric, modulates rainfall distribution and precipitation extremes across Middle Americas during 2000–2024.

Main figure groups:

| Figure | Main content | Suggested script |
|---|---|---|
| Figure 1 | TC structural properties by basin/category | `figures/fig01_structure_boxplots.py` |
| Figure 2 | Radial rainfall profiles | `figures/fig02_radial_profiles.py` |
| Figure 3 | Seasonal maps of precipitation and structure | `figures/fig03_seasonal_maps.py` |
| Figure 4 | Mean radius vs accumulated precipitation | `figures/fig04_radius_precip_scatter.py` |
| Figure 5 | Radial-quadrant distribution of extreme events | `figures/fig05_extreme_radial_quadrants.py` |
| Figure 6 | Distance distribution of extreme events | `figures/fig06_extreme_distance_histograms.py` |
| Figure 7 | Trends in TC structural variables | `figures/fig07_structure_trends.py` |
| Figure 8 | Environmental composites R1–R2 | `figures/fig08_environment_composites_r1_r2.py` |
| Figure 9 | Environmental composites R3–R4 | `figures/fig09_environment_composites_r3_r4.py` |
| Figure 10 | Mixed layer depth anomalies | `figures/fig10_mld_anomalies.py` |

## Installation

Recommended with conda/mamba:

```bash
mamba env create -f environment.yml
conda activate tc-size-rainfall
python -m ipykernel install --user --name tc-size-rainfall --display-name "Python (tc-size-rainfall)"
```

Or with conda:

```bash
conda env create -f environment.yml
conda activate tc-size-rainfall
```

Install the local package in editable mode:

```bash
pip install -e .
```

## Suggested workflow

1. Place original input files in `data/raw/`.
2. Use notebooks only for exploration.
3. Move stable processing steps into `src/tc_size_rainfall/`.
4. Keep one script per figure in `figures/`.
5. Export final figures to `outputs/figures/`.
6. Avoid committing heavy datasets.

## Data policy

Large files should not be committed to GitHub. Use `data/raw/`, `data/interim/`, and `data/processed/` locally, but keep only `.gitkeep` files in the repository.

## Reproducibility

Each figure script should be executable from the repository root, for example:

```bash
python figures/fig02_radial_profiles.py
```

