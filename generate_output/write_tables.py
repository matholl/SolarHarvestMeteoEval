import csv
import os
import numpy as np

#%%
def write_monthly_mean_power_estimate_in_table(data, station_ids, months, year_of_interest, user_name, table_path, i):
    if not os.path.exists(table_path):
        os.makedirs(table_path)

    # generate user specific lists and write them to file
    filename = str(year_of_interest) + '_' + str(data[station_ids[i]]['station_name'].replace(" ", "")) + '_' + 'estimated_power.csv'
    csvfile = table_path + filename

    months = list(data[station_ids[i]]['month'].keys())

    user_estpow_monthly_collector = {}
    for j in range(0, len(months)):
        for m in range(0, len(data[station_ids[i]]['month'][months[j]]['mean_power_estimate'])):
            user_estpow_monthly_collector['user_'+str(m)] = ['user_'+str(m), user_name[m]]


    for j in range(0, len(months)):
        for m in range(0, len(data[station_ids[i]]['month'][months[j]]['mean_power_estimate'])):
            user_estpow_monthly_collector['user_'+str(m)].append(data[station_ids[i]]['month'][months[j]]['mean_power_estimate'][m])

    months_with_label = ['months'] + [' '] + months

    rows = zip(months_with_label, user_estpow_monthly_collector['user_0'], user_estpow_monthly_collector['user_1'], user_estpow_monthly_collector['user_2'], \
               user_estpow_monthly_collector['user_3'], user_estpow_monthly_collector['user_4'], user_estpow_monthly_collector['user_5'], \
               user_estpow_monthly_collector['user_6'])
    with open(csvfile, 'w') as output:
        writer = csv.writer(output, lineterminator='\n')
        for m in range(0, len(data[station_ids[i]]['month'][months[j]]['mean_power_estimate'])):
            for row in rows:
                writer.writerow(row)

    return

#%%
def write_monthly_mean_power_isc_based_in_table(data, station_ids, months, year_of_interest, user_name, table_path, i):
    if not os.path.exists(table_path):
        os.makedirs(table_path)

    # generate user specific lists and write them to file
    filename = str(year_of_interest) + '_' + str(data[station_ids[i]]['station_name'].replace(" ", "")) + '_' + 'isc_based_power.csv'
    csvfile = table_path + filename

    months = list(data[station_ids[i]]['month'].keys())

    user_isc_p_monthly_collector = {}
    for j in range(0, len(months)):
        for m in range(0, len(user_name)):
            user_isc_p_monthly_collector['user_'+str(m)] = ['user_'+str(m), user_name[m]]

    for j in range(0, len(months)):
        for m in range(0, len(user_name)):
            if m != 7:
                user_isc_p_monthly_collector['user_'+str(m)].append(np.nanmean(data[station_ids[i]]['month'][months[j]]['p_calc'][str(m)]))
            if m == 7:
                user_isc_p_monthly_collector['user_'+str(m)].append(np.nanmean(data[station_ids[i]]['month'][months[j]]['p_calc'][str(2)]) + (13/104) * np.nanmean(data[station_ids[i]]['month'][months[j]]['p_calc'][str(5)]) + (91/104) *  np.nanmean(data[station_ids[i]]['month'][months[j]]['p_calc'][str(6)]))

    # append yearly values (calculated from mean_power_isc or from p_calc)
    months.append('yearly mean_power_isc')
    for m in range(0, len(user_name)):
        user_isc_p_monthly_collector['user_'+str(m)].append(data[station_ids[i]]['yearly']['mean_power_isc'][str(m)])

    months.append('yearly mean of monthly p_calc')
    for m in range(0, len(user_name)):
        if m != 7:
            user_isc_p_monthly_collector['user_'+str(m)].append(np.nanmean([np.nanmean(data[station_ids[i]]['month'][months[j]]['p_calc'][str(m)]) for j in range(0, len(data[station_ids[i]]['month'].keys()))]))
        if m == 7:
            user_isc_p_monthly_collector['user_'+str(m)].append(np.nanmean([    np.nanmean(data[station_ids[i]]['month'][months[j]]['p_calc'][str(2)]) \
                                                                                + (13/104) * np.nanmean(data[station_ids[i]]['month'][months[j]]['p_calc'][str(5)]) \
                                                                                + (91/104) * np.nanmean(data[station_ids[i]]['month'][months[j]]['p_calc'][str(6)]) \
                                                                                for j in range(0, len(data[station_ids[i]]['month'].keys()))]))

    months_with_label = ['months'] + [' '] + months

    rows = zip(months_with_label, user_isc_p_monthly_collector['user_0'], user_isc_p_monthly_collector['user_1'], user_isc_p_monthly_collector['user_2'], \
               user_isc_p_monthly_collector['user_3'], user_isc_p_monthly_collector['user_4'], user_isc_p_monthly_collector['user_5'], \
               user_isc_p_monthly_collector['user_6'],user_isc_p_monthly_collector['user_7'])
    with open(csvfile, 'w') as output:
        writer = csv.writer(output, lineterminator='\n')
        for m in range(0, len(user_name)):
            for row in rows:
                writer.writerow(row)

    return
