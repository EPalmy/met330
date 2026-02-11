# Code for reading in data from WRF Output

# Import Modules
import netCDF4 as nc
import matplotlib.pyplot as plt

# Read in Data
main_file = 'wrfout_d02_2024-04-27_18-30-00'
fn = nc.Dataset(main_file,'r')
# These are read in as numpy arrays
pres = fn.variables['PB'][:]/100.0 # Units hPa
uwind = fn.variables['U'][:] # Units m/s
fn.close()

# Some Notes
# Colon makes sure that you get the data, not just the descriptions
# pres.shape = (1,44,250,300) --> (Time,z,y,x)
# pres[0,:,0,0].shape = (44,)

# Plotting
fig, ax = plt.subplots(constrained_layout=True)
ax.plot(uwind[0, :, 0,0],pres[0, :, 0,0]) # Slice the 4D arrays into 2D arrays
ax.set_ylim(1000,100) # Sets Y-limits, but also flips the data correctly
ax.set_xlabel('U Wind (m/s)')
ax.set_ylabel('Pressure (Pa)')
plt.savefig('nc_plot_1D.png')
plt.close()