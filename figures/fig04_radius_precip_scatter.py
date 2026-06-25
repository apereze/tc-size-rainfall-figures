import matplotlib.pyplot as plt

from tc_size_rainfall.config import FIGURE_DIR
from tc_size_rainfall.plotting import save_figure, set_paper_style

set_paper_style()

# TODO:
# Scatter mean radius Rp vs accumulated precipitation,
# separated by basin and colored by intensity category.

fig, ax = plt.subplots(figsize=(7, 4))
ax.text(0.5, 0.5, "Figure 4 placeholder", ha="center", va="center")
ax.set_axis_off()

save_figure(fig, FIGURE_DIR / "fig04_radius_precip_scatter.png")
