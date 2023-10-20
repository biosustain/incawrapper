"""This script creates a simulated data set for the simple model. The data set is used to show
to use the INCAWrapper to run Isotope Non-stationary 13C-MFA. The INCAWrapper does not include a 
good API for simulation, thus this is sometimes a bit hacky and requires some knowledge of how to
use INCA Matlab scripts."""
# %%
import pandas as pd
import numpy as np
import pathlib
import incawrapper
from incawrapper import run_inca
import ast

# %%
data_folder = pathlib.Path(__file__).parent
output_folder = data_folder / "simulated_data"
tracers_data = pd.read_csv(data_folder / "tracers.csv", 
   converters={'atom_mdv':ast.literal_eval, 'atom_ids':ast.literal_eval} # a trick to read lists from csv
)
reactions_data = pd.read_csv(data_folder / "reactions.csv")

# %%
# INCA only save the simulation for the MDV that are measured. 
# Thus, we will create some dummy measurements for the MDVs that
# we with to simulate. 

n_isotopomers = 4
def construct_abitrary_ms_measurement(
        experiement_id,
        met_id,
        ms_id,
        n_isotopomers,
        time,
)->pd.DataFrame:
    return pd.DataFrame({
        "experiment_id": [experiement_id]*n_isotopomers,
        "met_id": [met_id]*n_isotopomers,
        "ms_id": [ms_id]*n_isotopomers,
        'measurement_replicate': [1]*n_isotopomers,
        "labelled_atom_ids": [list(np.arange(1, n_isotopomers))]*n_isotopomers,
        "unlabelled_atoms" : [np.nan]*n_isotopomers,
        "mass_isotope" : np.arange(0, n_isotopomers),
        "intensity": [np.nan]*n_isotopomers,
        "intensity_std_error": [np.nan]*n_isotopomers,
        'time': [time]*n_isotopomers,
    })

#%%
collector_new_ms_data = []
for timepoint in np.arange(5):
    collector_new_ms_data.append(
        construct_abitrary_ms_measurement(
            experiement_id='exp1',
            met_id='B',
            ms_id='B1',
            n_isotopomers=4,
            time=timepoint,
        )
    )

    collector_new_ms_data.append(
        construct_abitrary_ms_measurement(
            experiement_id='exp1',
            met_id='F',
            ms_id='F1',
            n_isotopomers=4,
            time=timepoint,
        )
    )

    collector_new_ms_data.append(
        construct_abitrary_ms_measurement(
            experiement_id='exp1',
            met_id='E',
            ms_id='E1',
            n_isotopomers=2,
            time=timepoint,
        )
    )

new_ms_data = pd.concat([*collector_new_ms_data], ignore_index=True)


# %%
output_file = pathlib.Path(data_folder / "simple_model_simulation.mat")
script = incawrapper.create_inca_script_from_data(
    reactions_data=reactions_data, 
    tracer_data=tracers_data, 
    ms_measurements=new_ms_data, 
    experiment_ids=["exp1"]
)
script.add_to_block("options", incawrapper.define_options(sim_na=False, sim_ss=False))
script.add_to_block("runner", incawrapper.define_runner(output_file, run_estimate=False, run_simulation=True))

# In the following we set the flux distribution that we wish to simulate.
# To avoid having to specify a feasible flux distribution we will guess
# a flux distribution, fix the input flux value and then find the nearest
# feasible flux distribution. Futhermore, we specify some pool sizes to 
# make the simulation more interesting.

script.add_to_block(
    block_name='model_modifications',
    matlab_script_block="""
m.rates.flx.val = [100 110 50 20 20 200];
m.rates(1).flx.fix = true;
""" + 
"""
% Set the pool sizes\n""" +
incawrapper.modify_class_instance('states', None, "B", {'val': 100}) +
incawrapper.modify_class_instance('states', None, "F", {'val': 100}) +
"""% Find nearest feasible flux solution
m.rates.flx.val = transpose(mod2stoich(m));
"""
)

# %%
# Now we can run the INCA script
import dotenv
inca_directory = pathlib.Path(dotenv.get_key(dotenv.find_dotenv(), "INCA_base_directory"))
incawrapper.run_inca(script, INCA_base_directory=inca_directory)


# %%
res = incawrapper.INCAResults(output_file)
simulated_data = res.simulation.simulated_data

# fetch the ground truth values
true_fluxes = res.model.rates_in_net_exch_format
true_pool_sizes = res.model.states

#%% Add metadata to the simulated data
simulated_mdv = (
    pd.merge(
        new_ms_data,
        simulated_data, 
        left_on=['experiment_id', 'ms_id', 'mass_isotope', 'time'],
        right_on=['expt', 'id', 'mass_isotope', 'time']
    ).drop(columns=['expt', 'id', 'type', 'intensity'])
    .rename(columns={'mdv': 'intensity'})
    .assign(intensity_std_error=0.003)
)

#%% Pool sizes measurement table
pool_sizes_measurement = (
    true_pool_sizes
    .query("id in ['B', 'F']")
    .filter(['met', 'val'])
    .rename(columns={'met': 'met_id', 'val': 'pool_size'})
    .assign(
        experiment_id='exp1',
        pool_size_std_error=0.015,
    )
)

# %% Flux measurement
flux_measurements = (
    true_fluxes
    .query("rxn_id in ['R1', 'R5']")
    .assign(
        experiment_id='exp1',
    )
)
flux_measurements['flux_std_error'] = flux_measurements['flux'] * 0.003
# %%

# save ground truth values and simulated data
simulated_mdv.to_csv(output_folder / "mdv_no_noise.csv", index=False)
pool_sizes_measurement.to_csv(output_folder / "pool_sizes_measurement_no_noise.csv", index=False)
flux_measurements.to_csv(output_folder / "flux_measurements_no_noise.csv", index=False)
true_fluxes.to_csv(output_folder / "true_fluxes.csv", index=False)
true_pool_sizes.to_csv(output_folder / "true_pool_sizes.csv", index=False)

# %%
from matplotlib import pyplot as plt
import seaborn as sns
g = sns.FacetGrid(simulated_data, col="id", hue="mass_isotope", sharey=False)
g.map_dataframe(sns.lineplot, x="time", y="mdv")
plt.legend()
