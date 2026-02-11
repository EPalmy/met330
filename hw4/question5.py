# Ethan Palmisano
# MET-330
# Dr. Christopher Phillips
# 17 November 2025
# I have neither given or receieved nor have I tolerated others' use of unauthorized aid.

# Instructions: Compute the thermal wind for June 13th, 2022 at 12Z using the NAM file you have already downloaded.
# a) Compute the average temperature between 850 and 1000 mb.
# b) Use Numpy's gradient function to calculate the temperature gradient at each grid point.
# (NAM grid spacing is 12,000 m and be sure to convert temperature to Kelvin).
# c) Then, use the thermal wind equations to compute both vector components.
# d) Make a 4 panel plot showing the mean layer temperature, each component of the
# thermal wind, and the total speed of the thermal wind vector.

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
temp_850 = grbs.select(name='Temperature',level=850)[0]
temp_1000 = grbs.select(name='Temperature',level=1000)[0]
lats, lons = temp_850.latlons()
time = temp_850.validDate
temp_850 = temp_850.values#-273.15
temp_1000 = temp_1000.values#-273.15

av_temp = (temp_1000+temp_850)/2
grad = np.gradient(av_temp,12000)
grad_x = grad[0]
grad_y = grad[1]



map_crs = ccrs.PlateCarree()
data_crs = ccrs.PlateCarree()

fig, (ax1,ax2,ax3,ax4) = plt.subplots(subplot_kw={'projection':map_crs},constrained_layout=True,ncols=2,nrows=2)

ax1.set_extent([-130,-65,20,50])
ax2.set_extent([-130,-65,20,50])
ax3.set_extent([-130,-65,20,50])
ax4.set_extent([-130,-65,20,50])

cf1 = ax.contourf(lons,lats,av_temp,transform=data_crs,cmap='coolwarm')
cb1 = fig.colorbar(cf1, ax=ax1, orientation='horizontal')

ax1.add_feature(cfeature.COASTLINE.with_scale('50m'))
ax1.add_feature(cfeature.BORDERS)
ax1.add_feature(cfeature.STATES)
ax2.add_feature(cfeature.COASTLINE.with_scale('50m'))
ax2.add_feature(cfeature.BORDERS)
ax2.add_feature(cfeature.STATES)
ax3.add_feature(cfeature.COASTLINE.with_scale('50m'))
ax3.add_feature(cfeature.BORDERS)
ax3.add_feature(cfeature.STATES)
ax4.add_feature(cfeature.COASTLINE.with_scale('50m'))
ax4.add_feature(cfeature.BORDERS)
ax4 .add_feature(cfeature.STATES)

plt.savefig('q5_four_panel.png')