# Ethan Palmisano
# MET-330
# Dr. Christopher Phillips
# 23 October 2025
# I have neither given or receieved nor have I tolerated others' use of unauthorized aid.

# Instructions: Make a plot of Hurricane Idalia (August 30, 2023 at 12 UTC) with a user input.
# This plot should use composite reflectivity and a variable of your choosing.

# Import Modules
import urllib.request as ureq
import pygrib
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

user_date = input('Please input a date in YYYYMMDDhh format in UTC format: ')
date = datetime.strptime(user_date, "%Y%m%d%H")

if len(user_date) != 10: # Make sure it will not break the code
    print('Please input date in correct format.')
    exit()

# Download Grib2 File and Index
url = f'https://noaa-nam-pds.s3.amazonaws.com/nam.{user_date[0:8]}/nam.t{user_date[8:10]}z.awphys00.tm00.grib2'
index = f'https://noaa-nam-pds.s3.amazonaws.com/nam.{user_date[0:8]}/nam.t{user_date[8:10]}z.awphys00.tm00.grib2.idx'
grb = ureq.urlretrieve(url, f'nam_{user_date[0:8]}.grib2')
index = ureq.urlretrieve(index, f'nam_{user_date[0:8]}.grib2.idx')
grbs = pygrib.open(f'nam_{user_date[0:8]}.grib2')

data_proj = ccrs.PlateCarree()
map_proj = ccrs.PlateCarree()

# Composite Reflectivity Data, and other Info
grb = grbs.select(name='Maximum/Composite radar reflectivity')[0]
grb2 = grbs.select(name='Precipitable water')[0]
data = grb.values
mask = data<10
data[mask] = np.nan
data2 = grb2.values
lats, lons = grb.latlons()
time = grb.validDate

# Make the plot
fig, ax = plt.subplots(subplot_kw={'projection':map_proj},constrained_layout=True)
ax.set_extent([-130,-65,20,50])

mesh = ax.pcolormesh(lons,lats,data,cmap='turbo',transform=data_proj)
cntr = ax.contour(lons,lats,data2,colors=['green'],transform=data_proj)
ax.clabel(cntr, fontsize=10)
cb = fig.colorbar(mesh, ax=ax, orientation='vertical')
cb.set_label(f'{grb.name} ({grb.units})', fontsize=14)

ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.STATES)

fig.suptitle(f'{date:%Y%m%d} {date:%H}z Precipitable Water {grb2.units}')

plt.savefig(f'nam_{grb.name.replace('/','').replace(' ','')}.png') # added slash so it doesn't get messed up due to the maximum/composite thing
plt.close()