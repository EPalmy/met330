# This code is built for making basic plots using the stadium data.

# Import Modules
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import pandas as pd
from PIL import Image
import numpy as np
import urllib.request as ureq
import pygrib
import scipy
import shapely

# User Inputs
input_team = input('Input Baseball Team: ')
user_date = input('Input Game Day in UTC (YYYYMMDDHH): ')

# For Testing Only
#input_team = 'cubs'
#user_date = '2023040112'

# Download Grib2 File and Index
url = f'https://noaa-nam-pds.s3.amazonaws.com/nam.{user_date[0:8]}/nam.t{user_date[8:10]}z.awphys00.tm00.grib2'
index = f'https://noaa-nam-pds.s3.amazonaws.com/nam.{user_date[0:8]}/nam.t{user_date[8:10]}z.awphys00.tm00.grib2.idx'
grb = ureq.urlretrieve(url, f'dummy_nam.grib2')
index = ureq.urlretrieve(index, f'dummy_nam.grib2.idx')
grbs = pygrib.open(f'dummy_nam.grib2')

sfc_pres = grbs.select(name='Surface pressure')[0].values # units Pa
temp = grbs.select(name='2 metre temperature')[0] # K
dewpoint = grbs.select(name='2 metre dewpoint temperature')[0].values # K
uwind = grbs.select(name='10 metre U wind component')[0].values # m/s
vwind = grbs.select(name='10 metre V wind component')[0].values # m/s

lat, lon = temp.latlons()
time = temp.validDate
temp = temp.values

Cd = 0.3514 # MLB's Average Drag Coefficient for a 2024 Baseball
A = 0.0042 # Front facing part of the baseball for drag equation

# Read in Stadium Data
main_path = '/home/epalmisa/met330/final_project'
df = pd.read_csv(main_path+'/stadium_data/2026_Stadium_Data.csv')
team_found = False
for i, team in enumerate(df['Team']): # gets rid of spaces so PNGs can be read in correctly
    if team.lower() == input_team.lower() or team.lower() == input_team.lower().replace(' ',''):  
        team_str = team
        title_str = team
        if ' ' in team_str:
            team_str = team_str.replace(' ','')
        team_found = True
        break
if team_found == False:
    print('Please input viable team string.')
    exit()

# Conditional Statements
if df['Roof'][i] == True:
    user_cares = input("This team's stadium has a roof. Do you want to factor it in? (y/n): ")
    if user_cares == 'y':
        rf = 'Yes' # rf = Roof Factored
        rtf = True # rtf = Roof T/F
    elif user_cares == 'n':
        rf = 'Yes, Not Factored'
        rtf = False
    else:
        print('Please input a viable string.')
        exit()
else:
    rf = 'No'
    rtf = False

bias = str(df['Better Angle'][i])
if str(df['Better Angle'][i]).lower() == 'nan':
    bias = 'None'

# Find nearest grid point's data using Phillip's Black Magic Voodoo from Stack Overflow
distance = (df['Longitude'][i]-lon)**2+(df['Latitude'][i]-lat)**2
y_ind, x_ind = np.unravel_index(distance.argmin(),distance.shape)

# Calculate Variables, then Calculate Index Value
density = (sfc_pres[y_ind,x_ind])/(287.053*temp[y_ind,x_ind])
stad_u = uwind[y_ind,x_ind] # m/s
stad_v = vwind[y_ind,x_ind] # m/s
wspd = (stad_u**2+stad_v**2)**0.5 # m/s
wspd = wspd*2.23694 # mph
if stad_u > 0:
    wind_angle = 90-np.arctan(stad_v/stad_u)*(180/np.pi)+180 # Degrees
elif stad_u < 0:
    wind_angle = 90-np.arctan(stad_v/stad_u)*(180/np.pi) # Degrees
else:
    if stad_v > 0:
        wind_angle=180
    else:
        wind_angle=0

stad_angle = df['Angle_C'][i] # Degrees 
stad_rel_angle = (stad_angle-wind_angle)*(np.pi/180) # In Radians, used only for the final plot
if bias == 'Right':
    stad_angle = df['Angle_C'][i]+22.5
elif bias == 'Left':
    stad_angle = df['Angle_C'][i]-22.5
if stad_angle < 0:
    stad_angle = stad_angle+360
elif stad_angle >= 360:
    stad_angle = stad_angle-360

rel_angle = (stad_angle-wind_angle)*(np.pi/180) # Radians, 0 means blowing in ideal angle, negative is blowing to the right of ideal angle

# Drag Equation --> 0.5*Cd*A*p*v^2 (Cd and A are not used since they stay constant)
#drag = 0.5*Cd*A*density*(wspd*np.cos(rel_angle))**2 # negative means that the wind is helping the baseballs

# Final Calculation --> Wind is the primary variable taken into account
good_value = (1.25-density)*1.25+np.cos(rel_angle)*(wspd/10) # higher value = better for hitters

if rtf == True:
    good_value = good_value/2

if good_value >= 0.5:
    HorP = "Hitter's Day"
    hcolor = 'red'
elif good_value <= -0.5:
    HorP = "Pitcher's Day"
    hcolor = 'blue'
else:
    HorP = "Fair Game"
    hcolor = 'green'

# Read in Stadium PNG - needs to be in for loop
img = np.asarray(Image.open(f'{main_path}/stadium_data/stadium_pngs/{team_str}_Stadium.png'))

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(nrows=3, ncols=3)

ax1 = fig.add_subplot(gs[0:2,1::]) # Stadium Plot
ax1.imshow(img)
ax1.set_xticks([])
ax1.set_yticks([])
ax1.barbs(np.max(img)/2,np.max(img)/2,-1*wspd*np.sin(stad_rel_angle),wspd*np.cos(stad_rel_angle)) # Plots wind with repsect to the field
ax2 = fig.add_subplot(gs[0,0]) # Hitter or Pitcher Final Analysis Spot
ax2.text(0.5,0.8,'Hitter or Pitcher?',horizontalalignment='center',verticalalignment='center_baseline',fontsize=14)
ax2.text(0.5,0.5,HorP,color=hcolor,horizontalalignment='center',verticalalignment='center_baseline',fontsize=14)
ax2.set_xticks([])
ax2.set_yticks([])
ax3 = fig.add_subplot(gs[1,0]) # Stadium Stats
ax3.text(0.5,0.85,'Stadium Stats',horizontalalignment='center',verticalalignment='center_baseline',fontsize=14)
ax3.text(0.5,0.6,f'Altitude: {df['Altitude (ft)'][i]} ft',horizontalalignment='center',verticalalignment='center_baseline')
ax3.text(0.5,0.4,f'Better Field: {bias}',horizontalalignment='center',verticalalignment='center_baseline')
ax3.text(0.5,0.2,f'Roof: {rf}',horizontalalignment='center',verticalalignment='center_baseline')
ax3.set_xticks([])
ax3.set_yticks([])
ax4 = fig.add_subplot(gs[2,0]) # Index Stats
ax4.text(0.5,0.85,'Index Stats',horizontalalignment='center',verticalalignment='center_baseline',fontsize=14)
ax4.text(0.5,0.6,f'Density: {density:.02f} kg/m³',horizontalalignment='center',verticalalignment='center_baseline')
ax4.text(0.5,0.4,f'Relative Angle: {rel_angle*(180/np.pi):.02f}°',horizontalalignment='center',verticalalignment='center_baseline')
ax4.text(0.5,0.2,f'Wind Speed: {wspd:.02f} mph',horizontalalignment='center',verticalalignment='center_baseline')
ax4.set_xticks([])
ax4.set_yticks([])
ax5 = fig.add_subplot(gs[2,1::]) # Final Index Value
ax5.text(0.5,0.85,'Final Index Value',horizontalalignment='center',verticalalignment='center_baseline',fontsize=14)
ax5.text(0.5,0.5,good_value,color=hcolor,horizontalalignment='center',verticalalignment='center_baseline',fontsize=14)
ax5.set_xticks([])
ax5.set_yticks([])

fig.suptitle(f'{title_str} - {df['Ballpark'][i]}, {user_date[4:6]}-{user_date[6:8]}-{user_date[0:4]} {user_date[8:10]} UTC')

plt.savefig('main_figure.png')