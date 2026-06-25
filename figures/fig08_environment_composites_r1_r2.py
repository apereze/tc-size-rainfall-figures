import matplotlib.pyplot as plt

from tc_size_rainfall.config import FIGURE_DIR
from tc_size_rainfall.plotting import save_figure, set_paper_style

set_paper_style()

# TODO:
# Composite SST + vertical wind shear maps and q + omega sections
# for R1 and R2.

fig, ax = plt.subplots(figsize=(8, 4))
ax.text(0.5, 0.5, "Figure 8 placeholder", ha="center", va="center")
ax.set_axis_off()

save_figure(fig, FIGURE_DIR / "fig08_environment_composites_r1_r2.png")
