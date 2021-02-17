#%%
# Import libraries
import numpy as np
import matplotlib.pyplot as plt

#%%
# Computing the temporal resolution
def compute_glo_sum(data, station_ids, months, i, j):

    res = []

    for p in range(0, len(data[str(station_ids[i])]['month'][months[j]]['dir'])):
        res.append(data[station_ids[i]]['month'][months[j]]['dir'][p] * \
        np.cos(data[station_ids[i]]['month'][months[j]]['sza'][p]) + \
        data[station_ids[i]]['month'][months[j]]['dif'][p])

    return res

#%%
# SWsum vs SWDR plot
def SWsum_vs_SWDR_plot(data, station_ids, months, i, j, month_names):

    for i in range(0, len(station_ids)):

        months = list(data[station_ids[i]]['month'].keys())
        number_of_subplots=len(months)

        # Subplots are organized in a Rows x Cols Grid
        # Tot and Cols are known
        Tot = number_of_subplots
        Cols = 3

        # Compute Rows required
        Rows = Tot // Cols
        Rows += Tot % Cols

        # Create a Position index
        Position = range(1,Tot + 1)

        fig = plt.figure(figsize=(14, 9))

        for j in range(Tot):
          # add every single subplot to the figure with a for loop

            fig.add_subplot(Rows,Cols,Position[j])
            plt.plot(data[station_ids[i]]['month'][months[j]]['glo'], data[station_ids[i]]['month'][months[j]]['glo_sum'], '*')
            plt.grid('on')
            plt.xlabel('SWD [W/m2]')
            plt.ylabel('SumSW [W/m2]')
            plt.title('%s, %s' %(data[station_ids[i]]['station_name'], month_names[int(months[j])-1]))

        fig.tight_layout()
        figname = './results/swd_vs_swsum_plots/S%s.pdf' % data[station_ids[i]]['station_name']
        plt.savefig(figname)
        plt.show()
        plt.close()

    return

#%%
# Computing the temporal resolution
def compute_temporal_res(data, station_ids, months, i, j):
    FirstTime = data[station_ids[i]]['month'][months[j]]['date_time'][0].minute
    SecondTime = data[station_ids[i]]['month'][months[j]]['date_time'][1].minute
    MinPerDP = SecondTime - FirstTime

    if MinPerDP != 1:
        FirstTimeAlternative = data[station_ids[i]]['month'][months[j]]['date_time'][1].minute
        SecondTimeAlternative = data[station_ids[i]]['month'][months[j]]['date_time'][2].minute
        MinPerDP = FirstTimeAlternative - SecondTimeAlternative
        data[station_ids[i]]['month'][months[j]]['TempRes'] = MinPerDP
        if MinPerDP != 1:
            print('ATTENTION: There is a temp. res. < 1 DP/min')
    else:
        data[station_ids[i]]['month'][months[j]]['TempRes'] = MinPerDP

    return data[station_ids[i]]['month'][months[j]]['TempRes']

#%%
# Computing the total radiation per month
def compute_monthly_radiation(data, station_ids, months, i, j, month_names):
    if 'glo' in data[station_ids[i]]['month'][months[j]].keys():
        if True in set(np.isnan(data[station_ids[i]]['month'][months[j]]['glo'])):
            NANfinder = np.isnan(np.array(data[station_ids[i]]['month'][months[j]]['glo'], dtype=np.float64))
            NanIndices = [p for p, x in enumerate(NANfinder) if x == 1]
            del NANfinder
        else:
            NanIndices = []

        toIntegrate = [data[station_ids[i]]['month'][months[j]]['glo'][p] for p, \
                       data[station_ids[i]]['month'][months[j]]['glo'][p] in \
                       enumerate(data[station_ids[i]]['month'][months[j]]['glo'])\
                       if p not in NanIndices]

        data[station_ids[i]]['month'][months[j]]['glo_monthly_radiation'] = \
            np.trapz(toIntegrate)*data[station_ids[i]]['month'][months[j]]['TempRes']*60        # *60 for min to s conversion
        del NanIndices

    else:
        print('No global radiation data available in station %s in month %s!' \
              %(data[station_ids[i]]['station_name'], month_names[int(months[j])-1]))

    return data[station_ids[i]]['month'][months[j]]['glo_monthly_radiation']

#%%
# Calculating some annual values
def get_annual_values(end_loop, data, station_ids, months, i):
    start_loop = 0

    if ['glo' in data[station_ids[i]]['month'][months[p]].keys() for p in range(start_loop, end_loop)] == [True]*end_loop:
        # Loop through monthly values
        nan_collector = 0
        dp_total = 0
        rad_total = 0
        dp_yearly_missing = 0
        for p in range(start_loop, end_loop):
            dp_total += len(data[station_ids[i]]['month'][months[p]]['glo'])
            nan_collector += data[station_ids[i]]['month'][months[p]]['glo_NANs']
            rad_total +=  data[station_ids[i]]['month'][months[p]]['monthly_radiation']
            if data[station_ids[i]]['month'][months[p]]['glo_missing_dp'] != 'No data':
                dp_yearly_missing += data[station_ids[i]]['month'][months[p]]['glo_missing_dp']

        dp_empty_perc = nan_collector / dp_total * 100
        dp_missing_perc = dp_yearly_missing / dp_total * 100
        dp_bad_perc = (nan_collector + dp_yearly_missing) / dp_total * 100

    else:
        print('No \'glo\' in list for station %d' % i)
        nan_collector = np.nan
        dp_total = np.nan
        rad_total = np.nan
        dp_yearly_missing = np.nan
        dp_empty_perc = np.nan
        dp_missing_perc = np.nan
        dp_bad_perc = np.nan

    return dp_total, nan_collector, rad_total, dp_yearly_missing, \
        dp_empty_perc, dp_missing_perc, dp_bad_perc

#%% annual estimated power output
def get_annual_mean_power_estimate(data, station_ids, user_name, cell_area_m2, months, i):
    # generate keys
    for j in range(0, len(months)):
        data[station_ids[i]]['yearly']['outside_time_glo_filled_whole_year'] = {}
        data[station_ids[i]]['yearly']['mean_power_estimate'] = {}
        for m in range(0, len(user_name)):
            data[station_ids[i]]['yearly']['outside_time_glo_filled_whole_year'][str(m)] = []
            data[station_ids[i]]['yearly']['mean_power_estimate'][str(m)] = []
    # save values
    for j in range(0, len(months)):
        for m in range(0, len(user_name)):
            data[station_ids[i]]['yearly']['outside_time_glo_filled_whole_year'][str(m)].extend(\
            data[station_ids[i]]['month'][months[j]]['outside_time_glo_filled'][m])
    # mean values
    for m in range(0, len(user_name)):
        data[station_ids[i]]['yearly']['mean_power_estimate'][str(m)] = \
            np.nanmean([data[station_ids[i]]['yearly']['outside_time_glo_filled_whole_year'][str(m)][p] \
                        *.2*.2*cell_area_m2 for p in range(0, len(data[station_ids[i]]['yearly']['outside_time_glo_filled_whole_year'][str(m)]))])
    return data

#%% annual estimated power output
def get_annual_mean_power_isc(data, station_ids, user_name, cell_area_m2, months, i):
    # generate keys
    for j in range(0, len(months)):
        data[station_ids[i]]['yearly']['mean_power_isc'] = {}
        data[station_ids[i]]['yearly']['power_isc_whole_year'] = {}
        for m in range(0, len(user_name)):
            data[station_ids[i]]['yearly']['mean_power_isc'][str(m)] = []
            data[station_ids[i]]['yearly']['power_isc_whole_year'][str(m)] = []
    # save values
    for j in range(0, len(months)):
        for m in range(0, len(user_name)):
            data[station_ids[i]]['yearly']['power_isc_whole_year'][str(m)].extend(\
            data[station_ids[i]]['month'][months[j]]['p_calc'][str(m)])
    # mean values
    for m in range(0, len(user_name)):
        data[station_ids[i]]['yearly']['mean_power_isc'][str(m)] = \
            np.nanmean(data[station_ids[i]]['yearly']['power_isc_whole_year'][str(m)])

    return data
