# Import Modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('rebinned_csv_all_flash_20240427.csv')
height = df['Mean Height (m)'].values
duration = df['Mean Duration (ns)'].values
mean_pos = df['Mean Positive Current (A)']
mean_neg = df['Mean Negative Current (A)']
time = df['Hour'].values+df['Minute'].values/60.0+df['Second'].values/3600.0 # convert all timestamps to hours
'''
fig, ax = plt.subplots()
ax.plot(time, height, color='black')
ax.scatter(time,height,color='firebrick')
ax.set_xlabel('Hour (local)',fontsize=14,fontweight='bold')
ax.set_ylabel('Height (m)',fontsize=14,fontweight='roman')
ax.set_title('Lightning Height',fontsize=18)
ax.set_ylim(0,12000)
ax.grid()
plt.savefig('go_cubs.png')

fig, (ax1,ax2) = plt.subplots(nrows=2,constrained_layout=True)
ax1.plot(time,height,color='black')
ax1.set_ylabel('Altitude (m)')
ax2.plot(time,duration,color='firebrick')
ax2.set_ylabel('Duration (ns)')
ax2.set_xlabel('Hour')
ax1.set_ylim(0,12000)
ax2.set_ylim(0,8*(10**8))
ax1.grid()
ax2.grid()
fig.suptitle('Lightning Height and Duration') # Super title!
# ax.text() for specifically moving where you want your titles
plt.savefig('go_cubs_go.png')


fig, (ax1,ax2) = plt.subplots(ncols=2,constrained_layout=True) # Always: x data, then y data
ax1.scatter(duration,mean_pos)
ax2.scatter(duration,mean_neg)
ax1.set_ylabel('Mean Positive Current (A)')
ax2.set_ylabel('Mean Negative Current (A)')
ax1.set_xlabel('Duration (ns)')
ax2.set_xlabel('Duration (ns)')
#fig.suptitle('Duration (ns)',)
ax1.grid()
ax2.grid()

plt.savefig('lets_go_cubs.png')
'''
fig, ax = plt.subplots(constrained_layout=True)
ax.plot(time,mean_pos,color='firebrick')
ax.set_ylabel('Positive Current (A)',color='firebrick')
ax2 = ax.twinx()
ax2.plot(time,mean_neg,color='dodgerblue')
ax2.set_ylabel('Negative Current (A)',color='dodgerblue')
ax.grid()
plt.savefig('cubs_win.png')