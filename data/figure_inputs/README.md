# Figure inputs

This directory is for small, curated CSV files that directly reproduce final
figure panels, such as PGFPlots tables or compact statistical summaries.

Do not place raw gridded data, per-position precipitation CSVs, NetCDF files, or
large intermediate products here. Those stay local under `data/raw/`,
`data/interim/`, `data/processed/`, or `data/external/`.

Committed inputs currently include:

- `NAQ.csv`, `EPQ.csv`, `NAcat.csv`, and `EPcat.csv`: long radial rainfall
  profiles migrated from the original `data_pgfplots/` folder.
- `*_wide.csv`: the same radial profiles pivoted for PGFPlots.
- `fig01_boxplot_stats.csv`: prepared boxplot statistics for the TC structural
  variables in Figure 1.
- `fig01_category_counts.csv`: sample counts by basin and intensity category
  used to audit Figure 1.
- `fig04_radius_precip_scatter.csv`: merged radius/accumulated-precipitation
  table for the scatterplot.
- `fig04_scatter/*.csv`: basin/category partitions used directly by the Figure
  4 PGFPlots source.
