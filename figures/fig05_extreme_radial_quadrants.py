import matplotlib.pyplot as plt

from tc_size_rainfall.config import FIGURE_DIR
from tc_size_rainfall.plotting import save_figure, set_paper_style

set_paper_style()

# TODO:
# Plot radial-quadrant distribution of extreme precipitation events
# in 200 km rings, stratified by basin and category.

fig, ax = plt.subplots(figsize=(6, 6))
ax.text(0.5, 0.5, "Figure 5 placeholder", ha="center", va="center")
ax.set_axis_off()

save_figure(fig, FIGURE_DIR / "fig05_extreme_radial_quadrants.png")
