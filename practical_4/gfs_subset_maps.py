import pygrib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

data_proj = map_proj = ccrs.PlateCarree()

grbs = pygrib.open('./data/nam.t00z.awphys00.tm00.grib2')
ugrb = grbs.select(name='10 metre U wind component')[0]
vgrb = grbs.select(name='10 metre V wind component')[0]
#temps = grbs.select(name='Temperature')# adding [0] after to index

grb = ugrb
data, lats, lons = grb.data(lat1=-40,lat2=40,lon1=-25,lon2=55)
time = grb.validDate
#print(data.shape,lats.shape,lons.shape)
#print(time)

fig, ax = plt.subplots(subplot_kw={'projection':map_proj})

ax.set_extent([-25,55,-40,40])

mesh = ax.pcolormesh(lons, lats, data,cmap='terrain')
cb = fig.colorbar(mesh, ax=ax, orientation='vertical')
cb.set_label(f'{grb.name} ({grb.units})', fontsize=14)

ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
ax.add_feature(cfeature.BORDERS)

plt.savefig(f'gfs_{grb.name.replace(' ','')}.png')
plt.close()