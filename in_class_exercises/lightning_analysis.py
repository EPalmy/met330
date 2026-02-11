# Code for working with lightning data from Canvas

# Import Modules
import numpy as np
import pandas as pd

# Read in Data
df = pd.read_csv('combined_csv_all_flash_20240427.csv')

heights = df['alt'].values
durations = df['duration'].values
amps = np.abs(df['amp'].values)
s_durations = durations/(10**9)
flash_types = df['type'].values

# Statistics, used a helper function because I learned how they work!
def do_stats(input):
    print(f'Min: {np.nanmin(input)}')
    print(f'Max: {np.nanmax(input)}')
    print(f'Mean: {np.nanmean(input)}')
    print(f'Standard Deviation: {np.std(input)}') 

#do_stats(heights)
#do_stats(s_durations)
#do_stats(amps)

# Locate Type 40 Flashes, throw out
wmask = (flash_types == 40.0)
#print(np.sum(wmask))

# Remove the bad flashes from the data
heights = heights[~wmask]
durations = durations[~wmask]
amps = amps[~wmask]
s_durations = s_durations[~wmask]
flash_types = flash_types[~wmask]

ic_mask = flash_types == 1.0
#ncgs = (flash_types==0) & (amps<0)
print((flash_types[ic_mask]).size)
print((flash_types[~ic_mask]).size)
#print(ncgs.size)