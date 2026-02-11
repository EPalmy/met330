# For Making a Skew-T Diagram

# Import Modules
import pandas as pd
import metpy.calc as mpcalc
from metpy.plots import Hodograph, SkewT
from metpy.units import units
import matplotlib.pyplot as plt

url = f'https://bergeron.valpo.edu/soundings/launches/20250618_01/20250618_01_SHARPPY.csv'

sonde = pd.read_csv(url, header=4, names=['p','z','t','td','wdir','wspd'])
sonde = sonde.drop(sonde.index[-1]) # Drops the last row
sonde = sonde.astype(float)

pres = units.hectopascal*sonde['p'].values
temp = units.celsius*sonde['t'].values
dewpoint = units.celsius*sonde['td'].values
wspd = (units.meter/units.second)*sonde['wspd'].values
wdir = units.degrees*sonde['wdir'].values

fig = plt.figure(figsize=(9,9))
skewt = SkewT(fig)

skewt.plot(pres, temp, color='firebrick')
skewt.plot(pres, dewpoint, color='forestgreen')

plt.savefig('./skew_test.png')
plt.close()