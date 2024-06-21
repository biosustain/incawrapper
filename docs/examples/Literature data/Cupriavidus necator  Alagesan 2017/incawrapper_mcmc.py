# %% [markdown]
# # INCAWrapper validation case medium size model
# This notebook serves as a validation case the show that the INCAWrapper produce similar results as a model run through the INCA GUI. Furthermore, this notebook can be used as an integration test of the INCAWrapper that can be run when changes are made to the codebase to ensure that the INCAWrapper performs consistently. This notebook is not meant as a tutorial and therefore code description is a bit more sparse. For a proper tutorial see the other examples at https://incawrapper.readthedocs.io/en/latest/examples/index.html.
#
# ## Introduction
# The model we use is from Alagesan, S., Minton, N.P. & Malys, N. 13C-assisted metabolic flux analysis to investigate heterotrophic and mixotrophic metabolism in Cupriavidus necator H16. Metabolomics 14, 9 (2018). https://doi.org/10.1007/s11306-017-1302-z, which is also used for one of the tutorials.
#
# To ensure that we can obtain a good fits to the data, we employ a simulated dataset for this validation. The simulation mimics three parallel experiment where *C. necator* is grown with different labelled fructose ([1-13C]fructose, [2-13C]fructose, and [6-13C]fructose). We simulated MS measurements of some amino acids and measurements of 4 exchanges fluxes. To increase the information in the data we added one additional reaction to the original model, i.e. CO2 -> CO2.ext. After simulating the data, we added 0.003 absolute measurement error to all MDV measurements and 0.003 relative measurement error to all flux measurements. For more details about the simulation see the file `docs/examples/Literature data/Cupriavidus necator  Alagesan 2017/c_necator_simulation.py`.
#
# ## Method for INCA GUI based flux estimation
# The model, experiments and data was manually entered into the INCA GUI. This model was saved to a file (`docs/examples/Literature data/Cupriavidus necator  Alagesan 2017/c_necator_gui.mat`). We then ran first the estimate and second the continuation procedure before saving the "fluxmap" to a difference file (`docs/examples/Literature data/Cupriavidus necator  Alagesan 2017/simulated_data/c_necator_gui_fluxmap.mat`).
#
# ## Note about randomness in INCA
# When INCA estimates the flux distribution it deploys an optimisation algorithm, which searches for a local optimum in the parameter space. To increase the probability that the found flux distribution is a global optimum INCA can be configured to restart the optimisation algorithm at different point in the parameter space. Unfortunately, the INCA manual do not describe any method to set the random seed for random restarts, thus the best we can do is to a large number of restarts in both the INCA GUI and the INCAWrapper to improve the probability that the two executions finds the same optimum. Therefore, we used 1000 restarts during flux estimation in both the INCAWrapper and the INCA GUI.
#
# ## Setting up the environment
# First, we will setup the coding environment, load packages, set pah to files and read-in the data.

# %%
import pandas as pd
import numpy as np
import dotenv
import ast
import pandera as pa
import incawrapper
from incawrapper import utils
from incawrapper import visualization
import pathlib
import matplotlib.pyplot as plt
import pytest
import time

# %%
# import environment variables
INCA_base_directory = dotenv.get_key(dotenv.find_dotenv(), "INCA_base_directory")

# %%
# set up path to data
working_dir = pathlib.Path(dotenv.find_dotenv()).parent
data_directory = (
    working_dir
    / "docs"
    / "examples"
    / "Literature data"
    / "Cupriavidus necator  Alagesan 2017"
    / "simulated_data"
)
results_file = data_directory / "c_necator_incawrapper_mcmc.mat"

# %%
# Reading the reactions, tracers, and simulated measurements
rxn = pd.read_csv(data_directory / "reactions_processed.csv")
tracers = pd.read_csv(
    data_directory / "tracer_info.csv",
    converters={"atom_ids": ast.literal_eval, "atom_mdv": ast.literal_eval},
)
flux_measurements = pd.read_csv(data_directory / "flux_measurements_noisy_rounded.csv")
mdv_measurements = pd.read_csv(
    data_directory / "mdv_noisy_rounded.csv",
    converters={"labelled_atom_ids": ast.literal_eval},
)

# %% [markdown]
# Looking at the traces dataframe, we can see the experimental design in this simulated dataset.

# %%

# %% [markdown]
# ## Setup the INCAScript
# We will now setup and run INCA. Notice that we set fit_restarts=1000, this increase the chance that the two optimization runs (GUI and INCAWrapper) find the same optimum.

# %%

# Create the INCA script
script = incawrapper.create_inca_script_from_data(
    reactions_data=rxn,
    tracer_data=tracers,
    flux_measurements=flux_measurements,
    ms_measurements=mdv_measurements,
    experiment_ids=tracers.experiment_id.unique().tolist(),
)

# Define options, the INCAWrapper leaves the remaining options at their default value
script.add_to_block(
    "options",
    incawrapper.define_options(
        fit_starts=1000,
        sim_ss=True,
        sim_na=True,
        sim_more=True,
    ),
)

# Define what algorithm to run in INCA
script.add_to_block(
    "runner",
    incawrapper.define_runner(
        output_filename=results_file,
        run_estimate=True,
        run_continuation=False,
        run_simulation=True,  # simulation has to be run otherwise the results file is invalid
        run_montecarlo=True,
    ),
)

# %%
# run INCA
incawrapper.run_inca(
    inca_script=script,
    INCA_base_directory=INCA_base_directory,
    execution_directory=data_directory,
)
