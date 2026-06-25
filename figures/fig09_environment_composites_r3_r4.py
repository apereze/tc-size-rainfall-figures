import matplotlib.pyplot as plt

from tc_size_rainfall.config import FIGURE_DIR
from tc_size_rainfall.plotting import save_figure, set_paper_style

set_paper_style()

# TODO:
# Same as Figure 8, but for R3 and R4.

fig, ax = plt.subplots(figsize=(8, 4))
ax.text(0.5, 0.5, "Figure 9 placeholder", ha="center", va="center")
ax.set_axis_off()

save_figure(fig, FIGURE_DIR / "fig09_environment_composites_r3_r4.png")
