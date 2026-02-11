# Ethan Palmisano
# MET-330
# Dr. Christopher Phillips
# 2 October 2025
# I have neither given or receieved nor have I tolerated others' use of unauthorized aid.

# Instructions: On Document, Practical #2

# Import Modules
# Do Not Import Pandas
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Read in Data
mtdata = open('Merged_ValpoMetTower_20250601-20250601 (1).csv','r')
scdata = open('SaltCreekValpoGageHeight (1).csv','r')

mttime = []
sctime = []
temp = []
relh = []
rain = []
gaugeheight = []

# MT Data: Date (YYYY-MM-DD_HH:MM:SS local),Temp (C),RH (%),Pres (mb),Rain (mm),Wspd (m/s),Wdir (deg),SWdown (W/m2)
for i, line in enumerate(mtdata): 
    if i < 1:
        continue
    sl = line.split(',')
    #mttime.append(str(sl[0]))
    temp.append(float(sl[1]))
    relh.append(float(sl[2]))
    rain.append(float(sl[4]))
    mttime.append(datetime.strptime(sl[0], "%Y-%m-%d_%H:%M:%S"))
for i, line in enumerate(scdata):
    if i < 30:
        continue
    sl = line.split()
    sctime.append(datetime.strptime(sl[2]+sl[3], '%Y-%m-%d%H:%M')-timedelta(hours=1))
    gaugeheight.append(float(line[35:39]))

mttime = np.array(mttime)
sctime = np.array(sctime)
temp = np.array(temp)
relh = np.array(relh)
rain = np.array(rain)
gaugeheight = np.array(gaugeheight)

# Make the masks
crazy_rain = rain > 2 * np.abs(np.std(rain)) + np.mean(rain)
crazy_gauge = gaugeheight > 2 * np.abs(np.std(gaugeheight)) + np.mean(gaugeheight)

# Plotting everything
fig, (ax1, ax2, ax3) = plt.subplots(nrows=3,constrained_layout=True) # Don't like the constrained
ax1.plot(mttime,temp,color='firebrick')
ax1.set_ylabel('Temp (Deg C)',color='firebrick',fontweight='bold')
ax15 = ax1.twinx()
ax15.plot(mttime,relh,color='dodgerblue')
ax15.set_ylabel('RH (%)',color='dodgerblue',fontweight='bold')
ax1.grid()
ax2.plot(mttime,rain,color='black')
ax2.set_ylabel('Rain (mm)',color='black',fontweight='bold')
ax2.grid()
ax2.scatter(mttime[crazy_rain],rain[crazy_rain],color='firebrick')
ax3.plot(sctime,gaugeheight,color='black')
ax3.set_ylabel('Gauge Height (ft)',color='black',fontweight='bold')
ax3.grid()
ax3.scatter(sctime[crazy_gauge],gaugeheight[crazy_gauge],color='firebrick')
ax1.set_xticks([])
ax2.set_xticks([])
xtick_locs = ax3.get_xticks()
xtick_labels = ax3.get_xticklabels()
ax3.set_xticks(xtick_locs)
ax3.set_xticklabels(xtick_labels,rotation=30)
plt.savefig('p2test.png')