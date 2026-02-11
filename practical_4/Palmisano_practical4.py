# Import Modules

import urllib.request as ureq
import pygrib
import matplotlib.pyplot as plt
import rasterio as rio
import numpy as np
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import numpy as np

date = '2025102018'

#band = input('Input Satellite Band: ')
#user_cmap = input('Input Color Map: ')
rfile = f'./data/LC08_L1TP_034027_20251020_20251020_02_RT_B4.TIF'
gfile = f'./data/LC08_L1TP_034027_20251020_20251020_02_RT_B3.TIF'
bfile = f'./data/LC08_L1TP_034027_20251020_20251020_02_RT_B2.TIF'

data_proj = ccrs.PlateCarree()
map_proj = ccrs.UTM(13)

# Read in files
red_src = rio.open(rfile)
red = red_src.read(1)
blue_src = rio.open(bfile)
blue = blue_src.read(1)
green_src = rio.open(gfile)
green = green_src.read(1)

# Compute coords
height = red.shape[0]
width = red.shape[1]
cols, rows = np.meshgrid(np.arange(width),np.arange(height)) 

x,y = rio.transform.xy(red_src.transform, rows, cols)

# Reshape x y to 2d
x = x.reshape(cols.shape)
y = y.reshape(rows.shape)

# Stack the arrays
rgb = np.stack([red,green,blue],axis=-1)
rgb[rgb<0] = 0

# Scale Data
gamma = 0.35 # no right value, just for what halps you see stuff
rgb = (rgb*0.0000275-0.2)

rgb = np.clip(rgb,0,1) # Force data to be between 0 and 1

# Get Grib Data
url = f'https://noaa-nam-pds.s3.amazonaws.com/nam.{date[0:8]}/nam.t{date[8:10]}z.awphys00.tm00.grib2'
index = f'https://noaa-nam-pds.s3.amazonaws.com/nam.{date[0:8]}/nam.t{date[8:10]}z.awphys00.tm00.grib2.idx'
grb = ureq.urlretrieve(url, f'nam_{date[0:8]}.grib2')
index = ureq.urlretrieve(index, f'nam_{date[0:8]}.grib2.idx')
grbs = pygrib.open(f'nam_{date[0:8]}.grib2')

ugrb = grbs.select(name='10 metre U wind component')[0]
vgrb = grbs.select(name='10 metre V wind component')[0]

uwind = ugrb.values
uwind = uwind*1.94
vwind = vgrb.values
vwind = vwind*1.94
lats, lons = ugrb.latlons()

# Plotting
fig, ax = plt.subplots(constrained_layout=True,dpi=300,subplot_kw={'projection':map_proj})

ax.add_feature(cfeature.COASTLINE.with_scale('50m'),edgecolor='red')
ax.add_feature(cfeature.BORDERS,edgecolor='red')
ax.add_feature(cfeature.STATES,edgecolor='red')

bounds = (float(np.nanmin(x)),float(np.nanmax(x)),float(np.nanmin(y)),float(np.nanmax(y)))
print(bounds)
ax.set_extent(bounds,crs=map_proj)

ax.imshow(rgb**gamma,extent=bounds,transform=map_proj)
ax.axis('off')

ax.barbs(lons[::5,::5],lats[::5,::5],uwind[::5,::5],vwind[::5,::5],color='orange',transform=data_proj)
#ax.scatter(-111.888,40.761,c='red',transform=ccrs.PlateCarree()) # Can change for Teddy Park
ax.text(-103.4627,46.9509,'Teddy Roosevelt National Park',color='green',transform=data_proj)
ax.scatter(-103.4627,46.9509,color='green',transform=data_proj)
plt.savefig(f'mapmapmap.png')