#%%
# Import libraries
import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np

#%%
from data_import import data_overview

#%%
def get_BSRN_stations(location_BSRN_overview):
    filename = 'BSRN_stations'
#    path = './data/' + filename + '.csv'
    path = './data_import/data/' + filename + '.csv'
    f = open(path)
    reader = csv.reader(f, delimiter = ';')
    stations = list(reader)


    c = -1
    while stations[c][0] == '':
        c -= 1

    stations = stations[0:c+1][:]

    ov_station_name = []
    ov_station_abbrev = []
    ov_station_location = []
    ov_station_lat = []
    ov_station_lon = []
    ov_station_alt = []
    ov_station_start_date = []
    ov_station_end_date = []
    ov_station_comment = []
    ov_station_id = []
    ov_station_surf = []
    ov_station_topo = []
    ov_station_scientist = []
    ov_station_tz_name = []
    ov_station_utcdiffh = []
    ov_station_utcdiffmin = []
    ov_station_dstyn = []
    ov_station_dststart = []
    ov_station_dstend = []
    ov_station_dstdiff = []


    for i in range(1, len(stations)):
        ov_station_name.append(stations[i][0])
        ov_station_abbrev.append(stations[i][1])
        ov_station_location.append(stations[i][2])
        ov_station_lat.append(float(stations[i][3]))
        ov_station_lon.append(float(stations[i][4]))
        ov_station_alt.append(stations[i][5])
        ov_station_start_date.append(stations[i][6])
        ov_station_end_date.append(stations[i][7])
        ov_station_comment.append(stations[i][8])
        ov_station_tz_name.append(stations[i][9])
        ov_station_utcdiffh.append(int(stations[i][10]))
        ov_station_utcdiffmin.append(int(stations[i][11]))
        ov_station_dstyn.append(stations[i][12])
        ov_station_dststart.append(stations[i][13])
        ov_station_dstend.append(stations[i][14])
        if ov_station_dstyn[-1] == 'y':
            ov_station_dstdiff.append(int(stations[i][15]))
        else:
            ov_station_dstdiff.append(stations[i][15])


#        j = i - 1
    for j in range(0, len(ov_station_comment)):
        if 'BSRN station' in ov_station_comment[j]:
            start_ind = ov_station_comment[j].find('BSRN station no: ') + len('BSRN station no: ')
            end_ind = ov_station_comment[j].find('; ', start_ind)
            ov_station_id.append(int(ov_station_comment[j][start_ind:end_ind]))

            start_ind = ov_station_comment[j].find('; Surface type: ') + len('; Surface type: ')
            end_ind = ov_station_comment[j].find('; Topography type: ', start_ind)
            ov_station_surf.append(ov_station_comment[j][start_ind:end_ind])

            start_ind = ov_station_comment[j].find('; Topography type: ') + len('; Topography type: ')
            end_ind = ov_station_comment[j].find('; Station scientist: ', start_ind)
            ov_station_topo.append(ov_station_comment[j][start_ind:end_ind])

            start_ind = ov_station_comment[j].find('; Station scientist: ') + len('; Station scientist: ')
            end_ind = len(ov_station_comment[j])
            ov_station_scientist.append(ov_station_comment[j][start_ind:end_ind])

        elif 'BSRN Candidate.' in ov_station_comment[j]:
            start_ind = ov_station_comment[j].find('Station no: ') + len('Station no: ')
            end_ind = ov_station_comment[j].find('; ', start_ind)
            ov_station_id.append(int(ov_station_comment[j][start_ind:end_ind]))

            if '; Surface type: ' in ov_station_comment[j] and '; Topography type: ' in ov_station_comment[j]:
                start_ind = ov_station_comment[j].find('; Surface type: ') + len('; Surface type: ')
                end_ind = ov_station_comment[j].find('; Topography type: ', start_ind)
                ov_station_surf.append(ov_station_comment[j][start_ind:end_ind])

                start_ind = ov_station_comment[j].find('; Topography type: ') + len('; Topography type: ')
                end_ind = ov_station_comment[j].find('; Station scientist: ', start_ind)
                ov_station_topo.append(ov_station_comment[j][start_ind:end_ind])
            else:
                ov_station_surf.append('unknown')
                ov_station_topo.append('unknown')
            start_ind = ov_station_comment[j].find('; Station scientist: ') + len('; Station scientist: ')
            end_ind = len(ov_station_comment[j])
            ov_station_scientist.append(ov_station_comment[j][start_ind:end_ind])

        for j in range(0, len(ov_station_topo)):
            if ';' in ov_station_topo[j]:
                ov_station_topo[j] = ov_station_topo[j].split(';')[0]

    return ov_station_name, ov_station_abbrev, ov_station_location, ov_station_lat, ov_station_lon, \
    ov_station_alt, ov_station_start_date, ov_station_end_date, ov_station_comment, \
    ov_station_id, ov_station_surf, ov_station_topo, ov_station_scientist,\
    ov_station_tz_name, ov_station_utcdiffh, ov_station_utcdiffmin, ov_station_dstyn, \
    ov_station_dststart, ov_station_dstend, ov_station_dstdiff

#%%
def read_file(str):
    path = str
    f = open(path)
    reader = csv.reader(f)
    df = list(reader)

    for i in range(0, len(df)):
        if len(df[i]) == 0:
            df[i] = ''
        else:
            df[i] = df[i][0]

    return df

#%%
def get_station_info(df, i):
    ind_station_info = [j for j, s in enumerate(df[:]) if '0001' in s[2:6]]

    if len(ind_station_info) > 1:
        print('Warning: found \'0001\' more than once in file with i = ', str(i), 'at indices ', str(ind_station_info), '!')
    if len(ind_station_info) == 0:
        print('Warning: did not find \'0001\' in file with i = ', str(i), '!')

    station_info = df[ind_station_info[0]+1].split()
    station_info = [int(station_info[i]) for i in range(0, len(station_info))]

    station_id = station_info[0]
    station_month = station_info[1]
    station_year = station_info[2]

    return station_id, station_month, station_year

#%%
def get_station_info_2(df, i):
    ind_station_info_2 = [j for j, s in enumerate(df[:]) if '0004' in s[2:6]]

    if len(ind_station_info_2) > 1:
        print('Warning: found \'0004\' more than once in file with i = ', str(i), 'at indices ', str(ind_station_info_2), '!')
    if len(ind_station_info_2) == 0:
        print('Warning: did not find \'0004\' in file with i = ', str(i), '!')

    station_info_21 = df[ind_station_info_2[0]+2].split()
    station_info_21 = [int(station_info_21[i]) for i in range(0, len(station_info_21))]
    station_info_22 = df[ind_station_info_2[0]+6].split()
    station_info_22 = [station_info_22[i] for i in range(0, len(station_info_22))]
    surface_type = station_info_21[0]
    topography_type = station_info_21[1]
    lat = float(station_info_22[0]) - 90 # -90 is the correction from the BSRN format to the ISO-6709 format
    lon = float(station_info_22[1]) - 180 #> -180 is the correction from the BSRN format to the ISO-6709 format
    alt = float(station_info_22[2])

    return surface_type, topography_type, lat, lon, alt

#%%
def get_data_indices(df, i):
    ind_data = [i for i, s in enumerate(df[:]) if '0100' in s[2:6]]
    if len(ind_data) > 1:
        print('Warning: found \'0100\' more than once in file with i = ', str(i), 'at indices ', str(ind_data), '!')
    if len(ind_data) == 0:
        print('Warning: did not find \'0100\' in file with i = ', str(i), '!')
    if len(ind_data) == 1:
        ind_data = ind_data[0]+1

    ind_end_data = [i for i, s in enumerate(df[:]) if '0200' in s[2:6]]
    if len(ind_end_data) == 0:
        ind_end_data.append([i for i, s in enumerate(df[:]) if '0300' in s[2:6]])
        ind_end_data.append([i for i, s in enumerate(df[:]) if '0400' in s[2:6]])
        ind_end_data.append([i for i, s in enumerate(df[:]) if '0500' in s[2:6]])
        ind_end_data.append([i for i, s in enumerate(df[:]) if '1000' in s[2:6]])
        ind_end_data.append([i for i, s in enumerate(df[:]) if '1100' in s[2:6]])
        ind_end_data.append([i for i, s in enumerate(df[:]) if '1200' in s[2:6]])
        ind_end_data.append([i for i, s in enumerate(df[:]) if '1300' in s[2:6]])
        ind_end_data.append([i for i, s in enumerate(df[:]) if '1500' in s[2:6]])
        ind_end_data.append([i for i, s in enumerate(df[:]) if '3010' in s[2:6]])
        ind_end_data.append([i for i, s in enumerate(df[:]) if '3030' in s[2:6]])
        ind_end_data.append([i for i, s in enumerate(df[:]) if '3300' in s[2:6]])
        ind_end_data.append([i for i, s in enumerate(df[:]) if '4000' in s[2:6]])

    ind_end_data = [val for sublist in ind_end_data for val in sublist]

    if len(ind_end_data) > 1:
        ind_end_data = min(ind_end_data)-1
    elif len(ind_end_data) == 1:
        ind_end_data = ind_end_data[0]-1
    elif len(ind_end_data) == 0:
        ind_end_data = len(df)

    if isinstance( ind_data, int ) == False:
        print('ind_data at filenumber indices[i] with i = ', str(i))
    if isinstance( ind_end_data, int ) == False:
        print('ind_data at filenumber indices[i] with i = ', str(i))

    return ind_data, ind_end_data

#%%
def getData(df, ind_data, ind_end_data, station_month, station_year, i, n):
    if n < 100:
        print('File %02d out of %02d' % (i+1, n))
    elif 1000 > n >= 100:
        print('File %03d out of %03d' % (i+1, n))
    elif 10000 > n >= 1000:
        print('File %04d out of %04d' % (i+1, n))

    # raw data
    station_data_l1 = df[ind_data:ind_end_data-1:2]
    station_data_l2 = df[ind_data+1:ind_end_data:2]

    # date and time information
    year = [station_year]*len(station_data_l1)
    month = [station_month]*len(station_data_l1)
    day = [int(station_data_l1[p][0:3].strip()) for p in range(0, len(station_data_l1))]
    min_of_day = [int(station_data_l1[p][4:8].strip()) for p in range(0, len(station_data_l1))]
    hour = [min_of_day[p] // 60 for p in range(0, len(min_of_day))]
    minute = [min_of_day[p] % 60 for p in range(0, len(min_of_day))]

    date_time = [datetime.datetime(year[p], month[p], day[p], hour[p], minute[p]) for p in range(0, len(station_data_l1))]

    # gloabal radiation
    raw_glo_rad = [station_data_l1[p][11:31].strip().split() for p in range(0, len(station_data_l1))]
    glo_rad_mean = [float(raw_glo_rad[p][0]) for p in range(0, len(raw_glo_rad))]

    # direct radiation
    raw_dir_rad = [station_data_l1[p][34:54].strip().split() for p in range(0, len(station_data_l1))]
    dir_rad_mean = [float(raw_dir_rad[p][0]) for p in range(0, len(raw_dir_rad))]

    # diffuse radiation
    raw_dif_rad = [station_data_l2[p][11:31].strip().split() for p in range(0, len(station_data_l2))]
    dif_rad_mean = [float(raw_dif_rad[p][0]) for p in range(0, len(raw_dif_rad))]

    # detect missing values and mark them as NA
    for i in range(0, len(glo_rad_mean)):
        if glo_rad_mean[i] == -999.0 or glo_rad_mean[i] == -99.0:
            glo_rad_mean[i] = float('NaN')

    for i in range(0, len(dir_rad_mean)):
        if dir_rad_mean[i] == -999.0 or dir_rad_mean[i] == -99.0:
            dir_rad_mean[i] = float('NaN')

    for i in range(0, len(dif_rad_mean)):
        if dif_rad_mean[i] == -999.0 or dif_rad_mean[i] == -99.0:
            dif_rad_mean[i] = float('NaN')

    return date_time, glo_rad_mean, dir_rad_mean, dif_rad_mean

#%%
def nan_finder(data, station_id, station_month):
    # Replace empty values with NANs and count them

    # glo
    data[str(station_id)]['month'][str(station_month)]['glo_NANs'] = \
         list(np.isnan(data[str(station_id)]['month'][str(station_month)]['glo'])).count(1)

    # dir
    data[str(station_id)]['month'][str(station_month)]['dir_NANs'] = \
         list(np.isnan(data[str(station_id)]['month'][str(station_month)]['dir'])).count(1)

    # dif
    data[str(station_id)]['month'][str(station_month)]['dif_NANs'] = \
         list(np.isnan(data[str(station_id)]['month'][str(station_month)]['dif'])).count(1)

    return  data[str(station_id)]['month'][str(station_month)]['glo_NANs'], \
            data[str(station_id)]['month'][str(station_month)]['dir_NANs'], \
            data[str(station_id)]['month'][str(station_month)]['dif_NANs']

#%%
def identify_stations_by_year(file_station, file_year, file_month, year_of_interest, location_BSRN_database_without_extension):

    if year_of_interest in [1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999]:
         indices = [i for i, x in enumerate(file_year) if x == int(year_of_interest-1900)]
         n = len(indices)
    else:
         indices = [i for i, x in enumerate(file_year) if x == int(year_of_interest-2000)]
         n = len(indices)

    number_of_stations = len(set([file_station[indices[p]] for p in range(0, n)]))
    stations_year_of_interest = set([file_station[indices[p]] for p in range(0, n)])
    file_paths = []
    for i in range(0, n):
        file_paths.append(location_BSRN_database_without_extension + file_station[indices[i]] + '%02d' % file_month[indices[i]] + '%02d' %  file_year[indices[i]] + '.dat')

    print('There are %d station files from %d stations available in the chosen year %d' %(n, number_of_stations, year_of_interest))

    return file_paths, n, stations_year_of_interest

#%%
def combine_station_information(ov_station_id, station_id):

    ov_index = ov_station_id.index(station_id)

    return ov_index

#%%
def control_plot(date_time, glo_rad_mean, dir_rad_mean, dif_rad_mean, ov_ind, ov_station_name, station_month, station_year):

    plt.close('all')

    f, ax = plt.subplots(3, figsize=(14, 12), sharex = True)

    ax[0].plot(date_time, glo_rad_mean)
    ax[0].grid('on')
    ax[0].set_ylabel('global radiation')
    plt.title(ov_station_name[ov_ind] + '_' + str(station_month) + '_' + str(station_year))

    ax[1].plot(date_time, dir_rad_mean)
    ax[1].grid('on')
    ax[1].set_ylabel('direct radiation')

    ax[2].plot(date_time, dif_rad_mean)
    ax[2].grid('on')
    ax[2].set_ylabel('diffuse radiation')

    plt.xlim([min(date_time), max(date_time)])
    path = '/mnt/Data/Dropbox (ARTORG)/PhD_Data/0_SolarRadiationSW_Data/Test/'
    figure_name = ''.join([path, ov_station_name[ov_ind], '%02d' % station_month, '%02d' % station_year, '.pdf'])
    plt.savefig(figure_name)
    # plt.show()
    return

#%%
def control_plot_yearly(data, station_id, ov_station_name, station_year):

    available_months = list(data[str(station_id)]['month'].keys())

    print('Plotting the yearly control plot of station ' + ov_station_name[data[str(station_id)]['ov_ind']])
    print('The station id is ' + str(data[str(station_id)]['ov_ind']))


    plt.close('all')

    counter  = 1
    f, ax = plt.subplots(len(available_months), figsize=(14, 12))
    for i in available_months:
        plt.subplot(len(available_months),1,counter)
        plt.plot(data[str(station_id)]['month'][i]['date_time'], data[str(station_id)]['month'][i]['glo'])
        plt.xlim([min(data[str(station_id)]['month'][i]['date_time']), max(data[str(station_id)]['month'][i]['date_time'])])
        # ax[i].grid('on')
        plt.ylabel('glo')
        plt.subplots_adjust(hspace = 0.6)
        if i == 0:
            plt.title(str(station_year)  + ': ' +  ov_station_name[data[str(station_id)]['ov_ind']])
        counter += 1

    plt.tight_layout()
    path = './results/YearlyControlPlots/'
    figure_name = ''.join([path, '%02d' % station_year,  '_', ov_station_name[data[str(station_id)]['ov_ind']], '_YearlyOverview', '.pdf'])
    plt.savefig(figure_name)
    # plt.show()
    return


#%%
def get_station_name(station_id, ov_station_id, ov_station_name):

    ind = ov_station_id.index(int(station_id))
    station_name = ov_station_name[ind]

    return station_name

#%%
def main(location_BSRN_overview, year_of_interest, location_BSRN_database_without_extension):
    # get basic information on stations
    ov_station_name, ov_station_location, ov_station_lat, ov_station_lon, \
    ov_station_alt, ov_station_start_date, ov_station_end_date, ov_station_comment, \
    ov_station_id, ov_station_surf, ov_station_topo, ov_station_scientist \
    = get_BSRN_stations(location_BSRN_overview)

    # get overview of existing data
    file_station, file_year, file_month, station_abbrevs, number_of_stations, \
    all_years, number_of_years, all_months, number_of_months, number_of_datasets, \
    start_of_stationloop, end_of_stationloop = data_overview.get_file_overview(location_BSRN_overview)

    # display information of the data in the current year, get file-paths
    file_paths, n = identify_stations_by_year(file_station, file_year, file_month, year_of_interest, location_BSRN_database_without_extension)


    for i in range(0, n):
        # read the file and extract information
        df = read_file(file_paths[i])

        station_id, station_month, station_year = get_station_info(df, i)

        surface_type, topography_type, lat, lon, alt = get_station_info_2(df, i)

        ov_ind = combine_station_information(ov_station_id, station_id)

        ind_data, ind_end_data = get_data_indices(df, i)

        date_time, glo_rad_mean, dir_rad_mean, dif_rad_mean = \
            getData(df, ind_data, ind_end_data, station_month, station_year, i)

        # controlplot
        control_plot(date_time, glo_rad_mean, dir_rad_mean, dif_rad_mean, ov_ind, ov_station_name, station_month, station_year)

    return

#%%
if __name__ == "__main__":
    main(location_BSRN_overview, year_of_interest, location_BSRN_database_without_extension)
