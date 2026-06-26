# LaTeX figures

This directory contains PGFPlots sources for figures that benefit from direct
LaTeX rendering.

Current PGFPlots figures:

- `figures/fig01_structure_boxplots.tex`
- `figures/fig02_radial_profiles.tex`
- `figures/fig04_radius_precip_scatter.tex`

Compile from the repository root so relative data paths resolve, for example:

```bash
pdflatex -output-directory outputs/figures latex/figures/fig02_radial_profiles.tex
```

The data sources live in `data/figure_inputs/`. Regenerate derived PGFPlots
inputs with:

```bash
python scripts/prepare_pgfplots_inputs.py --source-dir C:\path\to\Figures_Article_Size_Pcp
```

Or compile every LaTeX figure listed above:

```bash
python scripts/render_latex_figures.py
```
