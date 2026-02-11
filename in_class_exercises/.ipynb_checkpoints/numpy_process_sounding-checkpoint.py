# This code is for working through sounding data in "sample_sounding.csv"

# Import
import numpy as np

### Game Plan!
# Open File
fn = open('sample_sounding.csv', 'r')
# Lists to hold the data
levels = []
heights = []
temps = []
dews = []
directions = []
speeds = []
# Loop over the file
for i, line in enumerate(fn):
    if (i < 6) or ('%' in line) or ('-999' in line): # Skip the header, the ending line, and bad data
        continue
    # Split the line into data columns and store it
    # Data is LEVEL, HGHT, TEMP, DWPT, WDIR, WSPD
    sl = line.split(',')
    levels.append(float(sl[0]))
    heights.append(float(sl[1]))
    temps.append(float(sl[2]))
    dews.append(float(sl[3]))
    directions.append(float(sl[4]))
    speeds.append(float(sl[5]))
fn.close()

np_levels = np.array(levels)
np_heights = np.array(heights)
np_temps = np.array(temps) # in C
np_dews = np.array(dews)
np_directions = np.array(directions)
np_speeds = np.array(speeds)

np_temps = np_temps+273.15
np_heights = np_heights/1000
print(np_temps[0:10],np_heights[0:10])

# Do something to find the inversion
start_t = temps[0]
for j in range(1, len(temps)):
    if (temps[j] > temps[j-1]):
        break

# Write out the data we find into a text file
fn = open('sounding_stats.txt','w')
fn.write(f'The inversion pressure is {levels[j]}.\n')
fn.write(f'The inversion height is {heights[j]} meters.\n')
fn.write(f'The inversion temperature is {temps[j]} Celsius.\n')
fn.write(f'The inversion dew point is {dews[j]}.')
fn.close()