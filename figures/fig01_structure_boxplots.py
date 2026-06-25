import matplotlib.pyplot as plt
import seaborn as sns

from tc_size_rainfall.config import FIGURE_DIR
from tc_size_rainfall.plotting import save_figure, set_paper_style

set_paper_style()

# TODO:
# 1. Read processed table with quadrant radii and structural metrics.
# 2. Create upper panels for RNE, RNW, RSW, RSE by basin/category.
# 3. Create lower panels for Asymmetry, Dispersion, Solidity.
# 4. Export to outputs/figures/fig01_structure_boxplots.png/pdf.

fig, ax = plt.subplots(figsize=(8, 4))
ax.text(0.5, 0.5, "Figure 1 placeholder", ha="center", va="center")
ax.set_axis_off()

save_figure(fig, FIGURE_DIR / "fig01_structure_boxplots.png")
