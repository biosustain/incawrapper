"""This script is a part of the INCAWrapper validation. It executes MCMC sampling from the flux distributions of a simple model. 
"""

import pandas as pd
import dotenv
import ast
import incawrapper
import pathlib


# import environment variables
INCA_base_directory = dotenv.get_key(dotenv.find_dotenv(), "INCA_base_directory")

# set up path to data
working_dir = pathlib.Path(dotenv.find_dotenv()).parent
data_directory = (
    working_dir
    / "docs"
    / "examples"
    / "Literature data"
    / "simple model"
    / "simulated_data"
)
results_file = data_directory / "simple_model_incawrapper_fluxmap_mcmc.mat"
mcmc_results_file = data_directory / "simple_model_incawrapper_mcmc_results.csv"

# Reading the reactions, tracers, and simulated measurements
rxn = pd.read_csv(data_directory / "reactions.csv")
tracers = pd.read_csv(
    data_directory / "tracers.csv",
    converters={"atom_ids": ast.literal_eval, "atom_mdv": ast.literal_eval},
)

mdv_measurements = pd.read_csv(
    data_directory / "mdv_noisy.csv",
    converters={"labelled_atom_ids": ast.literal_eval},
)
pool_sizes = pd.read_csv(data_directory / "pool_sizes_measurement_noisy.csv")
flux_measurements = pd.read_csv(data_directory / "flux_measurements_noisy.csv")

mdv_measurements["intensity"] = round(mdv_measurements["intensity"], 4)
pool_sizes["pool_size"] = round(pool_sizes["pool_size"], 4)
flux_measurements["flux"] = round(flux_measurements["flux"], 4)
flux_measurements["flux_std_error"] = round(flux_measurements["flux_std_error"], 4)

mdv_measurements.to_csv(data_directory / "mdv_noisy_rounded.csv", index=False)
pool_sizes.to_csv(
    data_directory / "pool_sizes_measurement_noisy_rounded.csv", index=False
)
flux_measurements.to_csv(
    data_directory / "flux_measurements_noisy_rounded.csv", index=False
)
script = incawrapper.create_inca_script_from_data(
    reactions_data=rxn,
    tracer_data=tracers,
    flux_measurements=flux_measurements,
    ms_measurements=mdv_measurements,
    experiment_ids=["exp1"],
    pool_measurements=pool_sizes,
)

# Define options, the INCAWrapper leaves the remaining options at their default value
script.add_to_block(
    "options",
    incawrapper.define_options(
        fit_starts=1000,
        sim_ss=False,
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


# run INCA
incawrapper.run_inca(
    inca_script=script,
    INCA_base_directory=INCA_base_directory,
    execution_directory=data_directory,  # set the execution directory to store the results in case the script is interrupted
)

res = incawrapper.INCAResults(results_file, load_mc_data=True)
res.mc.samples.to_csv(mcmc_results_file, index=False)
