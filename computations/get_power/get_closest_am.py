#%%
from bisect import bisect

#%%
# get ocvoltage from irradiation
def get_am(data, station_ids, am, am_names, months, i, j, air_masses):
    index1 = []
    for p in range(0, len(data[station_ids[i]]['month'][months[j]]['air_mass'])):
        ind1 = bisect(air_masses, data[station_ids[i]]['month'][months[j]]['air_mass'][p])
        
        if ind1 == 0:
            index1.append(ind1)
        
        elif ind1 == len(am_names):
            index1.append(ind1-1)
        
        elif abs(air_masses[ind1] - data[station_ids[i]]['month'][months[j]]['air_mass'][p]) \
            < abs(air_masses[ind1-1] - data[station_ids[i]]['month'][months[j]]['air_mass'][p])\
            and ind1 >= 1:
            index1.append(ind1)
        
        else:
            index1.append(ind1-1)
            
    data[station_ids[i]]['month'][months[j]]['ind_am_names'] = index1
        
    return data