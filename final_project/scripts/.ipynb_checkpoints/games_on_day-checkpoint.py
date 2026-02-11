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
temp = date
if date[-2:] != '26':
    print('This script currently only supports dates in the 2026 season.')
    exit()
if len(date) != 10:
    print('Please input date in viable format. ')
    exit()
if date[0] == '0':
    date = date[1:]

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