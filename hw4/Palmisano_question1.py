# Ethan Palmisano
# MET-330
# Dr. Christopher Phillips
# 17 November 2025
# I have neither given or receieved nor have I tolerated others' use of unauthorized aid.

# Instructions: Using Cartopy, create a map of the globe using the Robinson projection.
# a) Add borders for coastlines and countries.
# b) Color the land and ocean (do not use the stock_img feature).
# c) Add dots and text labels for Paris, New York, Moscow, Tokyo, Sydney, Buenos Aires
# (Argentina), Aruba, and Niamey (Niger). Do not include the locations and names in
# the code. Read them from a text file that you create.

# Import Modules
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import pandas as pd

# Read in City list, set some crs
data = pd.read_csv('/home/epalmisa/met330/hw4/city_list.txt')
data_crs = ccrs.PlateCarree()
map_crs = ccrs.Robinson()

# Actual Plotting
fig, ax = plt.subplots(constrained_layout=True,subplot_kw={'projection':map_crs})
ax.set_extent([-180,180,-90,90],crs=ccrs.PlateCarree()) # setting extent because map wanted to 

#ax.add_feature(cfeature.STATES)
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.COASTLINE)

ax.scatter(data['Lon'],data['Lat'],transform=data_crs,color='red',zorder=5)
for i, city in enumerate(data['City']):
    ax.text(data['Lon'][i],data['Lat'][i],city,color='black',transform=data_crs)

plt.savefig('question1_image.png')