# Make satellite imagery for the fires

# Import Modules
import rasterio as rio
import matplotlib.pyplot as plt
import geopandas as gpd
import shapely
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import numpy as np
from pyproj import CRS

sat = rio.open('CampFireData/camp_fire_20180719_L8_refl.tif') # Land reflectivity, not radar reflectivity
#print('Bands:',sat.indexes)
#print(sat.crs) # gives an ESRI
#print(sat.bounds) # gives 

rgb = np.stack([sat.read(3),sat.read(2),sat.read(1)],axis=-1) # (red, green, blue)

# sat_crs = CRS.from_epsg(102039) # --> this gives an error! have to look up the ESRI, find the EPSG (which is Albers), and make the crs
# sat_crs = CRS.from_epsg(4269) # --> works, but their servers are often down, so better to make the Albers yourself
#print(sat_crs.name)

sat_crs = ccrs.AlbersEqualArea(central_longitude=-96,central_latitude=23,standard_parallels=(29.5,45.5))
sat_extent = (sat.bounds.left,sat.bounds.right,sat.bounds.bottom,sat.bounds.top)

fire_crs = ccrs.AlbersEqualArea(central_longitude=-96,central_latitude=23,standard_parallels=(29.5,45.5))

# Read in the shape flie
fire = gpd.read_file('CampFireData/camp_fire_20180719_20190722_burn_bndy.shp')
fire_geoms = list(fire['geometry'])

fig, ax = plt.subplots(constrained_layout=True,subplot_kw={'projection':fire_crs})
ax.imshow((rgb/255.0)**0.7,extent=sat_extent,transform=sat_crs) # reads in Red Band, then scales it from 0 to 1, and finally applies a gamma of 0.7

# Fancy Plot
ax.add_feature(cfeature.STATES)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.OCEAN)

# Fire Geometries
for f, c in zip(fire_geoms,['red','blue','green','yellow']):
    ax.add_geometries(f,fire_crs, facecolor='none',edgecolor=c) # Function to add LIST of shapes
    #ax.scatter(f.centroid.x,f.centroid.y,transform=fire_crs,color='black',s=8,zorder=10)
plt.savefig('fancy.png')