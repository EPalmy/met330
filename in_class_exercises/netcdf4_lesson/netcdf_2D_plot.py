# Code for reading in data from WRF Output

# Import Modules
import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Cartopy Definitions
map_proj = ccrs.RotatedPole()
data_proj = ccrs.PlateCarree()
#data_proj = map_proj

# Read in Data
main_file = '/home/epalmisa/met330/wrfout_d01_2024-04-27_18:30:00'
fn = nc.Dataset(main_file,'r')
temp2m = fn.variables['T2'][0,:,:]
pres2m = fn.variables['PSFC'][0,:,:]/100
uwnd = fn.variables['U10'][0,:,:]*1.94
uwnd = uwnd[::30,::30]
vwnd = fn.variables['V10'][0,:,:]*1.94
vwnd = vwnd[::30,::30]

# These are read in as numpy arrays
refl = fn.variables['REFL_10CM'][0,:,:,:]
ltg = fn.variables['LIGHT'][0,:,:]
lats = fn.variables['XLAT'][0,:,:]
lons = fn.variables['XLONG'][0,:,:]
c_refl = np.nanmax(refl,axis=0) # Composite Reflectivity
fn.close()

flash_mask = ltg>0

# Plotting
fig, ax = plt.subplots(constrained_layout=True,subplot_kw={'projection':map_proj})

ax.set_extent([-100, -90, 30, 40],crs=data_proj)

ax.add_feature(cfeature.COASTLINE.with_scale('50m'))#, linewidth=0.5)
ax.add_feature(cfeature.STATES)#, linewidth=0.5)
ax.add_feature(cfeature.BORDERS)#, linewidth=0.5)
ax.add_feature(cfeature.OCEAN)

cf = ax.contourf(lons,lats,temp2m,cmap='plasma',transform=data_proj)
mesh = ax.pcolormesh(lons,lats,temp2m,cmap='turbo',transform=data_proj)
cb = fig.colorbar(mesh,ax=ax,orientation='horizontal')
cb.set_label('Temp (K)')

cont = ax.contour(lons,lats,pres2m, colors='blue')
ax.barbs(lons[::30,::30],lats[::30,::30],uwnd,vwnd,transform=data_proj)
ax.clabel(cont, fontsize=9, fmt='%.0f')
ax.scatter(lons[flash_mask], lats[flash_mask],s=4,marker='x')


plt.savefig('new_nc_plot_2D.png')
plt.close()
