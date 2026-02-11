import matplotlib.pyplot as pp
import rasterio as rio
import geopandas as gpd
import numpy as np
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import urllib.request as ureq
from datetime import datetime
from pyproj import CRS
import pygrib
import glob
import netCDF4 as nc
import shapely
from shapely.geometry import Point, LineString, Polygon

storm_data = pd.read_csv('storm_data_search_results.csv')

Tornado = gpd.read_file('storm_data_search_results.csv')
print(Tornado.columns)

map_crs = ccrs.PlateCarree()
data_crs = ccrs.PlateCarree()

mask1 = storm_data['TOR_F_SCALE'].values == 'EF4' 
mask2 = storm_data['TOR_F_SCALE'].values == 'EF3'
mask3 = storm_data['TOR_F_SCALE'].values == 'EF2'

test_points = []
lines = []

for i, entry in enumerate(storm_data[mask1].iterrows()):
    point = Point([(storm_data['BEGIN_LON'][i], storm_data['BEGIN_LAT'][i])])
    point2 = Point([(storm_data['END_LON'][i], storm_data['END_LAT'][i])])
    line = LineString([point, point2])
    lines.append(line)

for i, entry in enumerate(storm_data[mask2].iterrows()):
    point = Point([(storm_data['BEGIN_LON'][i], storm_data['BEGIN_LAT'][i])])
    point2 = Point([(storm_data['END_LON'][i], storm_data['END_LAT'][i])])
    line = LineString([point, point2])
    lines.append(line)

for i, entry in enumerate(storm_data[mask3].iterrows()):
    point = Point([(storm_data['BEGIN_LON'][i], storm_data['BEGIN_LAT'][i])])
    point2 = Point([(storm_data['END_LON'][i], storm_data['END_LAT'][i])])
    line = LineString([point, point2])
    test_points.append(point)
    lines.append(line)

#for a in lines:
#    print(a)
#    print(type(a))
#print(lines)
#print(len(lines))


fig,ax = pp.subplots(subplot_kw={"projection": map_crs}, constrained_layout=True)
ax.add_feature(cfeature.STATES)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS)
#ax.add_geometries(lines, crs=ccrs.PlateCarree(),linewidth=200)
ax.plot(*line.xy, color="blue")
ax.set_extent([-125, -70, 25, 50], crs = ccrs.PlateCarree())
ax.set_title(f"March 14, 2025 Significant Tornadoes", fontsize=10, fontweight='bold')

pp.savefig('Stippich_tornado_March_14.png')
pp.close()