# Repository structure audit

This repository follows a lightweight scientific reproducibility layout: raw
inputs remain local, deterministic code is versioned, figure scripts are
separated from reusable utilities, and regenerated artifacts are written to
`outputs/`.

## Required top-level layout

| Path | Purpose | Version-control policy |
|---|---|---|
| `data/raw/` | Original downloaded or received datasets | Keep local; commit only `.gitkeep` |
| `data/interim/` | Temporary intermediate products | Keep local; commit only `.gitkeep` |
| `data/processed/` | Analysis-ready tables and grids | Keep local unless tiny metadata |
| `data/external/` | Reference layers from external sources | Keep local unless tiny metadata |
| `data/figure_inputs/` | Small curated CSVs for exact final panels | Commit when lightweight |
| `docs/` | Data inventory, figure plan, structure notes | Commit |
| `figures/` | One executable script per manuscript figure | Commit |
| `latex/figures/` | PGFPlots sources for publication-quality figure panels | Commit |
| `notebooks/` | Exploration and diagnostics | Commit only lightweight notebooks |
| `outputs/figures/` | Regenerated publication figures | Keep local; commit only `.gitkeep` |
| `outputs/tables/` | Regenerated tables | Keep local; commit only `.gitkeep` |
| `scripts/` | Repository-level checks and orchestration | Commit |
| `src/tc_size_rainfall/` | Reusable Python package code | Commit |
| `tests/` | Smoke and structural tests | Commit |

## Enforced checks

Run:

```bash
python scripts/validate_repository.py
```

The validator checks that:

- required directories and files exist;
- local-only data/output directories retain `.gitkeep` placeholders;
- `figures/figure_manifest.json` is valid JSON;
- each manifest script exists;
- each manifest entry declares required inputs and outputs;
- `scripts/run_all_figures.py` uses the same figure order as the manifest;
- tracked files under `data/` and `outputs/` do not include large scientific
  artifacts, except curated CSVs under `data/figure_inputs/`.

## Current audit result

As of this structure update, the layout is present and machine-validated. The
remaining reproducibility gap is scientific completeness: Figure 2 has a Python
plotting path, Figures 1, 2, and 4 have PGFPlots sources, and the remaining
figure scripts still need final data-loading, analysis, and plotting routines as
processed inputs become available.
