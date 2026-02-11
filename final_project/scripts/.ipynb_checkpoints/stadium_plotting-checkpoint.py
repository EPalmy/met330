### TESTING CODE ###
# This code is built for making basic plots using the stadium data.

# Import Modules
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import pandas as pd
from PIL import Image
import numpy as np

input_team = input('Input Baseball Team: ')

# Read in Stadium Data
main_path = '/home/epalmisa/met330/final_project'
df = pd.read_csv(main_path+'/stadium_data/2025_Stadium_Data.csv')
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
    
# Read in Stadium PNG - needs to be in for loop
img = np.asarray(Image.open(f'{main_path}/stadium_data/stadium_pngs/{team_str}_Stadium.png'))

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(nrows=3, ncols=3)

ax1 = fig.add_subplot(gs[0:2,1::]) # Stadium Plot
ax1.imshow(img)
ax1.set_xticks([])
ax1.set_yticks([])
ax1.barbs(np.max(img)/2,np.max(img)/2,10*np.sin(df['Angle_C'][i]*(np.pi/180)),-10*np.cos(df['Angle_C'][i]*(np.pi/180))) # currently plotting due north
ax2 = fig.add_subplot(gs[0,0]) # Hitter or Pitcher Final Analysis Spot
ax2.text(0.5,0.5,'Hitter or Pitcher?',horizontalalignment='center',verticalalignment='center_baseline')
ax2.set_xticks([])
ax2.set_yticks([])
ax3 = fig.add_subplot(gs[1,0]) # General Stats
ax3.text(0.5,0.85,'Stadium Stats',horizontalalignment='center',verticalalignment='center_baseline',fontsize=14)
ax3.text(0.5,0.6,f'Altitude: {df['Altitude (ft)'][i]} ft',horizontalalignment='center',verticalalignment='center_baseline')
ax3.text(0.5,0.4,f'Better Field: {bias}',horizontalalignment='center',verticalalignment='center_baseline')
ax3.text(0.5,0.2,f'Roof: {rf}',horizontalalignment='center',verticalalignment='center_baseline')
ax3.set_xticks([])
ax3.set_yticks([])
ax4 = fig.add_subplot(gs[2,:]) # Each Variable Plotted

fig.suptitle(f'{title_str} - {df['Ballpark'][i]}, (DATE)')

plt.savefig('test.png')