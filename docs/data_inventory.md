# Data inventory

Use this document to record local data sources, paths, versions, checksums, and
preprocessing status. Large data files should remain local and should not be
committed to GitHub.

| Dataset | Purpose | Native format | Local path | Version/date | Checksum or DOI | Status |
|---|---|---|---|---|---|---|
| HURDAT2 / IBTrACS | TC tracks, intensity, position | CSV | `data/raw/` | pending | pending | pending |
| ROCLOUD | TC quadrant size and structural metrics | CSV/Parquet | `data/raw/` | pending | pending | pending |
| MSWEP V2 | Precipitation | NetCDF | `data/raw/` | pending | pending | pending |
| ERA5 | SST, wind, humidity, omega | NetCDF/GRIB | `data/raw/` | pending | pending | pending |
| GLORYS | Mixed layer depth | NetCDF | `data/raw/` | pending | pending | pending |
| PGFPlots radial-profile tables | Final lightweight panel inputs | CSV | `data/figure_inputs/` | migrated from original code folder | local source | migrated |
| Figure 1 PGFPlots boxplot summaries | Final lightweight panel inputs | CSV | `data/figure_inputs/fig01_*.csv` | generated from original `db/dfna.csv` and `db/dfep.csv` | local source | migrated |
| Figure 4 PGFPlots scatter tables | Final lightweight panel inputs | CSV | `data/figure_inputs/fig04_*.csv` and `data/figure_inputs/fig04_scatter/` | generated from original radius and precipitation summaries | local source | migrated |

## Minimum metadata for each dataset

- Source URL, DOI, or access instructions.
- Download date or dataset version.
- Native spatial and temporal resolution.
- Local filename pattern.
- Processing script that converts it into `data/processed/`.
- Checksum for any immutable input file when practical.
