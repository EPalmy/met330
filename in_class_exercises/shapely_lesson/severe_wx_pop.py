# Code for SPC Plot in class

# Import Modules
import geopandas as gpd
import pandas as pd
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import matplotlib as mpl
import shapely

# Read in Census from Phillips' Directory
phillips_path = '/storage/cphill19/met330_data/'
pop = pd.read_csv(phillips_path+'nhgis0003_ds258_2020_county.csv')
census = gpd.read_file(phillips_path+'nhgis0001_shapefile_tl2020_us_county_2020.zip')
census = census.merge(pop, on='GISJOIN') # merge two datasets since they have the same number of rows and have a similar column

### print(census.columns) 
# Index(['GISJOIN', 'STATEFP', 'COUNTYFP', 'COUNTYNS', 'GEOID_x', 'NAME_x',
#       'NAMELSAD', 'LSAD', 'CLASSFP', 'MTFCC', 'CSAFP', 'CBSAFP', 'METDIVFP',
#       'FUNCSTAT_x', 'ALAND', 'AWATER', 'INTPTLAT_x', 'INTPTLON_x',
#       'Shape_Leng', 'Shape_Area', 'geometry', 'YEAR', 'STUSAB', 'GEOID_y',
#       'GEOCODE', 'REGIONA', 'DIVISIONA', 'STATE', 'STATEA', 'COUNTY',
#       'COUNTYA', 'COUSUBA', 'COUSUBCC', 'SUBMCDA', 'CONCITA', 'PLACEA',
#       'PLACECC', 'TRACTA', 'BLKGRPA', 'BLOCKA', 'AIANHHA', 'RES_ONLYA',
#       'TRUSTA', 'AIANHHCC', 'AITSA', 'TTRACTA', 'TBLKGRPA', 'ANRCA', 'CBSAA',
#       'MEMI', 'CSAA', 'METDIVA', 'NECTAA', 'NMEMI', 'CNECTAA', 'NECTADIVA',
#       'CBSAPCI', 'NECTAPCI', 'UAA', 'URA', 'CD116A', 'SLDU18A', 'SLDL18A',
#       'VTD', 'VTDI', 'ZCTAA', 'SDELMA', 'SDSECA', 'SDUNIA', 'PUMA',
#       'AREALAND', 'AREAWATR', 'BASENAME', 'NAME_y', 'FUNCSTAT_y',
#       'INTPTLAT_y', 'INTPTLON_y', 'LSADC', 'UGA', 'U7H001'], # U7H001 is the one we want for population
#      dtype='object')

census_crs = ccrs.AlbersEqualArea(central_longitude=-96,central_latitude=37.5,standard_parallels=(29.5,45.5))
map_crs = census_crs

# Set SPC Date
date = input('Input Date in YYYYMMDDHHmm: ')
if date == 'test':
    date = '202405211200'
spc_url = f'https://www.spc.noaa.gov/products/outlook/archive/{date[0:4]}/day1otlk_{date[0:8]}_{date[8:12]}-shp.zip'

risk = gpd.read_file(spc_url)
risk = risk.to_crs(census_crs)

spc_crs = ccrs.PlateCarree()

geoms = risk['geometry']
mod_risk = geoms.geometry[4]

fig, ax = plt.subplots(constrained_layout=True,subplot_kw={'projection':map_crs}) # using the county crs, as this will save it from transforming all 3000 counties

ax.set_extent([-130, -65, 25, 50],crs=ccrs.PlateCarree())

cmap = mpl.colormaps['plasma']
colors = cmap(np.log(census.U7H001)/np.log(np.nanmax(census.U7H001)))

mesh = ax.add_geometries(census.geometry, census_crs,facecolor=colors,linewidth=0.25,cmap='plasma')

# Create a colorbar
ticklabels = np.array([1,10,100,1000,10000,100000,1000000])
ticks = np.log(ticklabels)/np.log(np.nanmax(census.U7H001))
cb = fig.colorbar(mesh, orientation='horizontal',pad=0.02)
cb.set_ticks(ticks)
cb.set_ticklabels(ticklabels, rotation=30)
cb.set_label('Population',fontsize=14,fontweight='bold')

for row in risk.itertuples():
    ax.add_geometries([row.geometry],census_crs,edgecolor=row.stroke,facecolor=row.fill,alpha=0.7)
    # Add a LEGEND using a ghost point for legend purposes
    ax.scatter(0,0,c=row.stroke,marker='s',label=row.LABEL,alpha=0.7)
    total_pop = 0
    for county, pop in zip(census.geometry[:],census.U7H001[:]):
        if (shapely.contains(row.geometry,county)):
            total_pop += pop
    print(row.LABEL, total_pop)
            #print(pop)

ax.add_feature(cfeature.STATES,linewidth=0.5)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.OCEAN)

ax.legend(loc='lower left')


plt.savefig('yayay.png')