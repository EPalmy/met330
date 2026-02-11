# Ethan Palmisano
# MET-330
# Dr. Christopher Phillips
# 3 October 2025
# I have neither given or receieved nor have I tolerated others' use of unauthorized aid.
#
# Instructions: Using the provided ozone data file, read the data in line by line, replacing any bad data with NaNs. Then compute the max, min, and mean ozone concentration for the day.

import pandas as pd

# Read in file
df = pd.read_csv('./Met330_Ozone_July7th_2025.csv',header=1,names=['Time','Ozone'])

# Replace Bad Data, Single out good data for calculation
df.loc[df['Ozone']==-999] = float('nan')
g_ozones = df.loc[df['Ozone']>0] # use >0 as ozone cannot be negative

# Calculate Min/Max/Mean
ototal = 0 #
for o in g_ozones['Ozone']:
    ototal+=float(o)
print(f'Minimum Ozone: {min(g_ozones['Ozone'])}')
print(f'Maximum Ozone: {max(g_ozones['Ozone'])}')
print(f'Mean Ozone: {ototal/len(g_ozones['Ozone'])}')