### TESTING CODE ###

# Code for working with the schedules to try to add them to a plot. 

# Import Modules
import pandas as pd
import geopandas as gpd
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
import plotly.express as px # Interactive plot maker thingy
import warnings

main_path = '/home/epalmisa/met330/final_project'
#date = '06/16/2026' # Test date
date = input('Please input date (MM/DD/YYYY): ')
if date == 'test':
    date = '06/16/2026'
    user_date = date[6:10]+date[0:2]+date[3:5]
temp = date
if date[-2:] != '26':
    print('This script currently only supports dates in the 2026 season.')
    exit()
if len(date) != 10:
    print('Please input date in viable format. ')
    exit()
if date[0] == '0':
    user_date = date[6:10]+date[0:2]+date[3:5]
    date = date[1:]
else:
    user_date = date[6:10]+date[0:2]+date[3:5]

date2 = temp[0:6]+temp[8:10]

# ['Game Date', 'Day of Week', 'Local Time', 'Time - ET', 'Game', 'Away Team', 'Home Team', 'Location']
df = pd.read_csv(main_path+'/schedules/2026/Full_MLB.csv')
stadium_df = pd.read_csv(main_path+'/stadium_data/2026_Stadium_Data.csv')

home_teams = []
data_home_teams = []
away_teams = []
data_away_teams = []
lon_list = []
lat_list = []

for i, row in df.iterrows():
    if df['DATE'][i] == date:
        if '-' in row['HOME TEAM']: # Diamondbacks are only team with a hyphen
            home_team = 'Diamondbacks'
            dht = home_team
        elif ' ' in row['HOME TEAM']:
            home_team = row['HOME TEAM']
            dht = row['HOME TEAM'].replace(' ','')
        else:
            home_team = row['HOME TEAM']
            dht = home_team
        home_teams.append(home_team)
        data_home_teams.append(dht)

        if '-' in row['AWAY TEAM']: # Diamondbacks are only team with a hyphen
            away_team = 'Diamondbacks'
            dat = away_team
        elif ' ' in row['AWAY TEAM']:
            away_team = row['AWAY TEAM']
            dat = row['AWAY TEAM'].replace(' ','')
        else:
            away_team = row['AWAY TEAM']
            dat = away_team
        away_teams.append(away_team)
        data_away_teams.append(dat)

start_times = []
matchups = []
venues = []

for i, t in enumerate(data_home_teams):
    if t == 'Astros': # no astros data. stupid astros
        not_astros = away_teams[i]
        dummy_df = pd.read_csv(main_path+f'/schedules/2026/{not_astros}_Full.csv')
        dummy_mask = (dummy_df['START DATE'] == date2)
        start_time = dummy_df[dummy_mask]['START TIME ET'].to_list()
        start_times.append(start_time[0])
        matchup = dummy_df[dummy_mask]['SUBJECT'].to_list()
        matchups.append(matchup[0])
        venue = dummy_df[dummy_mask]['LOCATION'].to_list()
        venues.append(venue[0])
        continue
    dummy_df = pd.read_csv(main_path+f'/schedules/2026/{t}_Full.csv')
    dummy_mask = (dummy_df['START DATE'] == date2)
    start_time = dummy_df[dummy_mask]['START TIME ET'].to_list()
    start_times.append(start_time[0])
    matchup = dummy_df[dummy_mask]['SUBJECT'].to_list()
    matchups.append(matchup[0])
    venue = dummy_df[dummy_mask]['LOCATION'].to_list()
    venues.append(venue[0])

# Print all games on date (mainly for testing of smooth code)
counter = 0
print(f"Games on {date}:")
for i, j in enumerate(data_home_teams):
    print(matchups[i],'/', venues[i],'/', start_times[i])
    counter += 1
if counter == 0:
    print('None')

fig, ax = plt.subplots(constrained_layout=True, subplot_kw={'projection':ccrs.PlateCarree()})

ax.set_extent([-130,-60,22,52],crs=ccrs.PlateCarree())
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.STATES,linewidth=0.5)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.LAKES)

for team in home_teams: # Putting this in here so colors are all the same
    team_mask = (stadium_df['Team']==team)
    lon_list.append((stadium_df[team_mask]['Longitude'].to_list())[0])
    lat_list.append((stadium_df[team_mask]['Latitude'].to_list())[0])
ax.scatter(lon_list,lat_list,zorder=5,color='red',alpha=1,s=10,transform=ccrs.PlateCarree())
fig.suptitle(f'MLB Games on {date}')

plt.savefig('sched_test.png')

###########################################################################

print(start_times)
exit()

for i, j in enumerate(start_times):
    forecast_hour = 0
    if 'AM' in start_times[i]:
        print('AM time')
        exit()
    

# Download Grib2 File and Index
url = f'https://noaa-nam-pds.s3.amazonaws.com/nam.{user_date[0:8]}/nam.t12z.awphys00.tm00.grib2'
index = f'https://noaa-nam-pds.s3.amazonaws.com/nam.{user_date[0:8]}/nam.t12z.awphys00.tm00.grib2.idx'
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
    print('Team error.')
    exit()

# Conditional Statements
if df['Roof'][i] == True:
    #user_cares = input("This team's stadium has a roof. Do you want to factor it in? (y/n): ")
    user_cares = 'y'
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