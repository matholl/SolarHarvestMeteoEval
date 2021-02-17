#%%
# import library
import glob

#%%
def extract_available_data_info(str):
    
    # Extracts station abbreviation, year, month
    
    return str[len(str)-11 : len(str)-8], \
            str[len(str)-8 : len(str)-6], \
            str[len(str)-6 : len(str)-4]

#%%
def print_file_overview(stationsAbbrev, numberOfStations, allYears, numberOfYears,\
                    allMonths, numberOfMonths, numberOfDatasets):
    # Printing some info
    print('List of all stations:')
    print(stationsAbbrev)
    print('Number of available stations: ' + str(numberOfStations))
    print('List of all years:')
    print(allYears)
    print('Number of available years: ' + str(numberOfYears))
    print('List of all months:')
    print(allMonths)
    print('Number of available months: ' + str(numberOfMonths))
    print('Number of datasets: ' + str(numberOfDatasets))
    return

#%%
def get_file_overview(location_BSRN_database):
    filenames = glob.glob(location_BSRN_database)
    
    # Prepare file information collecting lists
    file_station = []
    file_year = []
    file_month = []
    
    # Loop over all files
    for p in range(0, len(filenames)):
        name, month, year = extract_available_data_info(filenames[p])
        file_station.append(name)
        file_month.append(int(month))
        file_year.append(int(year))
    
    # Information about the range of the dataset
    stationsAbbrev = list(set(file_station))
    stationsAbbrev.sort()
    numberOfStations = len(stationsAbbrev)
    allYears = list(set(file_year))
    numberOfYears = len(allYears)
    allMonths = list(set(file_month))
    numberOfMonths = len(allMonths)
    numberOfDatasets = len(file_station)
    startOfStationloop = 0
    endOfStationloop = numberOfStations
    
    return file_station, file_year, file_month, stationsAbbrev, numberOfStations, \
            allYears, numberOfYears, allMonths, numberOfMonths, numberOfDatasets, \
            startOfStationloop, endOfStationloop

#%%
def main(location_BSRN_database):
    # set directory of data manually
    
    file_station, file_year, file_month, stationsAbbrev, numberOfStations, \
    allYears, numberOfYears, allMonths, numberOfMonths, numberOfDatasets, \
    startOfStationloop, endOfStationloop = get_file_overview(location_BSRN_database)
    print_file_overview(stationsAbbrev, numberOfStations, allYears, numberOfYears,\
                    allMonths, numberOfMonths, numberOfDatasets)
    return

#%%
if __name__ == "__main__":
    main(location_BSRN_database)