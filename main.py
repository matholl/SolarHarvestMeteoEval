#%% Timer start
# Import timer
import time
# Timer begins
start_time = time.time()

#%% Import libraries
import numpy as np
import sys
import pickle

#%% import modules
# loading data
from data_import import read_station_archive_format
from data_import import definitions
from data_import import payerne15_data

# process data
from data_processing import check_incomplete_data
from data_processing import get_timezone
from data_processing import solarZenithAngleNOAA
from data_processing import negative_to_zero

# computations
from computations import general_computations
from computations import gfactor
from computations.artificial_user_profiles import get_artificial_user_profiles
from computations.get_power import get_closest_am
from computations.get_power import currdensv
from computations.get_power import ocvoltage
from computations.get_power import power_output

# generate output
from generate_output import write_tables
from generate_output import plot

#%%

###############################################################################
######################### Manual input ########################################
###############################################################################
#%%
# Generate new pickle dump y (1) / n (0)
pickleDump = 0

# test a specific station with index i
test_specific_station = 0
test_station_id = 1
if test_specific_station == 1:
    print('This is a testrun for station with id = ' + str(test_station_id))

# year format: 4 digit year, 1992 - 2017
year_of_interest = 2015

# computations.py
show_swsum_vs_swd_plot = 0

#interpolation range for eqe, bashkatov and SMARTS data
interp_range = np.arange(300, 2510, 10)

# for power calculation
cell_area_m2 = 3.6*1e-4

###############################################################################
######################### File structure ######################################
###############################################################################

#%% read_station_archive_format.py

# dataloc = 'D:/Dropbox (ARTORG)/PhD_Data/0_SolarRadiationSW_Data'
dataloc = '/mnt/Data/Dropbox (ARTORG)/PhD_Data/0_SolarRadiationSW_Data'
# dataloc = '/mnt/FAST/Max/0_SolarRadiationSW_Data'


location_BSRN_database = dataloc + '/BSRN_FullDatabase/*dat'
location_BSRN_database_without_extension = dataloc + '/BSRN_FullDatabase/'
location_BSRN_overview = dataloc + '/BSRN_Stations/'

#%% payerne15_data.py
pay_path = './data_import/payerne/'

#%% get_ocv.py
ocv_path = './data_import/data/OCV_IXYS_Cell.csv'

#%% get_cdv.py
cdv_path = './data_import/data/CurrentDensity_Voltage_IXYS_Cell.csv'

#%% get_artificial_user_profiles.py
path_artificial_user_profiles = './computations/artificial_user_profiles/'

#%% EQE.py
IXYS_EQE_path = './data_import/data/EQE_IXYS_Cell.csv'
EMPA_EQE_path = './data_import/data/CIGS_performance_Empa.csv'

#%% pickle path
pickle_path = dataloc + '/pickle/Bashka_2_5mm_3_6cm2/data' + str(year_of_interest)

#%% plot.py
plot_path = './results/estimated_power/'

#%% write_tables.py
table_path = './results/estimated_power/'

###############################################################################
########################### Data input ########################################
###############################################################################

if pickleDump == 1:
    #%% definitions.py
    #%%
    month_names, daysPerMonth, minPerMonth = \
        definitions.definitions()

    #%% read_station_archive_format.py
    #%%
    # get basic information on stations
    ov_station_name, ov_station_abbrev, ov_station_location, ov_station_lat, ov_station_lon, \
    ov_station_alt, ov_station_start_date, ov_station_end_date, ov_station_comment,\
    ov_station_id, ov_station_surf, ov_station_topo, ov_station_scientist,\
    ov_station_tz_name, ov_station_utcdiffh, ov_station_utcdiffmin, ov_station_dstyn, \
    ov_station_dststart, ov_station_dstend, ov_station_dstdiff = \
        read_station_archive_format.get_BSRN_stations(location_BSRN_overview)

    #%%
    # get overview of existing data
    file_station, file_year, file_month, station_abbrevs, number_of_stations, \
    all_years, number_of_years, all_months, number_of_months, number_of_datasets, \
    start_of_stationloop, end_of_stationloop = \
        read_station_archive_format.data_overview.get_file_overview(location_BSRN_database)

    # display information of the data in the current year, get file-paths
    file_paths, n, stations_year_of_interest = \
        read_station_archive_format.identify_stations_by_year(file_station, \
        file_year, file_month, year_of_interest, location_BSRN_database_without_extension)

    #%%
    # overall data collection dict
    print('Generating data collection dictionaries')
    data = {}

    ov_index_of_chosen_station = ov_station_id.index(test_station_id)
    test_station = ov_station_abbrev[ov_index_of_chosen_station]
    if test_specific_station == 1:
        if 1 in [test_station in file_paths[p] for p in range(0, len(file_paths))]:
            a = [i for i, x in enumerate(file_paths) if test_station in x][0]
            b = [i for i, x in enumerate(file_paths) if test_station in x][-1] + 1
        else:
            print('The chosen station %s is not availble in year %d!' % (ov_station_name[ov_index_of_chosen_station], year_of_interest))
            sys.exit()

    else:
        a = 0
        b = n

    for i in range(a, b):
        # read the file and extract information
        df = \
            read_station_archive_format.read_file(file_paths[i])

        station_id, station_month, station_year = \
            read_station_archive_format.get_station_info(df, i)

        # station specific data collection dict
        if str(station_id) not in data:
            data[str(station_id)] = {}

        if 'month' not in data[str(station_id)]:
             data[str(station_id)]['month'] = {}

        # station and month specific dict
        data[str(station_id)]['month'][str(station_month)] = {}

    #%%
    # collecting data
    print('Collecting data')
    for i in range(a, b):
        # read the file and save information to dicts
        df = read_station_archive_format.read_file(file_paths[i])
        station_id, station_month, station_year = read_station_archive_format.get_station_info(df, i)

        data[str(station_id)]['station_name'] = \
            read_station_archive_format.get_station_name(station_id, ov_station_id, ov_station_name)

        data[str(station_id)]['surface_type'], \
        data[str(station_id)]['topography_type'], \
        data[str(station_id)]['lat'], data[str(station_id)]['lon'], \
        data[str(station_id)]['alt'] = \
            read_station_archive_format.get_station_info_2(df, i)

        data[str(station_id)]['ov_ind'] = \
             read_station_archive_format.combine_station_information(ov_station_id, station_id)

        data[str(station_id)]['month'][str(station_month)]['ind_data'], \
        data[str(station_id)]['month'][str(station_month)]['ind_end_data'] = \
             read_station_archive_format.get_data_indices(df, i)

        data[str(station_id)]['month'][str(station_month)]['date_time'], \
        data[str(station_id)]['month'][str(station_month)]['glo'], \
        data[str(station_id)]['month'][str(station_month)]['dir'], \
        data[str(station_id)]['month'][str(station_month)]['dif'] = \
            read_station_archive_format.getData(df, \
            data[str(station_id)]['month'][str(station_month)]['ind_data'],\
            data[str(station_id)]['month'][str(station_month)]['ind_end_data'],\
            station_month, station_year, i, n)

        data[str(station_id)]['month'][str(station_month)]['glo_NANs'], \
        data[str(station_id)]['month'][str(station_month)]['dir_NANs'], \
        data[str(station_id)]['month'][str(station_month)]['dif_NANs'] = \
             read_station_archive_format.nan_finder(data, station_id, station_month)

        # read_station_archive_format.control_plot(data[str(station_id)]['month'][str(station_month)]['date_time'], \
        #                                         data[str(station_id)]['month'][str(station_month)]['glo'], \
        #                                         data[str(station_id)]['month'][str(station_month)]['dir'], \
        #                                         data[str(station_id)]['month'][str(station_month)]['dif'], \
        #                                         data[str(station_id)]['ov_ind'], \
        #                                         ov_station_name, station_month, station_year)

        del df, station_month, station_id, station_year

    current_station_ids = list(data.keys())

    print(current_station_ids)

    for i in range(0, len(current_station_ids)):
        read_station_archive_format.control_plot_yearly(data, current_station_ids[i], ov_station_name, year_of_interest)


    #%% include Payern's data of 2015 if year of interest is 2015
    if test_specific_station == 0:
        if year_of_interest == 2015:
            data = payerne15_data.get_pay_15_data(pay_path, data, ov_station_id)
    elif test_specific_station == 1:
        if test_station_id == ov_station_id[ov_station_abbrev.index('pay')]:
            if year_of_interest == 2015:
                data = payerne15_data.get_pay_15_data(pay_path, data, ov_station_id)


    #%%
    station_ids = list(data.keys())

    ###############################################################################
    ######################## Out of staion loop ###################################
    ###############################################################################

    #%% find indices of stations that have 12 months data sets
    full_year_data_ind = []
    for i in range(0, len(station_ids)):
        if len(list(data[station_ids[i]]['month'].keys())) == 12:
            full_year_data_ind.append(i)

    #%% gfactor.py
    #%%
    print('Calculating the overall attenuation factor due to TF and EQE')

    am, am_names, eqe, bashkatov, air_masses = gfactor.get_gfactor_data(interp_range, IXYS_EQE_path, EMPA_EQE_path)
    photon_energy, photon_energy_interp = gfactor.subcutaneous_irradiance.get_photon_energy(am, am_names)
    am = gfactor.subcutaneous_irradiance.get_photonflux(am, am_names, bashkatov, photon_energy_interp)
    am = gfactor.subcutaneous_irradiance.get_irradiance(am, am_names, bashkatov)
    am = gfactor.subcutaneous_irradiance.get_factors(am, am_names, photon_energy, photon_energy_interp)

    #%% get_artificial_user_profiles.py
    user_name, user_description, user_times = get_artificial_user_profiles.get_artificial_user_profiles(path_artificial_user_profiles)

    #%% power.py
    #cdv
    cd_voltage, cd_voltage_name, cd, cd_name = currdensv.get_cdv(cdv_path)

    #ocv
    ocv_irrad, ocv = ocvoltage.get_ocv(ocv_path)

    #%%

    ###############################################################################
    ######################## Data processing ######################################
    ###############################################################################

    #%% check_incomplete_data.py
    #%%
    for i in range(0, len(station_ids)):
        print('Checking for incomplete data-sets of station with id %s' % station_ids[i])
        months = list(data[station_ids[i]]['month'].keys())
        for j in range(0, len(months)):
            data[station_ids[i]]['month'][months[j]]['glo_missing_dp'], \
            data[station_ids[i]]['month'][months[j]]['dir_missing_dp'], \
            data[station_ids[i]]['month'][months[j]]['dif_missing_dp'] = \
                check_incomplete_data.check_incomplete_data(data, station_ids,\
                                                            months, i, j, \
                                                            minPerMonth)

    #%% set negative radiation values due to inaccurate calibration to zero
        data = negative_to_zero.set_negative_radiation_to_zero(data, station_ids, i, months)

        #%% get_timezone.py
        #%%
        print('Finding timezones of station with id %s' % station_ids[i])
        data[station_ids[i]]['UTC_diff_h'], \
        data[station_ids[i]]['Timezone_name'] = \
            get_timezone.get_timezone(data, station_ids, i, ov_station_tz_name, ov_station_utcdiffh,\
                 ov_station_utcdiffmin, ov_station_dstyn, ov_station_dststart,ov_station_dstend, \
                 ov_station_dstdiff, ov_station_id, ov_station_name)



        #%% solarZenithAngleNOAA.py
        #%%
        print('Calculating solar angles, sunrise/-set, air mass and local time of station with id %s' % station_ids[i])

        for j in range(0, len(months)):
            data[station_ids[i]]['month'][months[j]]['sza'], \
            data[station_ids[i]]['month'][months[j]]['saz'], \
            data[station_ids[i]]['month'][months[j]]['local_time'], \
            data[station_ids[i]]['month'][months[j]]['air_mass'], \
            data[station_ids[i]]['month'][months[j]]['sunrise_datetime'], \
            data[station_ids[i]]['month'][months[j]]['sunset_datetime'] = \
            solarZenithAngleNOAA.getSolarZenithAngle(data, station_ids, i, months, j)

        #%%

        ###############################################################################
        ########################## Computations #######################################
        ###############################################################################

        #%% get_artificial_user_profiles.py
        #%%
        print('Collecting user specific indices of station with id %s' % station_ids[i])
        for j in range(0, len(months)):
            data[station_ids[i]]['month'][months[j]]['outside_time_indices'] = \
                get_artificial_user_profiles.get_indices_of_user_outside_times(i, j, data, station_ids, months, user_times, user_name)
            data[station_ids[i]]['month'][months[j]]['outside_time_glo'], \
            data[station_ids[i]]['month'][months[j]]['outside_time_dir'], \
            data[station_ids[i]]['month'][months[j]]['outside_time_dif'], \
            data[station_ids[i]]['month'][months[j]]['outside_time_local_times']= \
                get_artificial_user_profiles.get_outside_time_data(data, i , j, station_ids, \
                months, data[station_ids[i]]['month'][months[j]]['outside_time_indices'])
            data = get_artificial_user_profiles.fill_outside_time_data(data, i , j, station_ids, months)
            data = get_artificial_user_profiles.get_monthly_mean_power_estimate(data, i , j, station_ids, months, cell_area_m2)

        #%% power.py
        #%%
        print('Calculating OCV, ISC and the power output of station with id %s' % station_ids[i])

        #power
        for j in range(0, len(months)):
            data = get_closest_am.get_am(data, station_ids, am, am_names, months, i, j, air_masses)
            data = power_output.subcutaneous_irradiation(data, station_ids, am, am_names, months, i, j)
            data = power_output.get_closest_ocv(ocv_irrad, ocv, data, station_ids, am, am_names, months, i, j)
            data = power_output.get_isc(data, station_ids, am, am_names, months, i, j, eqe, user_name)
            data = power_output.calculate_power(data, station_ids, months, cell_area_m2, i, j, user_name)

        #%% computations.py
        #%% monthly values
        print('Calculating monthly values of station with id %s' % station_ids[i])

        for j in range(0, len(months)):
            data[station_ids[i]]['month'][months[j]]['glo_sum'] = \
                general_computations.compute_glo_sum(data, station_ids, months, i, j)
            data[station_ids[i]]['month'][months[j]]['TempRes'] = \
                general_computations.compute_temporal_res(data, station_ids, months, i, j)
            data[station_ids[i]]['month'][months[j]]['monthly_radiation'] = \
                general_computations.compute_monthly_radiation(data, station_ids, months, i, j, month_names)

        if show_swsum_vs_swd_plot == 1:
            general_computations.SWsum_vs_SWDR_plot(data, station_ids, months, i, j, month_names)

        #%% yearly values
        print('Calculating yearly values of station with id %s' % station_ids[i])

        data[station_ids[i]]['yearly'] = {}

        data[station_ids[i]]['yearly']['dp_total'], \
        data[station_ids[i]]['yearly']['nan_collector'], \
        data[station_ids[i]]['yearly']['rad_total'], \
        data[station_ids[i]]['yearly']['dp_yearly_missing'], \
        data[station_ids[i]]['yearly']['dp_empty_perc'], \
        data[station_ids[i]]['yearly']['dp_missing_perc'], \
        data[station_ids[i]]['yearly']['dp_bad_perc'] = \
            general_computations.get_annual_values(len(list(data[station_ids[i]]['month'].keys())), data, station_ids, months, i)
        data = general_computations.get_annual_mean_power_estimate(data, station_ids, user_name, cell_area_m2, months, i)
        data = general_computations.get_annual_mean_power_isc(data, station_ids, user_name, cell_area_m2, months, i)
        #%%

        ###############################################################################
        ############################# Output ##########################################
        ###############################################################################

        #%% plot.py
        #%% plot estimated power output for user profiles from get_artificial_user_profiles.py
        print('Plotting user-specific mean estimated monthly power output of station with id %s' % station_ids[i])
        plot.plot_estimated_power(data, station_ids, months, year_of_interest, user_name, plot_path, i)
        plot.plot_isc_power(data, station_ids, months, year_of_interest, user_name, plot_path, i)

        #%% write_tables.py
        #%% estimated power output from get_artificial_user_profiles.py
        print('Writing table with user-specific mean estimated monthly power output of station with id %s' % station_ids[i])
        write_tables.write_monthly_mean_power_estimate_in_table(data, station_ids, months, year_of_interest, user_name, table_path, i)
        write_tables.write_monthly_mean_power_isc_based_in_table(data, station_ids, months, year_of_interest, user_name, table_path, i)

        #%% pickle dump
        print('starting pickle of station with id = %s' % station_ids[i])
        # Pickle: save data
        with open(pickle_path + str(station_ids[i]) + '.p', 'wb') as f:
            pickle.dump(data[station_ids[i]], f)
        del data[station_ids[i]]
    print('Saving the am dict')
    with open(pickle_path + '_am.p', 'wb') as f:
            pickle.dump(am, f)
    print('Saving some general variables')
    with open(pickle_path + '_general_variables.p', 'wb') as f:
            pickle.dump([month_names, daysPerMonth, minPerMonth, ov_station_name, ov_station_abbrev, \
                        ov_station_location, ov_station_lat, ov_station_lon, \
                        ov_station_alt, ov_station_start_date, ov_station_end_date, ov_station_comment,\
                        ov_station_id, ov_station_surf, ov_station_topo, ov_station_scientist,\
                        file_paths, n, stations_year_of_interest, station_ids, full_year_data_ind, \
                        am_names, eqe, bashkatov, air_masses, photon_energy, photon_energy_interp, \
                        user_name, user_description, user_times, cd_voltage, cd_voltage_name, cd, cd_name, ocv_irrad, ocv], f)
#%% pickle load
if pickleDump != 1:

    data = {}
    am = {}
    print('Loading some general variables')
    with open(pickle_path + '_general_variables.p', 'rb') as f:
            [month_names, daysPerMonth, minPerMonth, ov_station_name, ov_station_abbrev, \
            ov_station_location, ov_station_lat, ov_station_lon, \
            ov_station_alt, ov_station_start_date, ov_station_end_date, ov_station_comment,\
            ov_station_id, ov_station_surf, ov_station_topo, ov_station_scientist,\
            file_paths, n, stations_year_of_interest, station_ids, full_year_data_ind, \
            am_names, eqe, bashkatov, air_masses, photon_energy, photon_energy_interp, \
            user_name, user_description, user_times, cd_voltage, cd_voltage_name, cd, cd_name, ocv_irrad, ocv] = pickle.load(f)

    print('Loading the am dict')
    with open(pickle_path + '_am.p', 'rb') as f:
            am = pickle.load(f)

    lons = {}
    lats = {}
    labels = {}
    labels_monthly = {}
    for m in range(0, len(user_name)):
        lons[user_name[m]] = []
        lats[user_name[m]] = []
        labels[user_name[m]] = []
        labels_monthly[user_name[m]] = []

    for i in range(0, len(station_ids)):       #station
        print('Loading pickle of station number %02d out of %d' % (i+1, len(station_ids)))
        # Pickle: save data
        with open(pickle_path + str(station_ids[i]) + '.p', 'rb') as f:
            data[station_ids[i]] = pickle.load(f)

        # get list of all available months for the current station
        months = list(data[station_ids[i]]['month'].keys())
        # sort months
        months_int = [int(x) for x in months]
        months_int.sort()
        months = [str(x) for x in months_int]

        #%% plot.py
        #%% plot estimated power output for user profiles from get_artificial_user_profiles.py
        print('Plotting user-specific mean estimated monthly power output of station with id %s' % station_ids[i])
        lons, lats, labels, labels_monthly = plot.collect_data_for_world_map(data, station_ids, months, year_of_interest, user_name, plot_path, i, lons, lats, labels, labels_monthly)
        plot.plot_estimated_power(data, station_ids, months, year_of_interest, user_name, plot_path, i)
        plot.plot_isc_power(data, station_ids, months, year_of_interest, user_name, plot_path, i)

        #%% write_tables.py
        #%% estimated power output from get_artificial_user_profiles.py
        print('Writing table with user-specific mean monthly power output of station with id %s' % station_ids[i])
        write_tables.write_monthly_mean_power_estimate_in_table(data, station_ids, months, year_of_interest, user_name, table_path, i)
        write_tables.write_monthly_mean_power_isc_based_in_table(data, station_ids, months, year_of_interest, user_name, table_path, i)

        #%% save RAM
        del data[station_ids[i]]
    plot.plot_isc_power_on_world_map_circle_method(data, station_ids, year_of_interest, user_name, plot_path, i, lons, lats, labels, labels_monthly)
    plot.world_map_legend(data, station_ids, year_of_interest, user_name, plot_path, i, lons, lats, labels, labels_monthly)

#%% Timer ends
elapsed_time = time.time() - start_time
print ('Total elapsed time: ' + str(round(elapsed_time//60)) + ' min ' + str(round(elapsed_time%60)) + ' sec')
