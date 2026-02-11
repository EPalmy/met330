# Ethan Palmisano
# MET-330
# Dr. Christopher Phillips
# 3 October 2025
# I have neither given or receieved nor have I tolerated others' use of unauthorized aid.
#
# Instructions: Using the provided ozone data file, read the data in line by line, replacing any bad data with NaNs. Then compute the max, min, and mean ozone concentration for the day.

# Read in file
df = open('./Met330_Ozone_July7th_2025.csv','r')
ozones = []
g_ozones = [] # Separate list with good ozones so nans don't ruin my day
for i, line in enumerate(df):
    if i <= 1:
        continue
    dummy = line.split(',')
    if float(dummy[1]) < 0:
        ozones.append(float('nan')) # replace with nans if needed in future
    else:
        g_ozones.append(dummy[1])
        ozones.append(dummy[1])

# Calculate Min/Max/Mean
ototal = 0
for o in g_ozones:
    ototal+=float(o)
print(f'Minimum Ozone: {min(g_ozones)}')
print(f'Maximum Ozone: {max(g_ozones)}')
print(f'Mean Ozone: {ototal/len(g_ozones)}')