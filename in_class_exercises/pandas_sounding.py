# Pandas Python In-Class Exercise

# Import Modules
import pandas as pd

# Load the sounding
df = pd.read_csv('sample_sounding.csv',header=5,names=['P','Z','T','Td','WDIR','WSPD'])
#df.drop(df.loc[df['Z']==-999].index, inplace=True)
df.loc[df['Z']==-999] = float('nan')
#print(df)
warm_temps = df.loc[df['T']>0]
ax = df.plot('T','Z')
#ax = warm_temps.plot('T','Z')
fig = ax.get_figure()
fig.savefig('temp.png')
#print(df.columns)
