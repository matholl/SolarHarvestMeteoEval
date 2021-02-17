#%%
from bisect import bisect
import numpy as np
import os

if os.getcwd() == 'D:\\GoogleDrive\\0_PhD_ARTORG\\6_RadiationSW\\0_DataEvalCode\\Pyhton\\RadiationStudy_0\\computations':
    from get_power import get_closest_am
else:
    from computations.get_power import get_closest_am

#%% get subcutaneous irradiation using the general factors
def subcutaneous_irradiation(data, station_ids, am, am_names, months, i, j):
    data[station_ids[i]]['month'][months[j]]['subcutaneous'] = {}
    data[station_ids[i]]['month'][months[j]]['subcutaneous']['glo'] = []
    for p in range(0, len(data[station_ids[i]]['month'][months[j]]['glo'])):
        data[station_ids[i]]['month'][months[j]]['subcutaneous']['glo'].append(\
            data[station_ids[i]]['month'][months[j]]['glo'][p] * \
            am[am_names[data[station_ids[i]]['month'][months[j]]['ind_am_names'][p]]]['general_factor']['irradiance']['global_horizn'])
    return  data

#%% get ocvoltage from irradiation
def get_closest_ocv(ocv_irrad, ocv, data, station_ids, am, am_names, months, i, j):
    data[station_ids[i]]['month'][months[j]]['ocv'] = {}

    index1 = []
    for p in range(0, len(data[station_ids[i]]['month'][months[j]]['subcutaneous']['glo'])):
        ind1 = bisect(ocv_irrad, data[station_ids[i]]['month'][months[j]]['subcutaneous']['glo'][p])

        if ind1 == 0:
            index1.append(ind1)

        elif data[station_ids[i]]['month'][months[j]]['subcutaneous']['glo'][p] < 2:
            index1.append(0)

        elif ind1 == len(ocv_irrad):
            index1.append(ind1-1)

        elif abs(ocv_irrad[ind1] - data[station_ids[i]]['month'][months[j]]['subcutaneous']['glo'][p]) < \
           abs(ocv_irrad[ind1-1] - data[station_ids[i]]['month'][months[j]]['subcutaneous']['glo'][p]):
            index1.append(ind1)

        else:
            index1.append(ind1-1)

    data[station_ids[i]]['month'][months[j]]['ocv'] = [ocv[index1[p]] for p in range(0, len(index1))]
    return data

#%% calculate Isc
def get_isc(data, station_ids, am, am_names, months, i, j, eqe, user_name):
    q = 1.6021766208*1e-19

    data[station_ids[i]]['month'][months[j]]['isc'] = {}
    data[station_ids[i]]['month'][months[j]]['subcutaneous']['photon_flux_interp'] = {}
    for m in range(0, len(user_name)):
        data[station_ids[i]]['month'][months[j]]['subcutaneous']['photon_flux_interp'][str(m)] = []
        data[station_ids[i]]['month'][months[j]]['isc'][str(m)] = []
        for p in range(0, len(data[station_ids[i]]['month'][months[j]]['outside_time_glo_filled'][m])):
            data[station_ids[i]]['month'][months[j]]['subcutaneous']['photon_flux_interp'][str(m)].append( \
                [(data[station_ids[i]]['month'][months[j]]['outside_time_glo_filled'][m][p] / \
                am[am_names[data[station_ids[i]]['month'][months[j]]['ind_am_names'][p]]]['global_horizn_irradiance_interp_integral']) * \
                am[am_names[data[station_ids[i]]['month'][months[j]]['ind_am_names'][p]]]['photonflux']['subcutaneous']['global_horizn_interp'][n] \
                for n in range(0, len(am[am_names[data[station_ids[i]]['month'][months[j]]['ind_am_names'][p]]]['photonflux']['subcutaneous']['global_horizn_interp']))])

    for m in range(0, len(user_name)):
        for p in range(0, len(data[station_ids[i]]['month'][months[j]]['subcutaneous']['photon_flux_interp'][str(m)])):
            data[station_ids[i]]['month'][months[j]]['isc'][str(m)].extend( \
                [q * np.trapz([data[station_ids[i]]['month'][months[j]]['subcutaneous']['photon_flux_interp'][str(m)][p][n]\
                * eqe['ixys']['eqe_interp'][n] for n in range(0, len(eqe['ixys']['eqe_interp']))] , \
                [eqe['ixys']['wavelengths_interp'][n]for n in range(0, len(eqe['ixys']['wavelengths_interp']))])])

    del data[station_ids[i]]['month'][months[j]]['subcutaneous']['photon_flux_interp']
    return data

#%% calculate power output (80% ocvoltage * isc * cell_area)
def calculate_power(data, station_ids, months, cell_area_m2, i, j, user_name):
    data[station_ids[i]]['month'][months[j]]['p_calc'] = {}
    for m in range(0, len(user_name)):
        data[station_ids[i]]['month'][months[j]]['p_calc'][str(m)] = \
                [.8 * data[station_ids[i]]['month'][months[j]]['ocv'][p] * \
                float(data[station_ids[i]]['month'][months[j]]['isc'][str(m)][p]) * cell_area_m2 \
                for p in range(0, len(data[station_ids[i]]['month'][months[j]]['isc'][str(m)]))]

    return data

#%% calculate power output (including all subfunctions)
def get_power(data, station_ids, am, am_names, months, i, j, air_masses, eqe, ocv_irrad, ocv, cell_area_m2, user_name):
    data = get_closest_am.get_am(data, station_ids, am, am_names, months, i, j, air_masses)
    data = subcutaneous_irradiation(data, station_ids, am, am_names, months, i, j)
    data = get_closest_ocv(ocv_irrad, ocv, data, station_ids, am, am_names, months, i, j)
    data = get_isc(data, station_ids, am, am_names, months, i, j, eqe, user_name)
    data = calculate_power(data, station_ids, months, i, j, cell_area_m2)
    return data

#%%
def main(data, station_ids, am, am_names, months, i, j, air_masses, ocv_irrad, ocv, eqe, cell_area_m2):
    for i in range(0, len(station_ids)):
        months = list(data[station_ids[i]]['month'].keys())

        for j in range(0, len(months)):
            data = get_power(data, station_ids, am, am_names, months, i, j, air_masses, eqe, ocv_irrad, ocv, cell_area_m2)
    return data

#%%
if __name__ == '__main__':
    data = main(data, station_ids, am, am_names, months, i, j, air_masses, ocv_irrad, ocv, eqe, cell_area_m2)
