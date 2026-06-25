import matplotlib.pyplot as plt

from tc_size_rainfall.config import FIGURE_DIR
from tc_size_rainfall.plotting import save_figure, set_paper_style

set_paper_style()

# TODO:
# 1. Read radial profile table.
# 2. Plot quadrant profiles for NA and EP.
# 3. Plot category profiles for NA and EP.
# 4. Use 50 km ring spacing.

fig, ax = plt.subplots(figsize=(8, 4))
ax.text(0.5, 0.5, "Figure 2 placeholder", ha="center", va="center")
ax.set_axis_off()

save_figure(fig, FIGURE_DIR / "fig02_radial_profiles.png")
