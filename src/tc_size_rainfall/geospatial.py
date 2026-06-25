import cartopy.crs as ccrs
import cartopy.feature as cfeature


def middle_americas_axis(ax):
    """Configure a Cartopy axis for the Middle Americas domain."""
    ax.set_extent([-130, -60, 5, 35], crs=ccrs.PlateCarree())
    ax.coastlines(linewidth=0.7)
    ax.add_feature(cfeature.BORDERS, linewidth=0.4)
    ax.add_feature(cfeature.LAND, alpha=0.2)
    ax.add_feature(cfeature.OCEAN, alpha=0.1)
    gl = ax.gridlines(draw_labels=True, linewidth=0.3, alpha=0.5)
    gl.top_labels = False
    gl.right_labels = False
    return ax
