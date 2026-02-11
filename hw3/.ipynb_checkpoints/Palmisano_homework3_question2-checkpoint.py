# Ethan Palmisano
# MET-330
# Dr. Christopher Phillips
# 3 October 2025
# I have neither given or receieved nor have I tolerated others' use of unauthorized aid.

# Instructions: Using Pandas, read in the proper Valpo Met Tower observations and the
# same ozone data. Met tower data can be found at https://bergeron.valpo.edu/current/. Do not
# use any loops. Be sure to handle any missing data, and then:

# Import Modules
import pandas as pd
import numpy as np

# Read Data
url = 'https://bergeron.valpo.edu/mesonet_data/met_tower/2025/ValpoMetTower_20250707.csv'
ozone_data = 'Met330_Ozone_July7th_2025.csv'
tower_ds = pd.read_csv(url) # ['Date (YYYY-MM-DD_HH:MM:SS local)', 'Temp (C)', 'RH (%)', 'Pres (mb)', 'Rain (mm)', 'Wspd (m/s)', 'Wdir (deg)', 'SWdown (W/m2)'] # Using this for reference
ozone_ds = pd.read_csv(ozone_data) # ['Time (local)', 'Ozone (ppm)'] # Using this for reference

ozone_ds.loc[ozone_ds['Ozone (ppm)']==-999] = float('nan') # Replace Bad Data

# Define Needed Data, Calculate Partial Pressure
ozone = ozone_ds['Ozone (ppm)'].values
sw_down = tower_ds['SWdown (W/m2)'].values
pres = tower_ds['Pres (mb)'].values
ppm = ozone_ds['Ozone (ppm)'].values
partial_pressure = ppm*pres*(10**-6)

# Ideal Gas Law: P = roe*R*T
# roe = Pres/(R*T) # R for Ozone is 173.2 J*kg**-1*K**-1

temp_k = tower_ds['Temp (C)']+273.15
density = (partial_pressure*100)/(temp_k*173.2)

# Masks for min/max SW Down
min_mask = tower_ds['SWdown (W/m2)'].values == np.min(tower_ds['SWdown (W/m2)'])
max_mask = tower_ds['SWdown (W/m2)'].values == np.max(tower_ds['SWdown (W/m2)'])

print(f'Ozone at min/max Solar Radiation is {ozone[min_mask][0]}/{ozone[max_mask][0]}.')

ozone_ds['SWdown (W/m2)'] = sw_down # Combine into the same dataframe for the plotting

# Make Pandas Plot
ax = ozone_ds.plot.scatter('Ozone (ppm)','SWdown (W/m2)')
fig = ax.get_figure()
fig.savefig('hw3_ozone_swdown.png')