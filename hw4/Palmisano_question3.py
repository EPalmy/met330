# Ethan Palmisano
# MET-330
# Dr. Christopher Phillips
# 17 November 2025
# I have neither given or receieved nor have I tolerated others' use of unauthorized aid.

# Instructions: Using the provided GOES-16 file, create a grey scale image of the world. 
# No Cartopy mapping is necessary. CMI is the reflectance variable.

# Import Modules
import matplotlib.pyplot as plt
#import rasterio as rio
import numpy as np
import netCDF4 as nc

phillips_path = '/storage/cphill19/met330_data/hw4/GOES16_C02_202515516.nc'

data = nc.Dataset(phillips_path,'r')

print(data.variables)

cmi = data.variables['CMI'][::10,::10] # sliced so it doesn't take 10 millenia
lats = data.variables['y'][::10]
lons = data.variables['x'][::10]

print(cmi.shape,lats.shape,lons.shape)

fig, ax = plt.subplots(constrained_layout=True)

mesh = ax.pcolormesh(lons,lats,cmi,cmap='Greys_r')

plt.savefig('sattest.png')