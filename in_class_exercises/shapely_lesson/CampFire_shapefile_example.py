# Learning Shapely using Burn Data

# Import Modules
import geopandas as gpd
import shapely
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import numpy as np

#print(fire.crs) --> this will print the info needed for fire_crs
#print(fire.iloc[0]) ### takes a single one of the shapes
fire_crs = ccrs.AlbersEqualArea(central_longitude=-96,central_latitude=23,standard_parallels=(29.5,45.5))

# Read in the shape flie
fire = gpd.read_file('CampFireData/camp_fire_20180719_20190722_burn_bndy.shp')

fire_geoms = list(fire['geometry'])

for i, geom in enumerate(fire_geoms):
    print(f'geometry {i}')
    print(f'Center of the fire scar: {geom.centroid}') # in meters, in ALBERS
    print(f'Area of the fire scar: {geom.area:.2f} m^2')
    print(f'Perimeter of the fire scar: {geom.length:.2f} m')
    print('--------------------')


# Plotting Code
map_crs = fire_crs
fig, ax = plt.subplots(constrained_layout=True,subplot_kw={'projection':map_crs}) # projection --> what everything is converted to

#bounds = [-130,-110,35,45] # old bounds, these show the state lines and stuff
bounds = [-121.8,-121.3,39.6,39.9]

ax.set_extent(bounds,crs=ccrs.PlateCarree())

# Fancy Plot
ax.add_feature(cfeature.STATES)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.OCEAN)

# Fire Geometries
for f, c in zip(fire_geoms,['red','blue','green','yellow']):
    ax.add_geometries(f,fire_crs, color=c) # Function to add LIST of shapes
    ax.scatter(f.centroid.x,f.centroid.y,transform=fire_crs,color='black',s=8,zorder=10)
    #print(f.bounds)
plt.savefig('campfire_shape.png')