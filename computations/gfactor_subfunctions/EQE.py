#%% import libraries
import csv
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np

#%% Import EQE of IXYS solar cell
def import_ixys_eqe(interp_range, IXYS_EQE_path):
    f = open(IXYS_EQE_path)
    reader = csv.reader(f, delimiter = ',')
    df = list(reader)
    f.close()

    eqe = {}
    eqe['ixys'] = {}
    eqe['ixys']['wavelengths'] = [item[0] for item in df]
    del eqe['ixys']['wavelengths'][0]
    eqe['ixys']['wavelengths'] = [float(eqe['ixys']['wavelengths'][p]) for p in range(0,len(eqe['ixys']['wavelengths']))]
    eqe['ixys']['eqe'] = [item[1] for item in df]
    del eqe['ixys']['eqe'][0]
    eqe['ixys']['eqe'] = [float(eqe['ixys']['eqe'][p])/100 for p in range(0,len(eqe['ixys']['eqe']))]
    del df

     # Interpolate bashkatov
    f = interpolate.interp1d(eqe['ixys']['wavelengths'], eqe['ixys']['eqe'], kind='linear')
    eqe['ixys']['wavelengths_interp'] = interp_range
    eqe['ixys']['eqe_interp'] = f(eqe['ixys']['wavelengths_interp'])

    # Get signals from 400-2000 nm
    startindex = list(eqe['ixys']['wavelengths_interp']).index(min(interp_range))
    endindex = list(eqe['ixys']['wavelengths_interp']).index(max(interp_range))

    eqe['ixys']['wavelengths_interp'] = eqe['ixys']['wavelengths_interp'][startindex:endindex+1]
    eqe['ixys']['eqe_interp'] = eqe['ixys']['eqe_interp'][startindex:endindex+1]

    return eqe

#%%
# Import EQE of EMPA's CIGS solar cell
def import_empa_eqe(eqe, interp_range, EMPA_EQE_path):
    f = open(EMPA_EQE_path)
    reader = csv.reader(f, delimiter = ';')
    df = list(reader)
    f.close()

    eqe['empa'] = {}
    eqe['empa']['wavelengths'] = [item[0] for item in df]
    del eqe['empa']['wavelengths'][0]
    del eqe['empa']['wavelengths'][0]
    eqe['empa']['wavelengths'] = [float(eqe['empa']['wavelengths'][p]) for p in range(0,len(eqe['empa']['wavelengths']))]
    eqe['empa']['eqe'] = [item[1] for item in df]
    del eqe['empa']['eqe'][0]
    del eqe['empa']['eqe'][0]
    eqe['empa']['eqe'] = [float(eqe['empa']['eqe'][p]) for p in range(0,len(eqe['empa']['eqe']))]
    del df

    # Interpolate bashkatov
    f = interpolate.interp1d(eqe['empa']['wavelengths'], eqe['empa']['eqe'], kind='linear')
    eqe['empa']['wavelengths_interp'] = interp_range
    eqe['empa']['eqe_interp'] = f(eqe['empa']['wavelengths_interp'])

    # Get signals from interp_range
    startindex = list(eqe['empa']['wavelengths_interp']).index(min(interp_range))
    endindex = list(eqe['empa']['wavelengths_interp']).index(max(interp_range))

    eqe['empa']['wavelengths_interp'] = eqe['empa']['wavelengths_interp'][startindex:endindex+1]
    eqe['empa']['eqe_interp'] = eqe['empa']['eqe_interp'][startindex:endindex+1]

    return eqe

#%%
def interpol_plot_ixys(eqe, interp_range):
    plt.figure(figsize=(10,8))
    plt.plot(eqe['ixys']['wavelengths'], eqe['ixys']['eqe'], '-x', eqe['ixys']['wavelengths_interp'], eqe['ixys']['eqe_interp'], 'o', markersize = 4)
    plt.legend(['direct values', 'interpolation'])
    plt.xlabel(r'$\lambda$ [nm]')
    plt.xlim([min(interp_range), max(interp_range)])
    plt.xticks(np.arange(min(interp_range), max(interp_range)+1, 100), rotation=45)
    plt.ylim([0, 1])
    plt.yticks(np.arange(0, 1+.000001, .1))
    plt.ylabel('EQE []')
    plt.grid('on')
    plt.title('IXYS monocrystalline solar cell')
    return

#%%
def interpol_plot_empa(eqe, interp_range):
    plt.figure(figsize=(10,8))
    plt.plot(eqe['empa']['wavelengths'], eqe['empa']['eqe'], '-x', eqe['empa']['wavelengths_interp'], eqe['empa']['eqe_interp'], 'o', markersize = 4)
    plt.legend(['direct values', 'interpolation'])
    plt.xlabel(r'$\lambda$ [nm]')
    plt.xlim([min(interp_range), max(interp_range)])
    plt.xticks(np.arange(min(interp_range), max(interp_range)+1, 100), rotation=45)
    plt.ylim([0, 1])
    plt.yticks(np.arange(0, 1+.000001, .1))
    plt.ylabel('EQE []')
    plt.grid('on')
    plt.title('EMPA CIGS solar cell')
    return

#%%
def get_eqe(interp_range, IXYS_EQE_path, EMPA_EQE_path):
    print('Loading EQE')
    eqe = import_ixys_eqe(interp_range, IXYS_EQE_path)
    eqe = import_empa_eqe(eqe, interp_range, EMPA_EQE_path)
    return eqe

#%%
def main(interp_range, IXYS_EQE_path, EMPA_EQE_path):
    eqe = get_eqe(interp_range, IXYS_EQE_path, EMPA_EQE_path)
    interpol_plot_ixys(eqe, interp_range)
    interpol_plot_empa(eqe, interp_range)
    return

#%%
if __name__ == '__main__':
    main(interp_range, IXYS_EQE_path, EMPA_EQE_path)
