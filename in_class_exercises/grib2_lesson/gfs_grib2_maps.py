import pygrib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

data_proj = map_proj = ccrs.PlateCarree()

grbs = pygrib.open('gfs.t00z.sfluxgrbf000.grib2')
grb = grbs.select(name='Surface pressure')[0]
temps = grbs.select(name='Temperature')# adding [0] after to index

data = grb.values
lats, lons = grb.latlons()
time = grb.validDate
#print(data.shape,lats.shape,lons.shape)
#print(time)

fig, ax = plt.subplots(subplot_kw={'projection':map_proj})

ax.set_extent([-25,55,-40,40])

mesh = ax.pcolormesh(lons, lats, data,cmap='terrain')
cb = fig.colorbar(mesh, ax=ax, orientation='vertical')
cb.set_label(f'{grb.name} ({grb.units})', fontsize=14)

ax.add_feature(cfeature.COASTLINE.with_scale('50m'))#, linewidth=0.5)
ax.add_feature(cfeature.BORDERS)#, linewidth=0.5)

plt.savefig(f'gfs_{grb.name.replace(' ','')}.png')
plt.close()