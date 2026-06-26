# Data directory

This directory is for local data needed to regenerate manuscript figures.

- `raw/`: original downloaded or received datasets.
- `interim/`: temporary intermediate products.
- `processed/`: analysis-ready tables and grids consumed by figure scripts.
- `external/`: reference layers or external auxiliary data.
- `figure_inputs/`: small committed CSV inputs for exact final figure panels.

Large scientific files are intentionally ignored by Git. Record source,
version, checksum, and preprocessing notes in `docs/data_inventory.md`.
