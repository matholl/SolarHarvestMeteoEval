#%% Get open circuit voltage dependent on the irradiance
# import libraries
import csv
import matplotlib.pyplot as plt

#%% Read data
def get_ocv(ocv_path):
    f = open(ocv_path)
    reader = csv.reader(f, delimiter = ',')
    df = list(reader)
    f.close()
        
    ocv_irrad = [item[0] for item in df]
    ocv_irrad = [float(ocv_irrad[p]) for p in range(0,len(ocv_irrad))]
    ocv = [item[1] for item in df]
    ocv = [float(ocv[p]) for p in range(0,len(ocv))]
    del df
    
    return ocv_irrad, ocv

#%% plot
def plot_ocv(ocv_irrad, ocv):
    plt.figure(figsize=(10,8))
    plt.plot(ocv_irrad, ocv, '*')
    plt.grid('on')
    plt.ylim([0.4, 0.65])
    plt.ylabel('Open Circuit Voltage Voc [V]')
    plt.xlim([0, 1000])
    plt.xlabel('Irradiance E ($W/m^2$)')
    plt.title('IXYS monocrystalline solar cell - open circuit voltage vs irradiance characteristic')

#%%
def main(ocv_path):
    ocv_irrad, ocv = get_ocv(ocv_path)
    plot_ocv(ocv_irrad, ocv)
    return

#%%
if __name__ == '__main__':
    main(ocv_path)