#%%
import matplotlib.pyplot as plt
import numpy as np

#%% get wavelength specific photon energy
def get_photon_energy(am, am_names):
    # define some constants
    h = 6.626 * 1e-34       # planck's constant in Joule*s
    c = 2.998 * 1e8         # speed of light in m/s
    nm_2_m = 1e-09          # nm to m conversion
    
    # calculate the wavelength specific photon energy in J and eV
    photon_energy = [(h * c)/(am[am_names[0]]['wavelength'][p] * nm_2_m) \
                     for p in range(0, len(am[am_names[0]]['wavelength']))]
    photon_energy_interp = [(h * c)/(am[am_names[0]]['wavelength_interp'][p] * nm_2_m) \
                     for p in range(0, len(am[am_names[0]]['wavelength_interp']))]
    
    return photon_energy, photon_energy_interp

#%%
def get_photonflux(am, am_names, bashkatov, photon_energy_interp):
    for i in range(0, len(am_names)):
        
        # define data collection dicts
        am[am_names[i]]['photonflux'] = {}
        am[am_names[i]]['photonflux']['subcutaneous'] = {}
        am[am_names[i]]['photonflux']['subcutaneous']['global_horizn_interp'] = {}
        am[am_names[i]]['photonflux']['subcutaneous']['direct_horizn_interp'] = {}
        am[am_names[i]]['photonflux']['subcutaneous']['dif_horizntl_interp'] = {}
        am[am_names[i]]['photonflux']['subcutaneous']['global_tiltd_interp'] = {}
        
        # calculate photon fluxes
        am[am_names[i]]['photonflux']['subcutaneous']['global_horizn_interp'] = \
                  [am[am_names[i]]['global_horizn_irradiance_interp'][p] * bashkatov['tf_interp'][p] / photon_energy_interp[p] \
                   for p in range(0, len(am[am_names[i]]['global_horizn_irradiance_interp']))]
        am[am_names[i]]['photonflux']['subcutaneous']['direct_horizn_interp'] = \
                  [am[am_names[i]]['direct_horizn_irradiance_interp'][p] * bashkatov['tf_interp'][p] / photon_energy_interp[p] \
                   for p in range(0, len(am[am_names[i]]['direct_horizn_irradiance_interp']))]
        am[am_names[i]]['photonflux']['subcutaneous']['dif_horizntl_interp'] = \
                  [am[am_names[i]]['difuse_horizn_irradiance_interp'][p] * bashkatov['tf_interp'][p] / photon_energy_interp[p] \
                   for p in range(0, len(am[am_names[i]]['difuse_horizn_irradiance_interp']))]
        am[am_names[i]]['photonflux']['subcutaneous']['global_tiltd_interp'] = \
                  [am[am_names[i]]['global_tilted_irradiance_interp'][p] * bashkatov['tf_interp'][p] / photon_energy_interp[p] \
                   for p in range(0, len(am[am_names[i]]['global_tilted_irradiance_interp']))]
        
    return am

#%%
def photonflux_plots(am, am_names):
    plt.figure(figsize=(15,8))
    
    plt.subplot(121)
    for i in range(0, len(am_names)):
        plt.plot(am[am_names[i]]['wavelength_interp'], am[am_names[i]]['photonflux']['subcutaneous']['global_horizn_interp'])
    legend_names = list(am_names)
    plt.legend(legend_names)
    plt.xlabel(r'$\lambda$ [nm]')
    plt.ylabel(r'subcutaneous photon flux $\phi$ [$\frac{1}{cm^2\ s\ nm}$]')
    plt.grid('on')
    plt.title('Global horizontal subcutaneous photon flux')
    
    plt.subplot(122)
    for i in range(0, len(am_names)):
        plt.plot(am[am_names[i]]['wavelength_interp'], am[am_names[i]]['photonflux']['subcutaneous']['global_tiltd_interp'])
    legend_names = list(am_names)
    plt.legend(legend_names)
    plt.xlabel(r'$\lambda$ [nm]')
    plt.ylabel(r'subcutaneous photon flux $\phi$ [$\frac{1}{cm^2\ s\ nm}$]')
    plt.grid('on')
    plt.title('Global tilted (90°) subcutaneous photon flux')
    
    return

#%%
def get_irradiance(am, am_names, bashkatov):
    for i in range(0, len(am_names)):
        
        am[am_names[i]]['irradiance'] = {}
        am[am_names[i]]['irradiance']['subcutaneous'] = {}
        am[am_names[i]]['irradiance']['subcutaneous']['global_horizn_irradiance_interp'] = {}
        am[am_names[i]]['irradiance']['subcutaneous']['direct_horizn_irradiance_interp'] = {}
        am[am_names[i]]['irradiance']['subcutaneous']['dif_horizntl_irradiance_interp'] = {}
        am[am_names[i]]['irradiance']['subcutaneous']['global_tiltd_irradiance_interp'] = {}
        
        am[am_names[i]]['irradiance']['subcutaneous']['global_horizn_interp'] = \
                  [am[am_names[i]]['global_horizn_irradiance_interp'][p] * bashkatov['tf_interp'][p] \
                   for p in range(0, len(am[am_names[i]]['global_horizn_irradiance_interp']))]
        am[am_names[i]]['irradiance']['subcutaneous']['direct_horizn_interp'] = \
                  [am[am_names[i]]['direct_horizn_irradiance_interp'][p] * bashkatov['tf_interp'][p] \
                   for p in range(0, len(am[am_names[i]]['direct_horizn_irradiance_interp']))]
        am[am_names[i]]['irradiance']['subcutaneous']['dif_horizntl_interp'] = \
                  [am[am_names[i]]['difuse_horizn_irradiance_interp'][p] * bashkatov['tf_interp'][p] \
                   for p in range(0, len(am[am_names[i]]['difuse_horizn_irradiance_interp']))]
        am[am_names[i]]['irradiance']['subcutaneous']['global_tiltd_interp'] = \
                  [am[am_names[i]]['global_tilted_irradiance_interp'][p] * bashkatov['tf_interp'][p] \
                   for p in range(0, len(am[am_names[i]]['global_tilted_irradiance_interp']))]
    
    return am

#%%
def irradiance_plots(am, am_names):
    plt.figure(figsize=(15,8))
    
    plt.subplot(121)
    for i in range(0, len(am_names)):
        plt.plot(am[am_names[i]]['wavelength_interp'], am[am_names[i]]['irradiance']['subcutaneous']['global_horizn_interp'])
    legend_names = list(am_names)
    plt.legend(legend_names)
    plt.xlabel(r'$\lambda$ [nm]')
    plt.ylabel(r'subcutaneous irradiance  [$\frac{W}{m^2}$]')
    plt.grid('on')
    plt.title('Global horizontal subcutaneous irradiance')
    
    plt.subplot(122)
    for i in range(0, len(am_names)):
        plt.plot(am[am_names[i]]['wavelength_interp'], am[am_names[i]]['irradiance']['subcutaneous']['global_tiltd_interp'])
    legend_names = list(am_names)
    plt.legend(legend_names)
    plt.xlabel(r'$\lambda$ [nm]')
    plt.ylabel(r'subcutaneous irradiance  [$\frac{W}{m^2}$]')
    plt.grid('on')
    plt.title('Global tilted (90°) subcutaneous irradiance')
    
    return

#%%
def get_factors(am, am_names, photon_energy, photon_energy_interp):
    print('Calculating general factors')
    for i in range(0, len(am_names)):
        am[am_names[i]]['general_factor'] = {}
        
        # irradiance factors
        am[am_names[i]]['general_factor']['irradiance'] = {}
        # global horizontal
        am[am_names[i]]['general_factor']['irradiance']['global_horizn'] = \
                    (np.trapz(am[am_names[i]]['irradiance']['subcutaneous']['global_horizn_interp'], am[am_names[i]]['wavelength_interp']) / \
                    np.trapz(am[am_names[i]]['global_horizn_irradiance_interp'], am[am_names[i]]['wavelength_interp']))
        
        # photon flux factors
        am[am_names[i]]['general_factor']['photon_flux'] = {}
        #global horizontal
        am[am_names[i]]['general_factor']['photon_flux']['global_horizn'] = \
                    (np.trapz(am[am_names[i]]['photonflux']['subcutaneous']['global_horizn_interp'], am[am_names[i]]['wavelength_interp']) / \
                    np.trapz([am[am_names[i]]['global_horizn_irradiance_interp'][p] / photon_energy_interp[p] \
                   for p in range(0, len(am[am_names[i]]['global_horizn_irradiance_interp']))], am[am_names[i]]['wavelength_interp']))
        
    return am

#%%
def info(am, am_names, photon_energy):
    print('____________________________________________________________')
    print('Radiation data overview')
    print('____________________________________________________________\n')
    for i in range(0, len(am_names)):
        # integrate the given and calculated irradiance over the given spectrum
        print('__%s________________________________________________________' % am_names[i])
        print('horizontal radiation (280-4000 nm):')
        print('%.2f W/m2 (global horizontal irradiance)' \
              % (np.trapz(am[am_names[i]]['global_horizn_irradiance'], am[am_names[i]]['wavelength'])))
        print('%.2f W/m2 (direct horizontal irradiance)' \
              % (np.trapz(am[am_names[i]]['direct_horizn_irradiance'], am[am_names[i]]['wavelength'])))
        print('%.2f W/m2 (diffuse horizontal irradiance)' \
              % (np.trapz(am[am_names[i]]['difuse_horizn_irradiance'], am[am_names[i]]['wavelength'])))
        print('%.2E #photons/m2s (based on calculated photon flux (global horizontal))' \
              % (np.trapz([am[am_names[i]]['global_horizn_irradiance'][p] / photon_energy[p] \
                   for p in range(0, len(am[am_names[i]]['global_horizn_irradiance']))], am[am_names[i]]['wavelength'])))
        print('%.2E #photons/m2s (based on given photon flux (global horizontal))' \
              % (np.trapz([am[am_names[i]]['global_horizn_photon_flux'][p] * int(1e4) * am[am_names[i]]['wavelength'][p] \
                for p in range(0, len(am[am_names[i]]['wavelength']))], am[am_names[i]]['wavelength']))) # * 1e4 für cm2 zu m2, * lambda für nm-1
        print('%.2E #photons/m2s (based on given photon flux (global horizontal, without lambda multiplication))\n' \
              % (np.trapz([am[am_names[i]]['global_horizn_photon_flux'][p] * int(1e4) \
                for p in range(0, len(am[am_names[i]]['wavelength']))], am[am_names[i]]['wavelength']))) # * 1e4 für cm2 zu m2, * lambda für nm-1
        
        print('direct normal radiation (280-4000 nm):')
        print('%.2f W/m2 (direct normal irradiance)\n' \
              % (np.trapz(am[am_names[i]]['direct_normal_irradiance'], am[am_names[i]]['wavelength'])))
        
        print('tilted global radiation (90°) (280-4000 nm):')
        print('%.2f W/m2 (global tilted (90°) irradiance)\n' \
              % (np.trapz(am[am_names[i]]['global_tilted_irradiance'], am[am_names[i]]['wavelength'])))
        
        print('Interpolated and lambda-restricted (400-2000 nm) data:')
        print('%.2f W/m2 (global horizontal irradiance)\n' \
              % (np.trapz(am[am_names[i]]['global_horizn_irradiance_interp'], am[am_names[i]]['wavelength_interp'])))
        
        
        # integrate the given and calculated irradiance over the given spectrum
        print('__%s_subcutaneous___________________________________________' % am_names[i])
        print('Interpolated and lambda-restricted (400-2000 nm) data:')
        print('%.2f W/m2 (global horizontal irradiance)' \
              % (np.trapz(am[am_names[i]]['irradiance']['subcutaneous']['global_horizn_interp'], am[am_names[i]]['wavelength_interp'])))
        print('%.2f W/m2 (direct horizontal irradiance)' \
              % (np.trapz(am[am_names[i]]['irradiance']['subcutaneous']['direct_horizn_interp'], am[am_names[i]]['wavelength_interp'])))
        print('%.2f W/m2 (diffuse horizontal irradiance)' \
              % (np.trapz(am[am_names[i]]['irradiance']['subcutaneous']['dif_horizntl_interp'], am[am_names[i]]['wavelength_interp'])))
        print('%.2f W/m2 (global tilted irradiance)' \
              % (np.trapz(am[am_names[i]]['irradiance']['subcutaneous']['global_tiltd_interp'], am[am_names[i]]['wavelength_interp'])))
        print('%.2E #photons/m2s (photon flux (global horizontal))\n' \
              % (np.trapz(am[am_names[i]]['photonflux']['subcutaneous']['global_horizn_interp'], am[am_names[i]]['wavelength_interp'])))
        
        print('__%s_factor_________________________________________________' % am_names[i])
        print('Relevant factor: \nphoton flux or irradiance(subcutaneous BSRN) / photon flux or irradiance(SMARTS)\n')
        print('restricted factor irradiance: %.2f (global horizontal irradiance)' % am[am_names[i]]['general_factor']['irradiance']['global_horizn'])
        print('restricted factor photon flux: %.2f (global horizontal photon flux)\n\n\n\n' % am[am_names[i]]['general_factor']['photon_flux']['global_horizn'])
        
    return

#%%
def main(am, am_names, bashkatov):
    photon_energy, photon_energy_interp = get_photon_energy(am, am_names)
    am = get_photonflux(am, am_names, bashkatov, photon_energy_interp)
    photonflux_plots(am, am_names)
    am = get_irradiance(am, am_names, bashkatov)
    irradiance_plots(am, am_names)
    am = get_factors(am, am_names, photon_energy, photon_energy_interp)
    info(am, am_names, photon_energy)
    return photon_energy, photon_energy_interp, am

#%%
if __name__ == '__main__':
    import airmass
    import bashka
    am, am_names, air_masses = airmass.get_am(interp_range)
    bashkatov = bashka.get_bashkatov(interp_range)
    photon_energy, photon_energy_interp, am = main(am, am_names, bashkatov)