# Import Modules

import matplotlib.pyplot as plt
import rasterio as rio

band = input('Input Satellite Band: ')
user_cmap = input('Input Color Map: ')
rfile = f'salt_lake_city/LC09_L2SP_038032_20251008_20251010_02_T1_SR_B{band}.TIF'
src = rio.open(rfile)
red = src.read(1)
print(rgb)
red[red<0] = 0

# Scale Data
gamma = 0.35 # no right value, just for what halps you see stuff
red = (red*0.0000275-0.2)

#print('Image map projection', red_src.crs) # This is the transform of the data
#print('File data type,', red_src.dtypes) # Data type in the file (uint8, int16 are the most common)
#print('Number of bands', red_src.count) # How many bands are in the file

fig, ax = plt.subplots(constrained_layout=True)
ax.imshow(red**gamma, cmap=user_cmap)
ax.axis('off')
plt.savefig(f'band{band}.png')