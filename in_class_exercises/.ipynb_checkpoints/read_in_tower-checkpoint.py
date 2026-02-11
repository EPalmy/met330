# Code for taking in Valpo's tower data

# Import Pandas
import pandas as pd
import numpy as np
#from datetime import datetime, timedelta # for messing around, not for the actual real code

user_date = input('Please input date as YYYYMMDD: ')

url = f'https://bergeron.valpo.edu/mesonet_data/met_tower/{user_date[0:4]}/ValpoMetTower_{user_date}.csv'
df = pd.read_csv(url)
temps = df['Temp (C)'].values+273.15 # very slightly faster, convert to K
pressures = df['Pres (mb)'].values*100.0 # convert to Pa
dates = df['Date (YYYY-MM-DD_HH:MM:SS local)']
df['Density'] = (pressures/(temps*287))
densities = df['Density'].values
print(densities)

ax = df.plot('Date (YYYY-MM-DD_HH:MM:SS local)','Density')
fig = ax.get_figure()
fig.savefig('another_tower_test.png')

#otemps = np.array(df['Temp (C)'])
#print(f'Maximum Temperature was {max(temps)} C, Minimum Temperature was {min(temps)} C')
#print(otemps[:10],temps[:10])