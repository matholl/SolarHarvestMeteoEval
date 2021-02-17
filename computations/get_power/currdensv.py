#%% Get current density dependent on the voltage
# import libraries
import csv
import matplotlib.pyplot as plt

#%% Read data
def get_cdv(cdv_path):
    f = open(cdv_path)
    reader = csv.reader(f, delimiter = ',')
    df = list(reader)
    f.close()
        
    cd_voltage = [item[0] for item in df]
    cd_voltage_name = cd_voltage[0]
    del cd_voltage[0]
    cd_voltage = [float(cd_voltage[p]) for p in range(0,len(cd_voltage))]
    cd = [item[1] for item in df]
    cd_name = cd[0]
    del cd[0]
    cd = [float(cd[p]) for p in range(0,len(cd))]
    del df
    
    return cd_voltage, cd_voltage_name, cd, cd_name

#%% plot
def plot_cdv(cd_voltage, cd_voltage_name, cd, cd_name):
    plt.figure(figsize=(10,8))
    plt.plot(cd_voltage, cd, '*')
    plt.grid('on')
    plt.ylim([min(cd), max(cd)*1.1])
    plt.ylabel(cd_name)
    plt.xlim([min(cd_voltage), max(cd_voltage)*1.1])
    plt.xlabel(cd_voltage_name)
    plt.title('IXYS monocrystalline solar cell - current density vs voltage characteristic')

#%%
def main(cdv_path):
    cd_voltage, cd_voltage_name, cd, cd_name = get_cdv(cdv_path)
    plot_cdv(cd_voltage, cd_voltage_name, cd, cd_name)
    return

#%%
if __name__ == '__main__':
    main(cdv_path)