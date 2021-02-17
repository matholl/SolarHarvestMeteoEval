#%% Import Payern's 2015 BSRN radiation data

#%%
import csv
from datetime import datetime
import numpy as np

#%%
def get_pay_15_data(pay_path, data, ov_station_id):
    year_str = '15'
    month = ['%02d' % p for p in range(1, 13)]
    station_month = ['%d' % p for p in range(1, 13)]
    station_id = 21
    
    data[str(station_id)] = {}
    data[str(station_id)]['month'] = {}
    
    data[str(station_id)]['station_name'] = 'Payerne'
    data[str(station_id)]['surface_type'] = 'cultivated'
    data[str(station_id)]['topography_type'] = 'hilly, rural'
    data[str(station_id)]['lat'] = 46.815 # -90 is the correction from the BSRN format to the ISO-6709 format
    data[str(station_id)]['lon'] = 6.944 #> -180 is the correction from the BSRN format to the ISO-6709 format
    data[str(station_id)]['alt'] = 491
    data[str(station_id)]['ov_ind'] = ov_station_id.index(station_id)
    
    for i in range(0, len(month)):
        filename = 'pay' + month[i] + year_str
        path = pay_path + filename + '.dat'
        f = open(path)
        reader = csv.reader(f, delimiter = '\t')
        df = list(reader)
        
        data[str(station_id)]['month'][str(station_month[i])] = {}
        date_time_raw = [df[p][1] for p in range(1, len(df))]
        data[str(station_id)]['month'][str(station_month[i])]['dir'] = [float(df[p][2]) for p in range(1, len(df))]
        data[str(station_id)]['month'][str(station_month[i])]['glo'] = [float(df[p][3]) for p in range(1, len(df))]
        data[str(station_id)]['month'][str(station_month[i])]['dif'] = [float(df[p][4]) for p in range(1, len(df))]
        
        
        # date and time information
        data[str(station_id)]['month'][str(station_month[i])]['date_time'] = \
             [datetime.strptime(date_time_raw[p], '%Y-%m-%dT%H:%M') for p in range(0, len(date_time_raw))]
        
        
        # find NANs
        # glo
        data[str(station_id)]['month'][str(station_month[i])]['glo_NANs'] = \
             list(np.isnan(data[str(station_id)]['month'][str(station_month[i])]['glo'])).count(1)
             
        # dir
        data[str(station_id)]['month'][str(station_month[i])]['dir_NANs'] = \
             list(np.isnan(data[str(station_id)]['month'][str(station_month[i])]['dir'])).count(1)
        
        # dif
        data[str(station_id)]['month'][str(station_month[i])]['dif_NANs'] = \
             list(np.isnan(data[str(station_id)]['month'][str(station_month[i])]['dif'])).count(1)
        
        
    return data