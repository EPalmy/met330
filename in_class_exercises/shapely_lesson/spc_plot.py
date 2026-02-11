# Code for SPC Plot in class

# Import Modules
import geopandas as gpd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt

date = input('Input Date in YYYYMMDDHHmm: ')
if date == 'test':
    date = '202405211200'
spc_url = f'https://www.spc.noaa.gov/products/outlook/archive/{date[0:4]}/day1otlk_{date[0:8]}_{date[8:12]}-shp.zip'

risk = gpd.read_file(spc_url)
print(risk)

spc_crs = ccrs.PlateCarree()

geoms = risk['geometry']

fig, ax = plt.subplots(constrained_layout=True,subplot_kw={'projection':spc_crs})

ax.set_extent([-130, -65, 25, 50])

for row in risk.itertuples():
    ax.add_geometries([row.geometry],spc_crs,edgecolor=row.stroke,facecolor=row.fill,alpha=0.7)
    # Add a LEGEND using a ghost point for legend purposes
    ax.scatter(0,0,c=row.stroke,marker='s',label=row.LABEL,alpha=0.7)

ax.add_feature(cfeature.STATES,linewidth=0.5)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.OCEAN)

ax.legend()

plt.savefig('yay.png')