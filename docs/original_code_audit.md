# Original code audit

Source folder reviewed:

`C:\Users\adolf\Documents\trabajos_coding_phd\Figures_Article_Size_Pcp`

The original folder contains the working code and intermediate products used to
generate the article figures. It should be treated as migration source material,
not copied wholesale into the reproducible repository.

## Repository impact

| Group | Keep in Git? | Rationale |
|---|---|---|
| Figure notebooks and Python scripts | Yes, after refactoring into `figures/`, `scripts/`, and `src/` | They encode the scientific workflow and plotting decisions |
| Small final-panel tables such as `data_pgfplots/*.csv` | Yes, under `data/figure_inputs/` | They are lightweight and improve exact figure reproduction |
| Massive or derived data such as `pcp_por_posicion/` and gridded NetCDF files | No | They are large reproducible intermediates or licensed external data |

## Useful source files by purpose

| Purpose | Original files | Migration target |
|---|---|---|
| Track cleanup and size distributions | `1_figure_size_distribution.ipynb`, `FIGURE_1_BOXPLOT_TENDENCIAS.ipynb`, `funciones_ape.py` | `src/tc_size_rainfall/tracks.py`, `figures/fig01_structure_boxplots.py` |
| Radial rainfall profiles | `procesar_cuenca.py`, `procesar_cuadrantes.py`, `radios_pcp.ipynb`, `radios_cuadrantes_pcp.ipynb`, `Figure_3_ perfiles_precipitacion.ipynb` | `src/tc_size_rainfall/precipitation.py`, `figures/fig02_radial_profiles.py` |
| Seasonal/category rainfall summaries | `FIGURE_2.ipynb`, `agrupar_csv.py`, `agrup_cat.py`, `PCP_TEMP.py` | Processing script plus `figures/fig03_seasonal_maps.py` |
| Radius versus precipitation | `FIGURA_7.ipynb`, `pcp_por_pos.py`, `pcpmeanbypos.py`, `acum_per_position.py`, `acum_per_ct.py` | `src/tc_size_rainfall/precipitation.py`, `figures/fig04_radius_precip_scatter.py` |
| Extreme precipitation | `Calcular_extremos_p95.ipynb`, `extremos.py`, `PCP_TEMP_extremos.py`, `FIGURE_4-5.ipynb` | `src/tc_size_rainfall/extremes.py`, `figures/fig05_extreme_radial_quadrants.py`, `figures/fig06_extreme_distance_histograms.py` |
| TC structure trends | `tendencias.py`, `FIGURE_1_BOXPLOT_TENDENCIAS.ipynb`, `resultados/tendencias_bootstrap*.csv` | `src/tc_size_rainfall/stats.py`, `figures/fig07_structure_trends.py` |
| SST, shear, q, omega composites | `SST_WSHEAR.py`, `SST_WSHEAR_anomalias_mensual.py`, `VERT_COMP.py`, `mensual_SST.py`, `climatologia_vertical_q_por_region.py`, `anomalias_verticales_q.py`, `fig_compuestos_sst_q.py`, `FIGURES_8_9.ipynb` | Future `src/tc_size_rainfall/environment.py`, `figures/fig08_environment_composites_r1_r2.py`, `figures/fig09_environment_composites_r3_r4.py` |
| GLORYS mixed-layer-depth composites | `GLORYS_MLD_CT_pipeline.py`, `GLORYS_MLD_anomaly.py`, `FIGURES_GLORYS.py`, `FIGURES_ANOMALIES_GLORYS.py` | Future `src/tc_size_rainfall/mld.py`, `figures/fig10_mld_anomalies.py` |

## First migration completed

The following reusable pieces have been ported out of notebook/script state:

- `src/tc_size_rainfall/tracks.py`: track column normalization, 6-hour filtering,
  datetime construction, and quadrant-radius validation.
- `src/tc_size_rainfall/precipitation.py`: MSWEP filename convention,
  gridded-precipitation point conversion, quadrant clipping, and radial profiles.
- `src/tc_size_rainfall/extremes.py`: p95 threshold loading, exceedance marking,
  and storm metadata attachment.
- `scripts/prepare_pgfplots_inputs.py`: extracts lightweight Figure 1 boxplot
  summaries and Figure 4 scatterplot inputs from the original local data
  products.
- `latex/figures/fig01_structure_boxplots.tex`,
  `latex/figures/fig02_radial_profiles.tex`, and
  `latex/figures/fig04_radius_precip_scatter.tex`: PGFPlots sources for the
  figures that benefit from LaTeX rendering.

These modules are covered by focused tests with small synthetic inputs.

## Data migration notes

Migrated lightweight figure inputs:

- `data_pgfplots/EPcat.csv` -> `data/figure_inputs/EPcat.csv`
- `data_pgfplots/EPcat_wide.csv` -> `data/figure_inputs/EPcat_wide.csv`
- `data_pgfplots/EPQ.csv` -> `data/figure_inputs/EPQ.csv`
- `data_pgfplots/EPQ_wide.csv` -> `data/figure_inputs/EPQ_wide.csv`
- `data_pgfplots/NAcat.csv` -> `data/figure_inputs/NAcat.csv`
- `data_pgfplots/NAcat_wide.csv` -> `data/figure_inputs/NAcat_wide.csv`
- `data_pgfplots/NAQ.csv` -> `data/figure_inputs/NAQ.csv`
- `data_pgfplots/NAQ_wide.csv` -> `data/figure_inputs/NAQ_wide.csv`
- `db/dfna.csv` and `db/dfep.csv` -> `data/figure_inputs/fig01_boxplot_stats.csv`
  and `data/figure_inputs/fig01_category_counts.csv` via
  `scripts/prepare_pgfplots_inputs.py`
- `acumulado_total_por_posicion/acumulado_total_na.csv`,
  `acumulado_total_por_posicion/acumulado_total_ep.csv`, `db/dfna.csv`, and
  `db/dfep.csv` -> `data/figure_inputs/fig04_radius_precip_scatter.csv` and
  `data/figure_inputs/fig04_scatter/*.csv` via
  `scripts/prepare_pgfplots_inputs.py`

Good candidates to commit after separate review:

- compact summaries from `resultados/tendencias_bootstrap*.csv` if final figures
  depend on them directly.

Do not commit:

- `pcp_por_posicion/` (~9 GB, 13,582 per-position CSV files);
- `resultados_extremos_total_*.csv` (~100 MB combined);
- NetCDF/GRIB/GeoTIFF/HDF/Zarr scientific data products;
- shapefile bundles that can be replaced by Cartopy/Natural Earth downloads or
  documented external references.

## Refactoring rules for the remaining migration

1. Replace hard-coded paths such as `D:\Descargas_Copernicus` and
   `G:\Mi unidad\Descargas_Copernicus` with parameters from
   `tc_size_rainfall.config`.
2. Keep data generation in `scripts/` and pure reusable logic in `src/`.
3. Keep each `figures/figXX_*.py` focused on reading prepared inputs and drawing
   the final panel.
4. Preserve original output filenames only in manifests or compatibility notes;
   final repository outputs should use `outputs/figures/figXX_*.png/pdf`.
5. Add tests around reusable math before replacing a placeholder figure script.
