#%%
import os

#%%
plots = 1

#%% import modules
if os.getcwd() == './computations':
    from gfactor_subfunctions import airmass
    from gfactor_subfunctions import bashka
    from gfactor_subfunctions import EQE
    from gfactor_subfunctions import subcutaneous_irradiance
else:
    from computations.gfactor_subfunctions import airmass
    from computations.gfactor_subfunctions import bashka
    from computations.gfactor_subfunctions import EQE
    from computations.gfactor_subfunctions import subcutaneous_irradiance
    from data_import import guenhan

#%%
def get_gfactor_data(interp_range, IXYS_EQE_path, EMPA_EQE_path):
    am, am_names, air_masses = airmass.get_am(interp_range)
    bashkatov = guenhan.import_guenhan(interp_range)
    eqe = EQE.get_eqe(interp_range, IXYS_EQE_path, EMPA_EQE_path)

    return am, am_names, eqe, bashkatov, air_masses
#%%
def main(interp_range, IXYS_EQE_path, EMPA_EQE_path):
   am, am_names, eqe, bashkatov, air_masses = get_gfactor_data(interp_range, IXYS_EQE_path, EMPA_EQE_path)
   photon_energy, photon_energy_interp = subcutaneous_irradiance.get_photon_energy(am, am_names)
   am = subcutaneous_irradiance.get_photonflux(am, am_names, bashkatov, photon_energy_interp)
   am = subcutaneous_irradiance.get_irradiance(am, am_names, bashkatov)
   am = subcutaneous_irradiance.get_factors(am, am_names, photon_energy, photon_energy_interp)

   if plots == 1:
       EQE.interpol_plot_ixys(eqe, interp_range)
       EQE.interpol_plot_empa(eqe, interp_range)
       bashka.plot_bashkatov_interp(bashkatov)
       bashka.plot_bashkatov_skinthickness(bashkatov)
       subcutaneous_irradiance.photonflux_plots(am, am_names)
       subcutaneous_irradiance.irradiance_plots(am, am_names)
       subcutaneous_irradiance.info(am, am_names, photon_energy)

   return am, am_names, eqe, bashkatov, air_masses

#%%
if __name__ == '__main__':
    am, am_names, eqe, bashkatov, air_masses =\
        main(interp_range, IXYS_EQE_path, EMPA_EQE_path)
