import pytz, datetime
#%%

def get_timezone(data, station_ids, i, ov_station_tz_name, ov_station_utcdiffh,\
                 ov_station_utcdiffmin, ov_station_dstyn, ov_station_dststart,\
                 ov_station_dstend, ov_station_dstdiff, ov_station_id, ov_station_name):

    current_station_ov_id = ov_station_id.index(int(station_ids[i]))

    timezone = float(ov_station_utcdiffh[current_station_ov_id]) + float(ov_station_utcdiffmin[current_station_ov_id])/60
    tz = ov_station_tz_name[current_station_ov_id]

    print('Current station: ' + str(ov_station_name[current_station_ov_id]))
    print('Current UTC OFFSET: ' + str(timezone))
    print('Current timezone: ' + tz)

    return timezone, tz


# Find correct time zone and UTC time differnece in hours
# Get the station's time zone and the UTC offset
def get_timezone_old(data, station_ids, i):

    tz = TimezoneFinder().timezone_at(lng=data[str(station_ids[i])]['lon'], lat=data[str(station_ids[i])]['lat'])

    if type(tz) != str:
        deltadegree = 1
        while(type(tz) != str or tz == 'uninhabited'):
            tz = TimezoneFinder().closest_timezone_at(lng=data[str(station_ids[i])]['lon'], lat=data[str(station_ids[i])]['lat'], delta_degree=deltadegree)
            deltadegree += 1

    UTC_diff =  datetime.datetime.now(pytz.timezone(tz)).strftime('%z')

    if  UTC_diff[0] == '+':
        timezone = float(UTC_diff[1:3]) + float(UTC_diff[3:5])/60
    elif UTC_diff[0] == '-':
        timezone = (-1) * float(UTC_diff[1:3]) + float(UTC_diff[3:5])/60
    else:
        print('ATTENTION: timezone detection failed at solarZenithAngleNOAA.py')

    return timezone, tz
