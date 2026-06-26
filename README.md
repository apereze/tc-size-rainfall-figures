# TC Size-Rainfall Figures

Reproducible repository to recreate the figures for the manuscript:

**Influence of Tropical Cyclone Size on Rainfall Distribution and Extremes in
Middle Americas**

This repository is organized as a code backup for figure reproduction. It keeps
large scientific datasets out of Git while preserving the scripts, reusable
helpers, environment definition, and documentation needed to regenerate the
paper figures from local input data.

## Current status

The repository structure is in place and each manuscript figure has a dedicated
script under `figures/`. Figures 1, 2, and 4 also have PGFPlots sources under
`latex/figures/` for publication-quality vector rendering. Some remaining
figure scripts still export placeholders while final processed inputs and
plotting logic are added. Use `figures/figure_manifest.json` as the source of
truth for the expected script, input, LaTeX source, and output paths.

## Repository layout

```text
tc-size-rainfall-figures/
|-- README.md
|-- environment.yml
|-- pyproject.toml
|-- data/
|   |-- raw/          # local-only original datasets
|   |-- interim/      # local-only intermediate products
|   |-- processed/    # local-only analysis-ready tables/grids
|   |-- external/     # local-only downloaded reference layers
|   `-- figure_inputs/# small committed CSV inputs for exact panels
|-- docs/
|   |-- data_inventory.md
|   |-- figure_plan.md
|   `-- repository_structure.md
|-- figures/
|   |-- figure_manifest.json
|   `-- figXX_*.py
|-- latex/
|   `-- figures/      # PGFPlots sources for publication panels
|-- notebooks/        # exploratory only
|-- outputs/
|   |-- figures/      # regenerated figure files
|   `-- tables/       # regenerated tabular outputs
|-- scripts/
|   |-- check_environment.py
|   |-- run_all_figures.py
|   `-- validate_repository.py
|-- src/tc_size_rainfall/
`-- tests/
```

## Installation

Recommended with conda or mamba:

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

Check that the expected Python packages are importable:

```bash
python scripts/check_environment.py
```

## Reproducibility workflow

1. Clone the repository.
2. Create the environment from `environment.yml`.
3. Place original input files in `data/raw/` and document them in
   `docs/data_inventory.md`.
4. Put deterministic processing code in `src/tc_size_rainfall/` or `scripts/`.
5. Keep one executable script per figure in `figures/`.
6. Export regenerated figures to `outputs/figures/`.
7. Run the repository checks before sharing changes:

```bash
python scripts/validate_repository.py
python -m pytest -q
```

Run every figure script from the repository root:

```bash
python scripts/run_all_figures.py
```

Run without executing scripts to inspect the planned order:

```bash
python scripts/run_all_figures.py --dry-run
```

Generate the lightweight PGFPlots input tables from the original local code
backup:

```bash
python scripts/prepare_pgfplots_inputs.py --source-dir C:\path\to\Figures_Article_Size_Pcp
```

Render the LaTeX figures, when a TeX engine is installed:

```bash
python scripts/render_latex_figures.py
```

## Figure scripts

| Figure | Main content | Script |
|---|---|---|
| Figure 1 | TC structural properties by basin/category | `figures/fig01_structure_boxplots.py`, `latex/figures/fig01_structure_boxplots.tex` |
| Figure 2 | Radial rainfall profiles | `figures/fig02_radial_profiles.py`, `latex/figures/fig02_radial_profiles.tex` |
| Figure 3 | Seasonal maps of precipitation and structure | `figures/fig03_seasonal_maps.py` |
| Figure 4 | Mean radius vs accumulated precipitation | `figures/fig04_radius_precip_scatter.py`, `latex/figures/fig04_radius_precip_scatter.tex` |
| Figure 5 | Radial-quadrant distribution of extreme events | `figures/fig05_extreme_radial_quadrants.py` |
| Figure 6 | Distance distribution of extreme events | `figures/fig06_extreme_distance_histograms.py` |
| Figure 7 | Trends in TC structural variables | `figures/fig07_structure_trends.py` |
| Figure 8 | Environmental composites R1-R2 | `figures/fig08_environment_composites_r1_r2.py` |
| Figure 9 | Environmental composites R3-R4 | `figures/fig09_environment_composites_r3_r4.py` |
| Figure 10 | Mixed layer depth anomalies | `figures/fig10_mld_anomalies.py` |

## Data policy

Large files should not be committed to GitHub. Use `data/raw/`,
`data/interim/`, `data/processed/`, and `data/external/` locally, but keep only
lightweight documentation and `.gitkeep` files in the repository. Small,
curated CSV inputs needed to reproduce exact final panels may be committed under
`data/figure_inputs/`. The `.gitignore` intentionally excludes common large
scientific formats such as NetCDF, GRIB, GeoTIFF, HDF, Zarr, Parquet, and Excel
files.
