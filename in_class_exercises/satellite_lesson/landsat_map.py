# Import Modules

import matplotlib.pyplot as plt
import rasterio as rio
import numpy as np
import cartopy.feature as cfeature
import cartopy.crs as ccrs

#band = input('Input Satellite Band: ')
#user_cmap = input('Input Color Map: ')
rfile = f'salt_lake_city/LC09_L2SP_038032_20251008_20251010_02_T1_SR_B4.TIF'
gfile = f'salt_lake_city/LC09_L2SP_038032_20251008_20251010_02_T1_SR_B3.TIF'
bfile = f'salt_lake_city/LC09_L2SP_038032_20251008_20251010_02_T1_SR_B2.TIF'

data_proj = map_proj = ccrs.UTM(12)

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

#print('Image map projection', red_src.crs) # This is the transform of the data
#print('File data type,', red_src.dtypes) # Data type in the file (uint8, int16 are the most common)
#print('Number of bands', red_src.count) # How many bands are in the file

fig, ax = plt.subplots(constrained_layout=True,dpi=300,subplot_kw={'projection':map_proj})
bounds = (x.min(),x.max(),y.min(),y.max())
ax.imshow(rgb**gamma,cmap='Greys_r',extent=bounds,transform=data_proj)
ax.axis('off')
ax.scatter(-111.888,40.761,c='red',transform=ccrs.PlateCarree())
plt.savefig(f'mapmapmap.png')