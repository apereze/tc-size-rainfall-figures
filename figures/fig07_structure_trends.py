import matplotlib.pyplot as plt
import cartopy.crs as ccrs

from tc_size_rainfall.config import FIGURE_DIR
from tc_size_rainfall.geospatial import middle_americas_axis
from tc_size_rainfall.plotting import save_figure, set_paper_style

set_paper_style()

# TODO:
# Map annual trends in Rp, S, A, D using bootstrap OLS.
# Add subregion boxes R1-R4 and category-frequency bar plots.

fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
middle_americas_axis(ax)
ax.set_title("Figure 7 placeholder")

save_figure(fig, FIGURE_DIR / "fig07_structure_trends.png")
