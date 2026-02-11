# Ethan Palmisano
# MET-330
# Dr. Christopher Phillips
# 17 November 2025
# I have neither given or receieved nor have I tolerated others' use of unauthorized aid.

# Instructions: Download a NAM weather model file for 12Z on June 13th, 2022. Then create the following plots:
# a) a map of the 500 mb geopotential heights as black contours, the wind as barbs, and the
# absolute vorticity as a filled contour.
# b) a map of the 850 mb geopotential heights as black contours, the wind as barbs, and the
# temperature as a filled contour.

# Import Modules
import urllib.request as ureq
import pygrib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# Download Grib2 File and Index
user_date = '2022061312'
url = f'https://noaa-nam-pds.s3.amazonaws.com/nam.{user_date[0:8]}/nam.t{user_date[8:10]}z.awphys00.tm00.grib2'
index = f'https://noaa-nam-pds.s3.amazonaws.com/nam.{user_date[0:8]}/nam.t{user_date[8:10]}z.awphys00.tm00.grib2.idx'
grb = ureq.urlretrieve(url, f'nam_{user_date[0:8]}.grib2')
index = ureq.urlretrieve(index, f'nam_{user_date[0:8]}.grib2.idx')
grbs = pygrib.open(f'nam_{user_date[0:8]}.grib2')

# Read in Data
hght_500 = grbs.select(name='Geopotential height',level=500)[0].values
hght_850 = grbs.select(name='Geopotential height',level=850)[0].values
uwnd_500 = grbs.select(name='U component of wind',level=500)[0].values*1.94384
vwnd_500 = grbs.select(name='V component of wind',level=500)[0].values*1.94384
uwnd_850 = grbs.select(name='U component of wind',level=850)[0].values*1.94384
vwnd_850 = grbs.select(name='V component of wind',level=850)[0].values*1.94384
absv_500 = grbs.select(name='Absolute vorticity',level=500)[0].values
temp_850 = grbs.select(name='Temperature',level=850)[0] # don't make an array yet so we can get lats, lons, and time
lats, lons = temp_850.latlons()
time = temp_850.validDate
temp_850 = temp_850.values-273.15

# Set Projections
map_crs = ccrs.PlateCarree()
data_crs = ccrs.PlateCarree()

# Plot 1
fig, ax = plt.subplots(constrained_layout=True,subplot_kw={'projection':map_crs})

ax.set_extent([-130,-65,20,50])

cntr = ax.contour(lons,lats,hght_500,colors=['black'],transform=data_crs)
ax.clabel(cntr, fontsize=10)

#absv_mask = absv_500<=(-10**-4)

cfill = ax.contourf(lons,lats,absv_500,cmap='PuOr_r',transform=data_crs)
cb = fig.colorbar(cfill, ax=ax, orientation='horizontal')
#cfill2 = ax.contourf(lons,lats,absv_500,cmaps='Purples_r',transform=data_crs)

# make sure that both x and y are indexed
ax.barbs(lons[::60,::60],lats[::60,::60],uwnd_500[::60,::60],vwnd_500[::60,::60],color='black',transform=data_crs)

ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.STATES)

fig.suptitle(f'500 mb Absolute Vorticity - {user_date[4:6]}-{user_date[6:8]}-{user_date[0:4]} {user_date[8:10]}z')

plt.savefig('nam_500_plot.png')


# Plot 2
fig, ax = plt.subplots(constrained_layout=True,subplot_kw={'projection':map_crs})

ax.set_extent([-130,-65,20,50])

cntr = ax.contour(lons,lats,hght_850,colors=['black'],transform=data_crs)
ax.clabel(cntr, fontsize=10)

#absv_mask = absv_500<=(-10**-4)

cfill = ax.contourf(lons,lats,temp_850,cmap='coolwarm',transform=data_crs)
cb = fig.colorbar(cfill, ax=ax, orientation='horizontal')
#cfill2 = ax.contourf(lons,lats,absv_500,cmaps='Purples_r',transform=data_crs)

# make sure that both x and y are indexed
ax.barbs(lons[::60,::60],lats[::60,::60],uwnd_850[::60,::60],vwnd_850[::60,::60],color='black',transform=data_crs)

ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.STATES)

fig.suptitle(f'850 mb Temperature (C) - {user_date[4:6]}-{user_date[6:8]}-{user_date[0:4]} {user_date[8:10]}z')

plt.savefig('nam_850_plot.png')