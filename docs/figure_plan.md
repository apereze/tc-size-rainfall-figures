# Figure reproduction plan

`figures/figure_manifest.json` is the machine-readable source of truth for
script, input, and output paths. This document records the scientific intent for
each figure.

## Figure 1

Input: ROCLOUD/HURDAT merged table.
Output: boxplots of quadrant radii and structural metrics.
Current reproducible route: `scripts/prepare_pgfplots_inputs.py` reads the
original `db/dfna.csv` and `db/dfep.csv`, writes prepared statistics to
`data/figure_inputs/fig01_boxplot_stats.csv`, and generates the PGFPlots source
`latex/figures/fig01_structure_boxplots.tex`.

## Figure 2

Input: radial precipitation profiles computed with 50 km rings.
Output: line plots by quadrant and intensity category.
Current reproducible route: compact CSVs from the original `data_pgfplots/`
folder are committed under `data/figure_inputs/`. The figure can be drawn with
either `figures/fig02_radial_profiles.py` or
`latex/figures/fig02_radial_profiles.tex`.

## Figure 3

Input: gridded seasonal means.
Output: 3 x 5 seasonal maps.

## Figure 4

Input: synoptic-position table with mean radius and accumulated precipitation.
Output: scatterplots by basin and intensity category.
Current reproducible route: `scripts/prepare_pgfplots_inputs.py` merges
`db/dfna.csv`, `db/dfep.csv`, and
`acumulado_total_por_posicion/acumulado_total_*.csv`, then writes the combined
and basin/category-partitioned CSVs used by
`latex/figures/fig04_radius_precip_scatter.tex`.

## Figure 5

Input: extreme precipitation events with radial distance and quadrant.
Output: radial/quadrant percentage plot.

## Figure 6

Input: extreme precipitation event table.
Output: histograms and boxplots of distance from TC center.

## Figure 7

Input: annual gridded structural metrics.
Output: maps of trend slopes and significance.

## Figures 8-9

Input: ERA5 storm-centered composites by region.
Output: SST/shear maps and vertical q/omega sections.

## Figure 10

Input: GLORYS MLD anomalies composited by region.
Output: MLD anomaly maps.
