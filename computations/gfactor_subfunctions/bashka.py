#%%
# Import libraries
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from itertools import repeat

#%%
def get_bashkatov(interp_range):
    print('Loading skin\'s transmission factor')
    bashkatov = {}

    path = './data_import/data/PenetrationDepth_Bashkatov.csv'
    f = open(path)
    reader = csv.reader(f, delimiter = ',')
    df = list(reader)
    f.close()

    # lambda
    bashkatov['wavelengths'] = [item[0] for item in df]
    del bashkatov['wavelengths'][0]
    bashkatov['wavelengths'] = [float(bashkatov['wavelengths'][p]) for p in range(0,len(bashkatov['wavelengths']))]

    # penetration depth
    bashkatov['pen_depth'] = [item[1] for item in df]
    del bashkatov['pen_depth'][0]
    bashkatov['pen_depth'] = [float(bashkatov['pen_depth'][p]) for p in range(0,len(bashkatov['pen_depth']))]

    del df

    bashkatov['skin_thickness'] = 2.5

    bashkatov['tf'] = []
    for i in range(0, len(bashkatov['pen_depth'])):
        if bashkatov['pen_depth'][i] == 0:
            bashkatov['tf'].append(0)
        else:
            bashkatov['tf'].append(np.exp(-(bashkatov['skin_thickness']/bashkatov['pen_depth'][i]))) # skin thickness and penetration depth are both in mm

    # Interpolate bashkatov
    f = interpolate.interp1d(bashkatov['wavelengths'], bashkatov['tf'], kind='linear')
    bashkatov['wavelength_interp'] = interp_range
    bashkatov['tf_interp'] = f(bashkatov['wavelength_interp'])

    return bashkatov

#%%
def plot_bashkatov_interp(bashkatov, interp_range):
    plt.figure(figsize=(10,8))
    plt.plot(bashkatov['wavelengths'], bashkatov['tf'], '-x', bashkatov['wavelength_interp'], bashkatov['tf_interp'], 'o', markersize = 4)
    plt.legend(['direct values', 'interpolation'])
    plt.xlabel(r'$\lambda$ [nm]')
    plt.xlim([min(interp_range),max(interp_range)])
    plt.ylabel('transmission coefficient')
    plt.ylim([0, max(bashkatov['tf_interp'])*1.2])
    plt.grid('on')
    plt.title('Bashkatov transmission coefficient data interpolation')
    return

#%%
def plot_bashkatov_skinthickness(bashkatov, interp_range):
    # plot the transmission coefficient dependent on wavelength for the chosen skin thickness
    plt.figure(figsize=(10,8))
    plt.title('Transmission coefficient calculated based on Bashkatov et al 2005 (skin-thickness = ' + str(bashkatov['skin_thickness']) + 'mm)')
    plt.plot(bashkatov['wavelengths'], bashkatov['tf'])
    plt.xlabel(r'$\lambda$ [nm]')
    plt.ylabel('transmission coefficient')
    plt.xlim([min(interp_range),max(interp_range)])
    plt.ylim([0, max(bashkatov['tf'])*1.2])
    plt.grid('on')
    return

#%%
def plot_bashkatov_3d(bashkatov):
    # Plot the transmission coefficient dependent on wavelength and skin thickness
    skin_thickness = np.linspace(0.5, 5, len(bashkatov['wavelengths']))

    plot_transmission_coeff = []
    for i in range(0, len(skin_thickness)):
        for j in range(0, len(bashkatov['pen_depth'])):
            plot_transmission_coeff.append(np.exp(-(skin_thickness[i]/bashkatov['pen_depth'][j]))) # skin thickness and penetration depth are both in mm

    plot_skin_thickness = [x for item in skin_thickness for x in repeat(item, len(skin_thickness))]
    plot_wavelengths = bashkatov['wavelengths'] * len(bashkatov['wavelengths'])

    fig = plt.figure(figsize=(15,7.5))
    ax = fig.gca(projection='3d')
    p = ax.plot_trisurf(np.array(plot_wavelengths), np.array(plot_skin_thickness), np.array(plot_transmission_coeff), cmap='RdYlGn', vmin=0, vmax=1)
    cbar = fig.colorbar(p, shrink = 0.6)
    p.set_facecolor('white')
    cbar.set_label('transmission coefficient', rotation=90)
    ax.set_xlabel(r'$\lambda$ [nm]')
    ax.set_ylabel('skin thickness [mm]')
    ax.set_zlabel('transmission coefficient')
    plt.title('Transmission coefficient calculated based on Bashkatov et al 2005', fontsize = 14, y = 1.02)
    plt.tight_layout()
    fname2PDF =''.join(['D:/GoogleDrive/0_PhD_ARTORG/3_Data/SkinProperties/OpticalTissueBashkatov/TransCoeff_Bashkatov.pdf'])
    plt.savefig(fname2PDF, dpi = 600)
    return

#%%
def main(interp_range):
    bashkatov = get_bashkatov(interp_range)
    plot_bashkatov_interp(bashkatov, interp_range)
    plot_bashkatov_skinthickness(bashkatov, interp_range)
#    plot_bashkatov_3d(bashkatov)
    return

#%%
if __name__ == '__main__':
    main(interp_range)
