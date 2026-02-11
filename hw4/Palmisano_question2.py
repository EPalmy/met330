# Ethan Palmisano
# MET-330
# Dr. Christopher Phillips
# 17 November 2025
# I have neither given or receieved nor have I tolerated others' use of unauthorized aid.

# Instructions: Using the provided scm_output.nc file, create a 2 panel plot with time on the x axis
# and height on the y axis for the U and V wind variables.
# You can check the header of a netCDF file by using ncdump -h file_name > header on the
# command line. Then opening the new "header" file.

# Import Modules
import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np

path_line = '/storage/cphill19/met330_data/hw4/scm_output.nc'

data = nc.Dataset(path_line,'r')

time = data.variables['Time'][::] # units seconds
height = data.variables['Height'][::] # units m
uwind = data.variables['U'][::] # units m/s
vwind = data.variables['V'][::] # units m/s

print(time.shape,height.shape,uwind.shape,vwind.shape)

fig, (ax1, ax2) = plt.subplots(constrained_layout=True,ncols=2)

# Transpose the data in the contours to make sure the arrays are in the right order
cf1 = ax1.contourf(time,height,uwind.transpose(),cmap='coolwarm')
cf2 = ax2.contourf(time,height,vwind.transpose(),cmap='coolwarm')

cb1 = fig.colorbar(cf1, ax=ax1, orientation='horizontal')
cb2 = fig.colorbar(cf2, ax=ax2, orientation='horizontal')

plt.savefig('test2.png')