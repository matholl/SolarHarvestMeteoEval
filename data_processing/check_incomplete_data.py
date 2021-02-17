#%%
# Checking for incomplete data and storing the number of missing DPs and the corresponding months
def check_incomplete_data(data, station_ids, months, i, j, minPerMonth):
    #%%
    # glo
    if 'glo' in list(data[station_ids[i]]['month'][months[j]].keys()):
        # SWDR
        if len(data[station_ids[i]]['month'][months[j]]['glo']) + 1*24*60 > minPerMonth[j]:
            data[station_ids[i]]['month'][months[j]]['glo_missing_dp'] = 0
        else:
            if len(data[station_ids[i]]['month'][months[j]]['glo']) < minPerMonth[j]:
                data[station_ids[i]]['month'][months[j]]['glo_missing_dp'] = \
                     minPerMonth[j] - len(data[station_ids[i]]['month'][months[j]]['glo'])
                print('Incomplete global radiation dataset in station %s in month %s!' %(station_ids[i], months[j]))
            else:
                data[station_ids[i]]['month'][months[j]]['glo_missing_dp'] = 0
    else:
        data[station_ids[i]]['month'][months[j]]['glo_missing_dp'] = 'No data'
    
    #%%
    # dir
    if 'dir' in list(data[station_ids[i]]['month'][months[j]].keys()):
        # SWDR
        if len(data[station_ids[i]]['month'][months[j]]['dir']) + 1*24*60 > minPerMonth[j]:
            data[station_ids[i]]['month'][months[j]]['dir_missing_dp'] = 0
        else:
            if len(data[station_ids[i]]['month'][months[j]]['dir']) < minPerMonth[j]:
                data[station_ids[i]]['month'][months[j]]['dir_missing_dp'] = \
                     minPerMonth[j] - len(data[station_ids[i]]['month'][months[j]]['dir'])
                print('Incomplete direct radiation dataset in station %s in month %s!' %(station_ids[i], months[j]))
            else:
                data[station_ids[i]]['month'][months[j]]['dir_missing_dp'] = 0
    else:
        data[station_ids[i]]['month'][months[j]]['dir_missing_dp'] = 'No data'
      
    #%%
    # dif
    if 'dif' in list(data[station_ids[i]]['month'][months[j]].keys()):
        # SWDR
        if len(data[station_ids[i]]['month'][months[j]]['dif']) + 1*24*60 > minPerMonth[j]:
            data[station_ids[i]]['month'][months[j]]['dif_missing_dp'] = 0
        else:
            if len(data[station_ids[i]]['month'][months[j]]['dif']) < minPerMonth[j]:
                data[station_ids[i]]['month'][months[j]]['dif_missing_dp'] = \
                     minPerMonth[j] - len(data[station_ids[i]]['month'][months[j]]['dif'])
                print('Incomplete diffuse radiation dataset in station %s in month %s!' %(station_ids[i], months[j]))
            else:
                data[station_ids[i]]['month'][months[j]]['dif_missing_dp'] = 0
    else:
        data[station_ids[i]]['month'][months[j]]['dif_missing_dp'] = 'No data'
    
    #%%
    return data[station_ids[i]]['month'][months[j]]['glo_missing_dp'], \
           data[station_ids[i]]['month'][months[j]]['dir_missing_dp'], \
           data[station_ids[i]]['month'][months[j]]['dif_missing_dp']