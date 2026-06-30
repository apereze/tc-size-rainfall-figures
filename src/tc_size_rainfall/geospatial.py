import cartopy.crs as ccrs
import cartopy.feature as cfeature

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import numpy as np


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

def configurar_mapa(ax, crs, lon_extent=(-120, -80), lat_extent=(10, 35), lon_extent_begin = 1,
                    lat_extent_begin= 1, linewidth=2, tick_width=3, tick_size=10, label_size=20,
                     grid_spacing=4, grid_color='w', grid_alpha=0.6, grid_linestyle='--',
                     land_color='lightgray', land_alpha=0.8,
                     lon_tick_spacing=4, lat_tick_spacing=4 ):
    """
    Configura los elementos comunes del mapa para un subplot ax.

    Parámetros:
    ax : objeto de ejes de Cartopy
        El subplot donde se dibujará el mapa.
    lon_extent : tuple
        Extensión longitudinal (mínimo, máximo).
    lat_extent : tuple
        Extensión latitudinal (mínimo, máximo).
    lon_extent_begin : float
        Valor inicial para la extensión longitudinal.
    lat_extent_begin : float
        Valor inicial para la extensión latitudinal.
    linewidth : float
        Grosor de las líneas de la costa y fronteras.
    tick_width : float
        Grosor de los ticks de los ejes.
    tick_size : float
        Tamaño de los ticks.
    label_size : float
        Tamaño de las etiquetas de los ejes.
    grid_spacing : int
        Espaciado entre las líneas de la cuadrícula.
    grid_color : str
        Color de las líneas de la cuadrícula.
    grid_alpha : float
        Transparencia de las líneas de la cuadrícula.
    grid_linestyle : str
        Estilo de las líneas de la cuadrícula.
    land_color : str
        Color de la superficie terrestre.
    land_alpha : float
        Transparencia de la superficie terrestre.
    lon_tick_spacing : float
        Espaciado entre los ticks del eje X (longitud).
    lat_tick_spacing : float
        Espaciado entre los ticks del eje Y (latitud).
    crs: Func
        Sistema de coordenadas de referencia (CRS) para el mapa.
    """
    # Añadir características geográficas
    ax.add_feature(cfeature.COASTLINE, linewidth=linewidth)
    ax.add_feature(cfeature.BORDERS, linewidth=linewidth)
    ax.add_feature(cfeature.LAND.with_scale('50m'), facecolor=land_color, alpha=land_alpha, zorder=0)

    # Configurar el grosor del borde del mapa y los ticks
    ax.spines['geo'].set_linewidth(tick_width)
    ax.tick_params(axis='both', width=tick_width, size=tick_size, which='both', labelsize=label_size)

    # Definir la extensión del mapa
    ax.set_extent([lon_extent[0], lon_extent[1], lat_extent[0], lat_extent[1]], crs)

    # Configurar los ticks de los ejes
    ax.set_xticks(np.arange(lon_extent[0], lon_extent[1] + lon_extent_begin, lon_tick_spacing), crs=crs)
    ax.set_yticks(np.arange(lat_extent[0]+ lat_extent_begin, lat_extent[1] + lat_extent_begin, lat_tick_spacing), crs=crs)
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())

    # Añadir líneas de cuadrícula
    ax.gridlines(draw_labels=False, linewidth=1, color=grid_color, alpha=grid_alpha, linestyle=grid_linestyle, zorder=3,
                 xlocs=np.arange(lon_extent[0], lon_extent[1] + 1, grid_spacing),
                 ylocs=np.arange(lat_extent[0], lat_extent[1] + 1, grid_spacing))