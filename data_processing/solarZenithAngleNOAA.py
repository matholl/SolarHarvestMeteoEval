#%%
import numpy as np
import datetime

#%% Compute the solar zenith angle
def getSolarZenithAngle(data, station_ids, i, months, j):
    #%% Get the UTC time difference in hours
    timezone = data[str(station_ids[i])]['UTC_diff_h']
    
    #%% Get the local time
    localtime = [data[station_ids[i]]['month'][months[j]]['date_time'][p] + datetime.timedelta(hours = timezone) \
                 for p in range(0, len(data[station_ids[i]]['month'][months[j]]['date_time']))]
        
    #%% Get the day of the year and others
    DoY = [ localtime[p].timetuple().tm_yday for p in range(0, len(localtime))]
    hour = [localtime[p].hour for p in range(0, len(localtime))]
    minute = [localtime[p].minute for p in range(0, len(localtime))]
    second = [localtime[p].second for p in range(0, len(localtime))]
    
    # Get the fractional year
    gamma = [(2 * np.pi / 365) * (DoY[p] - 1 + ((hour[p] -12) / 24)) \
             for p in range(0, len(DoY))]
    
    # Get declination
    decl = [0.006918 - 0.399912 * np.cos(gamma[p]) + 0.070257 * np.sin(gamma[p]) \
            - 0.006758 * np.cos(2 * gamma[p]) + 0.000907 * np.sin(2 * gamma[p]) \
            - 0.002697 * np.cos(3 * gamma[p]) + 0.00148 * np.sin(3 * gamma[p]) \
            for p in range(0, len(gamma))]
    
    # Equation of time
    eqtime = [229.18 * (0.000075 + 0.001868 * np.cos(gamma[p]) - 0.032077 * \
            np.sin(gamma[p]) - 0.014615 * np.cos(2 * gamma[p]) - \
            0.040849 * np.sin(2 * gamma[p])) for p in range(0, len(gamma))]
    
    # Get time offset
    time_offset = [eqtime[p] + 4 * data[station_ids[i]]['lon'] \
                   - 60 * timezone for p in range(0, len(eqtime))]
    
    # ??
    tst = [hour[p] * 60 + minute[p] + second[p] / 60 + time_offset[p] for p in range(0,len(hour))]
    
    # Get the solar hour angle
    ha = [(tst[p] / 4) - 180 for p in range(0,len(tst))]
    
    # Degrees to rad
    deg_to_rad = 2 * np.pi / 360
    
    #%% Get the solar zenith angle
    sza = [np.arccos(np.sin(data[station_ids[i]]['lat']*deg_to_rad) \
            * np.sin(decl[p]) + np.cos(data[station_ids[i]]['lat']*deg_to_rad) \
            * np.cos(decl[p]) * np.cos(ha[p]*deg_to_rad)) for p in range(0,len(decl))]
    
    # Get the solar azimuth
    saz = [(np.arccos(-(np.sin(data[station_ids[i]]['lat']*deg_to_rad)\
            * np.cos(sza[p]) - np.sin(decl[p]))/(np.cos(data[station_ids[i]]['lat']*deg_to_rad) \
            * np.sin(sza[p]))) * (-1) - 180) * deg_to_rad for p in range(0,len(sza))] 
    
    #%% Get air mass
    am = []
    for q in range(0, len(sza)):
        if sza[q] > np.pi/2:
            am.append(1/np.cos(1/(np.pi/2)))
        else:
            am.append(1/np.cos(sza[q]))
    
    #%% Critical solar zenith angle sza at sunrise or sunset
    cr_sza = 90 * deg_to_rad
    
    # Find indices of sza where cr_sza is crossed
    sunriseIndices = []
    sunsetIndices = []
    for q in range(0, len(sza)-1):
        if sza[q] <= cr_sza:
            if sza[q+1] >= cr_sza:
                sunsetIndices.append(q)
        elif sza[q] >= cr_sza:
            if sza[q+1]<= cr_sza:
                sunriseIndices.append(q)
    
    sunrise_datetime = [data[station_ids[i]]['month'][months[j]]['date_time'][sunriseIndices[p]] for p in range(0, len(sunriseIndices))]
    sunset_datetime = [data[station_ids[i]]['month'][months[j]]['date_time'][sunsetIndices[p]] for p in range(0, len(sunsetIndices))]
    
    #%%
    return sza, saz, localtime, am, sunrise_datetime, sunset_datetime