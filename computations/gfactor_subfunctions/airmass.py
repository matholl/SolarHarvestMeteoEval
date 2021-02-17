#%%
# Import libraries
import csv
from scipy import interpolate
import numpy as np

#%%
def definitions():

    path = './data_import/data/airmassdata/'
    am_names = ['AM_1','AM_1_5', 'AM_2', 'AM_4', 'AM_6', 'AM_8', 'AM_10', 'AM_12']
    air_masses = [1, 1.5, 2, 4, 6, 8, 10, 12]
    file_name_beginning = 'smarts295_'
    location = 'Payerne'
    filename_extension = '.ext.txt'

    return path, am_names, file_name_beginning, location, filename_extension, air_masses

#%%
def define_dicts(am_names):
    am = {}
    for i in range(0, len(am_names)):
        am[am_names[i]] = {}
        am[am_names[i]]['wavelength'] = {}
        am[am_names[i]]['extraterrestrial_spectrm'] = {}
        am[am_names[i]]['direct_normal_irradiance'] = {}
        am[am_names[i]]['difuse_horizn_irradiance'] = {}
        am[am_names[i]]['global_horizn_irradiance'] = {}
        am[am_names[i]]['direct_horizn_irradiance'] = {}
        am[am_names[i]]['direct_tilted_irradiance'] = {}
        am[am_names[i]]['difuse_tilted_irradiance'] = {}
        am[am_names[i]]['global_tilted_irradiance'] = {}
        am[am_names[i]]['global_tilt_photon_irrad'] = {}
        am[am_names[i]]['beam_normal_photon_irrad'] = {}
        am[am_names[i]]['difuse_horiz_photn_irrad'] = {}
        am[am_names[i]]['global_horizn_photon_flux'] = {}
        am[am_names[i]]['dirct_normal_photon_flux'] = {}
        am[am_names[i]]['dif_horizntl_photon_flux'] = {}
        am[am_names[i]]['global_tiltd_photon_flux'] = {}

    return am

#%%
def read_file(path, am_names, i, file_name_beginning, location, filename_extension):
    file_path = ''.join([path, am_names[i], '/', file_name_beginning, location, '_', am_names[i], filename_extension])
    f = open(file_path)
    reader = csv.reader(f, delimiter = ' ')
    df = list(reader)
    f.close()

    # extend lists
    wavelength = [float(df[p][0]) for p in range(1,len(df))]
    extraterrestrial_spectrm = [float(df[p][1]) for p in range(1,len(df))]
    direct_normal_irradiance = [float(df[p][2]) for p in range(1,len(df))]
    difuse_horizn_irradiance = [float(df[p][3]) for p in range(1,len(df))]
    global_horizn_irradiance = [float(df[p][4]) for p in range(1,len(df))]
    direct_horizn_irradiance = [float(df[p][5]) for p in range(1,len(df))]
    direct_tilted_irradiance = [float(df[p][6]) for p in range(1,len(df))]
    difuse_tilted_irradiance = [float(df[p][7]) for p in range(1,len(df))]
    global_tilted_irradiance = [float(df[p][8]) for p in range(1,len(df))]
    global_tilt_photon_irrad = [float(df[p][9]) for p in range(1,len(df))]
    beam_normal_photon_irrad = [float(df[p][10]) for p in range(1,len(df))]
    difuse_horiz_photn_irrad = [float(df[p][11]) for p in range(1,len(df))]
    global_horizn_photon_flux = [float(df[p][12]) for p in range(1,len(df))]
    direct_normal_photon_flux = [float(df[p][13]) for p in range(1,len(df))]
    dif_horizntl_photon_flux = [float(df[p][14]) for p in range(1,len(df))]
    global_tiltd_photon_flux = [float(df[p][15]) for p in range(1,len(df))]

    return  wavelength, extraterrestrial_spectrm, direct_normal_irradiance, \
            difuse_horizn_irradiance, global_horizn_irradiance, \
            direct_horizn_irradiance, direct_tilted_irradiance, \
            difuse_tilted_irradiance, global_tilted_irradiance, \
            global_tilt_photon_irrad, beam_normal_photon_irrad, \
            difuse_horiz_photn_irrad, global_horizn_photon_flux, \
            direct_normal_photon_flux, dif_horizntl_photon_flux, \
            global_tiltd_photon_flux

    # return  wavelength, global_horizn_irradiance, \
    #         global_horizn_photon_flux

#%%
def interpolate_am(am, am_names, i, interp_range):
    # Interpolate am
    am[am_names[i]]['wavelength_interp'] = interp_range

    f = interpolate.interp1d(am[am_names[i]]['wavelength'], am[am_names[i]]['extraterrestrial_spectrm'], kind='linear')
    am[am_names[i]]['extraterrestrial_spectrm_interp'] = f(am[am_names[i]]['wavelength_interp'])

    f = interpolate.interp1d(am[am_names[i]]['wavelength'], am[am_names[i]]['direct_normal_irradiance'], kind='linear')
    am[am_names[i]]['direct_normal_irradiance_interp'] = f(am[am_names[i]]['wavelength_interp'])

    f = interpolate.interp1d(am[am_names[i]]['wavelength'], am[am_names[i]]['difuse_horizn_irradiance'], kind='linear')
    am[am_names[i]]['difuse_horizn_irradiance_interp'] = f(am[am_names[i]]['wavelength_interp'])

    f = interpolate.interp1d(am[am_names[i]]['wavelength'], am[am_names[i]]['global_horizn_irradiance'], kind='linear')
    am[am_names[i]]['global_horizn_irradiance_interp'] = f(am[am_names[i]]['wavelength_interp'])

    f = interpolate.interp1d(am[am_names[i]]['wavelength'], am[am_names[i]]['direct_horizn_irradiance'], kind='linear')
    am[am_names[i]]['direct_horizn_irradiance_interp'] = f(am[am_names[i]]['wavelength_interp'])

    f = interpolate.interp1d(am[am_names[i]]['wavelength'], am[am_names[i]]['direct_tilted_irradiance'], kind='linear')
    am[am_names[i]]['direct_tilted_irradiance_interp'] = f(am[am_names[i]]['wavelength_interp'])

    f = interpolate.interp1d(am[am_names[i]]['wavelength'], am[am_names[i]]['difuse_tilted_irradiance'], kind='linear')
    am[am_names[i]]['difuse_tilted_irradiance_interp'] = f(am[am_names[i]]['wavelength_interp'])

    f = interpolate.interp1d(am[am_names[i]]['wavelength'], am[am_names[i]]['global_tilted_irradiance'], kind='linear')
    am[am_names[i]]['global_tilted_irradiance_interp'] = f(am[am_names[i]]['wavelength_interp'])

    f = interpolate.interp1d(am[am_names[i]]['wavelength'], am[am_names[i]]['global_tilt_photon_irrad'], kind='linear')
    am[am_names[i]]['global_tilt_photon_irrad_interp'] = f(am[am_names[i]]['wavelength_interp'])

    f = interpolate.interp1d(am[am_names[i]]['wavelength'], am[am_names[i]]['beam_normal_photon_irrad'], kind='linear')
    am[am_names[i]]['beam_normal_photon_irrad_interp'] = f(am[am_names[i]]['wavelength_interp'])

    f = interpolate.interp1d(am[am_names[i]]['wavelength'], am[am_names[i]]['difuse_horiz_photn_irrad'], kind='linear')
    am[am_names[i]]['difuse_horiz_photn_irrad_interp'] = f(am[am_names[i]]['wavelength_interp'])

    f = interpolate.interp1d(am[am_names[i]]['wavelength'], am[am_names[i]]['global_horizn_photon_flux'], kind='linear')
    am[am_names[i]]['global_horizn_photon_flux_interp'] = f(am[am_names[i]]['wavelength_interp'])

    f = interpolate.interp1d(am[am_names[i]]['wavelength'], am[am_names[i]]['direct_normal_photon_flux'], kind='linear')
    am[am_names[i]]['direct_normal_photon_flux_interp'] = f(am[am_names[i]]['wavelength_interp'])

    f = interpolate.interp1d(am[am_names[i]]['wavelength'], am[am_names[i]]['dif_horizntl_photon_flux'], kind='linear')
    am[am_names[i]]['dif_horizntl_photon_flux_interp'] = f(am[am_names[i]]['wavelength_interp'])

    f = interpolate.interp1d(am[am_names[i]]['wavelength'], am[am_names[i]]['global_tiltd_photon_flux'], kind='linear')
    am[am_names[i]]['global_tiltd_photon_flux_interp'] = f(am[am_names[i]]['wavelength_interp'])

    return am

#%%
def integrate_given_spectra(am, am_names, i):
    am[am_names[i]]['global_horizn_irradiance_integral'] = \
      np.trapz(am[am_names[i]]['global_horizn_irradiance'], am[am_names[i]]['wavelength'])
    am[am_names[i]]['global_horizn_irradiance_interp_integral'] = \
      np.trapz(am[am_names[i]]['global_horizn_irradiance_interp'], am[am_names[i]]['wavelength_interp'])
    am[am_names[i]]['global_horizn_photon_flux_integral'] = \
      np.trapz(am[am_names[i]]['global_horizn_photon_flux'], am[am_names[i]]['wavelength'])
    am[am_names[i]]['global_horizn_photon_flux_interp_integral'] = \
      np.trapz(am[am_names[i]]['global_horizn_photon_flux_interp'], am[am_names[i]]['wavelength_interp'])
    return am

#%%
def get_am(interp_range):
    print('Loading airmass data')
    path, am_names, file_name_beginning, location, filename_extension, air_masses = \
        definitions()

    am = define_dicts(am_names)

    # read data
    for i in range(0, len(am_names)):
        am[am_names[i]]['wavelength'], am[am_names[i]]['extraterrestrial_spectrm'], am[am_names[i]]['direct_normal_irradiance'], \
        am[am_names[i]]['difuse_horizn_irradiance'], am[am_names[i]]['global_horizn_irradiance'], am[am_names[i]]['direct_horizn_irradiance'], \
        am[am_names[i]]['direct_tilted_irradiance'], am[am_names[i]]['difuse_tilted_irradiance'], am[am_names[i]]['global_tilted_irradiance'], \
        am[am_names[i]]['global_tilt_photon_irrad'], am[am_names[i]]['beam_normal_photon_irrad'], am[am_names[i]]['difuse_horiz_photn_irrad'], \
        am[am_names[i]]['global_horizn_photon_flux'], am[am_names[i]]['direct_normal_photon_flux'], am[am_names[i]]['dif_horizntl_photon_flux'], \
        am[am_names[i]]['global_tiltd_photon_flux'] = \
                read_file(path, am_names, i, file_name_beginning, location, filename_extension)

        am = interpolate_am(am, am_names, i, interp_range)
        am = integrate_given_spectra(am, am_names, i)

    return am, am_names, air_masses

#%%
def main(interp_range):
    am, am_names, air_masses = get_am(interp_range)

    return am, am_names

#%%
if __name__ == '__main__':
    am, am_names = main(interp_range)
