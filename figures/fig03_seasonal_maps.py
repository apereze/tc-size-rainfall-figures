import matplotlib.pyplot as plt
import cartopy.crs as ccrs

from tc_size_rainfall.config import FIGURE_DIR
from tc_size_rainfall.geospatial import middle_americas_axis
from tc_size_rainfall.plotting import save_figure, set_paper_style

set_paper_style()

# TODO:
# Build 3 x 5 seasonal map panel:
# precipitation, Rp, asymmetry, solidity, dispersion
# for May-Jun, Jul-Sep, Oct-Nov.

fig = plt.figure(figsize=(12, 7))
ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
middle_americas_axis(ax)
ax.set_title("Figure 3 placeholder")

save_figure(fig, FIGURE_DIR / "fig03_seasonal_maps.png")
