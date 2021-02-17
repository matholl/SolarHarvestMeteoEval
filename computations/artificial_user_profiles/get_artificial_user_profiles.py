#%% Import libraries
import csv
from datetime import datetime
import numpy as np

#%%
def get_artificial_user_profiles(path_artificial_user_profiles):

    filename = 'ArtificialUserProfiles'
    path = path_artificial_user_profiles + filename + '.csv'
    f = open(path)
    reader = csv.reader(f, delimiter = ',')
    user = list(reader)

    user_name = [user[p][0] for p in range(1, len(user))]
    user_description = [user[p][1] for p in range(1, len(user))]
    user_times = [user[p][2:] for p in range(1, len(user))]
    user_times = [list(filter(None, user_times[p])) for p in range(0, len(user_times))]

    for i in range(0, len(user_times)):
        for j in range(0, len(user_times[i])):
            user_times[i][j] = datetime.strptime(user_times[i][j], '%H:%M').time()
    return user_name, user_description, user_times

#%%
def get_indices_of_user_outside_times(i, j, data, station_ids, months, user_times, user_name):
    # definitions
    outside_time_indices = []
    weekdays = [0,1,2,3,4]
    saturday = [5]
    sunday = [6]

    # detecting indices
    for m in range(0, len(user_times)):

        ### FIND DAILY INDICES INDEPENDENT OF DAY IN THE WEEK ###
        # find all out- and in-going indices for the users
        indices_collector_out = []
        indices_collector_in = []

        for n in range(0, len(user_times[m]), 2):
            # find all indices of the going-outside-times within the current month
            indices_collector_out.extend([i for i, x in enumerate([data[station_ids[i]]['month'][months[j]]['local_time'][p].time() \
            for p in range(0, len(data[station_ids[i]]['month'][months[j]]['local_time']))]) if x == user_times[m][n]])
            # find all indices of the going-inside-times within the current month
            indices_collector_in.extend([i for i, x in enumerate([data[station_ids[i]]['month'][months[j]]['local_time'][p].time() \
            for p in range(0, len(data[station_ids[i]]['month'][months[j]]['local_time']))]) if x == user_times[m][n+1]])


        ### REMOVING ALL WRONG INDICES (DEPENDING ON THE WEEKDAY) ###
        # removing detected indices_collector_out on wrong days
        del_indices_collector_out = []
        for n in range(0, len(indices_collector_out)):
            # weekdaycheck
            if m in weekdays and data[station_ids[i]]['month'][months[j]]['local_time'][indices_collector_out[n]].weekday() not in weekdays:
                del_indices_collector_out.append(n)

            # weekendcheck active day
            elif (m == 5) and data[station_ids[i]]['month'][months[j]]['local_time'][indices_collector_out[n]].weekday() not in [5,6]:
                del_indices_collector_out.append(n)

            # weekendcheck lazy day
            elif (m == 6) and data[station_ids[i]]['month'][months[j]]['local_time'][indices_collector_out[n]].weekday() not in [5,6]:
                del_indices_collector_out.append(n)

        # delete indices_collector_out on wrong days
        for index in sorted(del_indices_collector_out, reverse=True):
            del indices_collector_out[index]

        # removing detected indices_collector_in on wrong days
        del_indices_collector_in = []
        for n in range(0, len(indices_collector_in)):
            # weekdaycheck
            if m in weekdays and data[station_ids[i]]['month'][months[j]]['local_time'][indices_collector_in[n]].weekday() not in weekdays:
                del_indices_collector_in.append(n)

            # weekendcheck active day
            elif (m == 5) and data[station_ids[i]]['month'][months[j]]['local_time'][indices_collector_in[n]].weekday() not in [5,6]:
                del_indices_collector_in.append(n)

            # weekendcheck lazy day
            elif (m == 6) and data[station_ids[i]]['month'][months[j]]['local_time'][indices_collector_in[n]].weekday() not in [5,6]:
                del_indices_collector_in.append(n)

        # delete indices_collector_in on wrong days
        for index in sorted(del_indices_collector_in, reverse=True):
            del indices_collector_in[index]

        # sort collectors
        indices_collector_in.sort()
        indices_collector_out.sort()

        # checking edges
        if indices_collector_out[0] > indices_collector_in[0]:
            del indices_collector_in[0]
#            print('Deleting first index of indices_collector_in for m = %d, i = %d and j = %d' % (m, i, j))
        if indices_collector_out[-1] > indices_collector_in[-1]:
            del indices_collector_out[-1]
#            print('Deleting last index of indices_collector_out for m = %d, i = %d and j = %d' % (m, i, j))

        # checking core
        q = 0
        long_user_times = user_times[m] * min([len(indices_collector_out), len(indices_collector_in)])
        index_user_times = long_user_times.index(data[station_ids[i]]['month'][months[j]]['local_time'][indices_collector_out[0]].time())
        while q < min([len(indices_collector_out), len(indices_collector_in)]):
            if data[station_ids[i]]['month'][months[j]]['local_time'][indices_collector_out[q]].time() == long_user_times[index_user_times] \
            and data[station_ids[i]]['month'][months[j]]['local_time'][indices_collector_in[q]].time() == long_user_times[index_user_times+1]:
                q += 1
                index_user_times += 2

            elif data[station_ids[i]]['month'][months[j]]['local_time'][indices_collector_out[q]].time() == long_user_times[index_user_times+2] \
            and data[station_ids[i]]['month'][months[j]]['local_time'][indices_collector_in[q]].time() == long_user_times[index_user_times+1+2]:
                print('Warning: skipped 1 outside time slots for station %s, month %s and user %d at q %d' % (data[station_ids[i]]['station_name'], months[j], m, q))
                q += 1
                index_user_times += 2+1*2

            elif data[station_ids[i]]['month'][months[j]]['local_time'][indices_collector_out[q]].time() == long_user_times[index_user_times+2*2] \
            and data[station_ids[i]]['month'][months[j]]['local_time'][indices_collector_in[q]].time() == long_user_times[index_user_times+1+2*2]:
                print('Warning: skipped 2 outside time slots for station %s, month %s and user %d at q %d' % (data[station_ids[i]]['station_name'], months[j], m, q))
                q += 1
                index_user_times += 2+2*2

            elif data[station_ids[i]]['month'][months[j]]['local_time'][indices_collector_out[q]].time() == long_user_times[index_user_times+2*3] \
            and data[station_ids[i]]['month'][months[j]]['local_time'][indices_collector_in[q]].time() == long_user_times[index_user_times+1+2*3]:
                print('Warning: skipped 3 outside time slots for station %s, month %s and user %d at q %d' % (data[station_ids[i]]['station_name'], months[j], m, q))
                q += 1
                index_user_times += 2+3*2

            elif data[station_ids[i]]['month'][months[j]]['local_time'][indices_collector_out[q]].time() == long_user_times[index_user_times+2*4] \
            and data[station_ids[i]]['month'][months[j]]['local_time'][indices_collector_in[q]].time() == long_user_times[index_user_times+1+2*4]:
                print('Warning: skipped 4 outside time slots for station %s, month %s and user %d at q %d' % (data[station_ids[i]]['station_name'], months[j], m, q))
                q += 1
                index_user_times += 2+4*2

            else:
                if data[station_ids[i]]['month'][months[j]]['local_time'][indices_collector_out[q]].time() != long_user_times[index_user_times] \
                and data[station_ids[i]]['month'][months[j]]['local_time'][indices_collector_out[q]].time() == long_user_times[index_user_times+2]\
                and data[station_ids[i]]['month'][months[j]]['local_time'][indices_collector_in[q]].time() == long_user_times[index_user_times+1]:
                    print('deleting indices_collector_in of user %d with q = %d' % (m,q))
                    del indices_collector_in[q]
                    q = 0
                    index_user_times = long_user_times.index(data[station_ids[i]]['month'][months[j]]['local_time'][indices_collector_out[0]].time())
                elif data[station_ids[i]]['month'][months[j]]['local_time'][indices_collector_in[q]].time() != long_user_times[index_user_times+1] \
                and data[station_ids[i]]['month'][months[j]]['local_time'][indices_collector_in[q]].time() == long_user_times[index_user_times+3]\
                and data[station_ids[i]]['month'][months[j]]['local_time'][indices_collector_out[q]].time() == long_user_times[index_user_times]:
                    print('deleting indices_collector_out of user %d with q = %d' % (m,q))
                    del indices_collector_out[q]
                    q = 0
                    index_user_times = long_user_times.index(data[station_ids[i]]['month'][months[j]]['local_time'][indices_collector_out[0]].time())
                else:
                    print('Warning! Check lines 100 - 130 in get_artificial_user_profiles.py \n' + \
                          'station %s month %s and user m = %d at q = %d!' % (data[station_ids[i]]['station_name'], months[j], m, q))
                    break


        indices_collector = indices_collector_in + indices_collector_out
        outside_time_indices.append(indices_collector)

    for m in range(0, len(outside_time_indices)):
        outside_time_indices[m].sort()

    # final check
    detected_outside_times = []
    number_detected_outside_times = []
    for m in range(0, len(outside_time_indices)):
        detected_outside_times.append(list(set([data[station_ids[i]]['month'][months[j]]['local_time'][outside_time_indices[m][p]].time() \
                                       for p in range(0, len(outside_time_indices[m]))])))
        number_detected_outside_times.append([[data[station_ids[i]]['month'][months[j]]['local_time'][outside_time_indices[m][p]].time() \
                                       for p in range(0, len(outside_time_indices[m]))].count(detected_outside_times[m][q]) \
                                        for q in range(0, len(detected_outside_times[m]))])

    # error messages
    for m in range(0, len(outside_time_indices)):
        # check if there are only pairs
        if len(outside_time_indices[m]) % 2 != 0:
            print('Warning! Uneven number of outside_time_indices for user with index m = %d (%s)' % (m, user_name[m]))

        # check whether local time length equals date_time lengths
        if len(data[station_ids[i]]['month'][months[j]]['local_time']) != len(data[station_ids[i]]['month'][months[j]]['date_time']):
            print('Local time list does not have the equal lengths as the date_time list')

        # check if last index is within the length of the current month's data
        if outside_time_indices[m][-1] > (len(data[station_ids[i]]['month'][months[j]]['local_time'])-1):
            print('outside_time_index[%d][-1] exceeds the dimensions of data[station_ids[%d]][\'month\'][months[%d]][\'local_time\']' % (m, i, j))

    return outside_time_indices

#%%
def get_outside_time_data(data, i , j, station_ids, months, outside_time_indices):
    global_radiation = []
    direct_radiation = []
    diffuse_radiation = []
    local_times = []
    for m in range(0, len(outside_time_indices)):
        global_collector = []
        direct_collector = []
        diffuse_collector = []
        local_times_collector = []
        for n in range(0, len(outside_time_indices[m]), 2):
                global_collector.append(data[station_ids[i]]['month'][months[j]]['glo'][outside_time_indices[m][n]:outside_time_indices[m][n+1]+1])
                direct_collector.append(data[station_ids[i]]['month'][months[j]]['dir'][outside_time_indices[m][n]:outside_time_indices[m][n+1]+1])
                diffuse_collector.append(data[station_ids[i]]['month'][months[j]]['dif'][outside_time_indices[m][n]:outside_time_indices[m][n+1]+1])
                local_times_collector.append([data[station_ids[i]]['month'][months[j]]['local_time'][outside_time_indices[m][n]], \
                                          data[station_ids[i]]['month'][months[j]]['local_time'][outside_time_indices[m][n+1]+1]])
        global_radiation.append(global_collector)
        direct_radiation.append(direct_collector)
        diffuse_radiation.append(diffuse_collector)
        local_times.append(local_times_collector)

    return global_radiation, direct_radiation, diffuse_radiation, local_times

#%%
def fill_outside_time_data(data, i , j, station_ids, months):
    data[station_ids[i]]['month'][months[j]]['outside_time_glo_filled'] = []
    for m in range(0, len(data[station_ids[i]]['month'][months[j]]['outside_time_indices'])):
        data[station_ids[i]]['month'][months[j]]['outside_time_glo_filled'].append(np.zeros(len(data[station_ids[i]]['month'][months[j]]['glo'])))
    for m in range(0, len(data[station_ids[i]]['month'][months[j]]['outside_time_indices'])):
        for n in range(0, len(data[station_ids[i]]['month'][months[j]]['outside_time_indices'][m]), 2):
            for q in range(data[station_ids[i]]['month'][months[j]]['outside_time_indices'][m][n], \
                           data[station_ids[i]]['month'][months[j]]['outside_time_indices'][m][n+1]+1):

                data[station_ids[i]]['month'][months[j]]['outside_time_glo_filled'][m][q] = data[station_ids[i]]['month'][months[j]]['glo'][q]

    return data

#%%
def get_monthly_mean_power_estimate(data, i , j, station_ids, months, cell_area_m2):
    data[station_ids[i]]['month'][months[j]]['mean_power_estimate'] = []
    for m in range(0, len(data[station_ids[i]]['month'][months[j]]['outside_time_glo_filled'])):
        data[station_ids[i]]['month'][months[j]]['mean_power_estimate'].append(\
            np.nanmean(data[station_ids[i]]['month'][months[j]]['outside_time_glo_filled'][m])*.2*.2*cell_area_m2)

    return data

#%%
def main(data, station_ids, months, cell_area_m2):
    user_name, user_description, user_times = get_artificial_user_profiles()

    for i in range(0, len(station_ids)):
        months = list(data[station_ids[i]]['month'].keys())
        for j in range(0, len(months)):
            data[station_ids[i]]['month'][months[j]]['outside_time_indices'] = \
                get_indices_of_user_outside_times(i, j, data, station_ids, months, user_times)
            data[station_ids[i]]['month'][months[j]]['outside_time_glo'], \
            data[station_ids[i]]['month'][months[j]]['outside_time_dir'], \
            data[station_ids[i]]['month'][months[j]]['outside_time_dif'], \
            data[station_ids[i]]['month'][months[j]]['outside_time_local_times']= \
                get_outside_time_data(data, i , j, station_ids, months, data[station_ids[i]]['month'][months[j]]['outside_time_indices'])
            data = fill_outside_time_data(data, i , j, station_ids, months)
            data = get_monthly_mean_power_estimate(data, i , j, station_ids, months, cell_area_m2)


    return user_name, user_description, user_times, data

#%%
if __name__ == "__main__":
    user_name, user_description, user_times, data = main(data, station_ids, months, cell_area_m2)
