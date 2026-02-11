# Code for Practical 5, working with shapefiles of NWS CWAs and Storm Events

# Import Modules
import numpy as np
import shapely
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
import geopandas as gpd

path = '/storage/cphill19/met330_data/practical5/'

sdf = pd.read_csv(path+'StormEvents_details-ftp_v1.0_d2010_c20170726.csv')
cdf = gpd.read_file(path+'w_18mr25.zip')

wx_type = 'Tornado'

map_crs = data_crs = ccrs.PlateCarree()
event_count = []

# Filter out the good data
for wfo in cdf.iterrows():
    wx_mask = sdf['EVENT_TYPE'].values == wx_type
    wfo_mask = sdf['WFO'].values == wfo[1]['WFO']
    matches = wx_mask & wfo_mask
    event_count.append(np.sum(matches))

event_count = np.array(event_count)

# Begin Plot
fig, ax = plt.subplots(constrained_layout=True,subplot_kw={'projection':map_crs})

ax.set_extent([-126,-66,23,48])

# Color Map
cmap = plt.get_cmap('plasma')
colors = cmap(event_count/event_count.max())

mesh = ax.add_geometries(cdf.geometry,data_crs,facecolor=colors,edgecolor='black',cmap=cmap)

cb = fig.colorbar(mesh, ax=ax, cmap=cmap, orientation='horizontal',pad=0.02)
ax.set_title(f'{wx_type}')
cb.set_label('Number of Reports')

# Setting Ticks
ticklabels = np.arange(0, event_count.max(), 20)

cb.set_ticks(ticklabels/event_count.max())
cb.set_ticklabels(ticklabels)

ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)

plt.savefig('test.png')