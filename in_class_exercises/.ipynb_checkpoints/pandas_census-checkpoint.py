# Pandas exercise with census data

# Import Modules
import pandas as pd

census = pd.read_csv('historical_state_population_by_year.csv', names = ['State','Year','Population'])
#print(census)
good_state = 'IL'
state = census.loc[census['State']==good_state]
ax = state.plot('Year','Population')
fig = ax.get_figure()
#ax.title = f'{good_state} Population Over Time'
fig.savefig('state_test.png')
data_2024 = census.loc[census['Year']==2024]
many_people_2024 = data_2024.loc[data_2024['Population']>(10000000)]
for s in many_people_2024['State'].values:
    print(s)
