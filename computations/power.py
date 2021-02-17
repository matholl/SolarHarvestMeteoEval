#%% import libraries
import os

#%% Manual input
plots = 0

#%% import modules
if os.getcwd() == 'D:\\GoogleDrive\\0_PhD_ARTORG\\6_RadiationSW\\0_DataEvalCode\\Pyhton\\RadiationStudy_0\\computations':
    from get_power import get_closest_am
    from get_power import currdensv
    from get_power import ocvoltage
    from get_power import power_output
else:
    from computations.get_power import get_closest_am
    from computations.get_power import currdensv
    from computations.get_power import ocvoltage
    from computations.get_power import power_output

#%%
def calculate_power_output(am, am_names, data, station_ids, months, air_masses, eqe, cell_area_m2, user_name):
    #cdv
    cd_voltage, cd_voltage_name, cd, cd_name = currdensv.get_cdv()
    if plots == 1:
        currdensv.plot_cdv(cd_voltage, cd_voltage_name, cd, cd_name)
    
    #ocv
    ocv_irrad, ocv = ocvoltage.get_ocv()
    if plots == 1:
        ocvoltage.plot_ocv(ocv_irrad, ocv)
    
    #power
    for i in range(0, len(station_ids)):
        months = list(data[station_ids[i]]['month'].keys())
        for j in range(0, len(months)):
            data = get_closest_am.get_am(data, station_ids, am, am_names, months, i, j, air_masses)
            data = power_output.subcutaneous_irradiation(data, station_ids, am, am_names, months, i, j)
            data = power_output.get_closest_ocv(ocv_irrad, ocv, data, station_ids, am, am_names, months, i, j)
            data = power_output.get_isc(data, station_ids, am, am_names, months, i, j, eqe, user_name)
            data = power_output.calculate_power(data, station_ids, months, cell_area_m2, i, j, user_name)
            
    return data

#%%
def main(am, am_names, data, station_ids, months, air_masses, eqe, cell_area_m2):
    data = calculate_power_output(am, am_names, data, station_ids, months, air_masses, eqe, cell_area_m2)
    return data
#%%
if __name__ == '__main__':
    data = main(am, am_names, data, station_ids, months, air_masses, eqe, cell_area_m2, user_name)