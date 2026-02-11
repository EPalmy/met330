# Import Modules

import matplotlib.pyplot as plt
import rasterio as rio
import numpy as np

#band = input('Input Satellite Band: ')
#user_cmap = input('Input Color Map: ')
rfile = f'salt_lake_city/LC09_L2SP_038032_20251008_20251010_02_T1_SR_B4.TIF'
gfile = f'salt_lake_city/LC09_L2SP_038032_20251008_20251010_02_T1_SR_B3.TIF'
bfile = f'salt_lake_city/LC09_L2SP_038032_20251008_20251010_02_T1_SR_B2.TIF'
nirfile = f'salt_lake_city/LC09_L2SP_038032_20251008_20251010_02_T1_SR_B5.TIF'
swfile = f'salt_lake_city/LC09_L2SP_038032_20251008_20251010_02_T1_SR_B6.TIF'

# Read in files
red_src = rio.open(rfile)
red = red_src.read(1)
blue_src = rio.open(bfile)
blue = blue_src.read(1)
green_src = rio.open(gfile)
green = green_src.read(1)
nir_src = rio.open(nirfile)
nir = nir_src.read(1)
sw_src = rio.open(swfile)
sw = sw_src.read(1)

# Stack the arrays
red = (red*0.0000275-0.2)
green = (green*0.0000275-0.2)
blue = (blue*0.0000275-0.2)
nir = (nir*0.0000275-0.2)
sw = (sw*0.0000275-0.2)
rgb = np.stack([red,green,blue],axis=-1)
rgb[rgb<0] = 0

# Scale Data
gamma = 0.35 # no right value, just for what halps you see stuff
#rgb = (rgb*0.0000275-0.2)

# Different Indices Things
ndvi = (nir-red)/(nir+red)
ndwi = (green-nir)/(green+nir)
ndbi = (sw-nir)/(sw+nir)

rgb = np.clip(rgb,0,1) # Force data to be between 0 and 1
ndvi = np.clip(ndvi,0,1)
ndwi = np.clip(ndwi,0,1)
ndbi = np.clip(ndbi,0,1)

#print('Image map projection', red_src.crs) # This is the transform of the data
#print('File data type,', red_src.dtypes) # Data type in the file (uint8, int16 are the most common)
#print('Number of bands', red_src.count) # How many bands are in the file

fig, axes = plt.subplots(nrows=2,ncols=2,dpi=600,constrained_layout=True)

axes[0,0].imshow(rgb**gamma) # **gamma
axes[0,1].imshow(ndvi)
axes[1,0].imshow(ndwi)
axes[1,1].imshow(ndbi)
axes[0,0].set_title('True Color')
axes[0,1].set_title('NDVI')
axes[1,0].set_title('NDWI')
axes[1,1].set_title('NDBI')

plt.savefig('four_panel.png')