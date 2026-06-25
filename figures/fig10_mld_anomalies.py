import matplotlib.pyplot as plt
import cartopy.crs as ccrs

from tc_size_rainfall.config import FIGURE_DIR
from tc_size_rainfall.geospatial import middle_americas_axis
from tc_size_rainfall.plotting import save_figure, set_paper_style

set_paper_style()

# TODO:
# Map MLD anomalies composited for R1-R4.

fig = plt.figure(figsize=(8, 5))
ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
middle_americas_axis(ax)
ax.set_title("Figure 10 placeholder")

save_figure(fig, FIGURE_DIR / "fig10_mld_anomalies.png")
