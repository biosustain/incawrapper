import pandas as pd
import dotenv
import os
import logging
# set working directory to the root of the repository
os.chdir(dotenv.find_dotenv().replace(".env", ""))

from BFAIR.mfa import INCA

# Loading data
modelReaction_data_I = pd.read_csv(
    os.path.join(
        "tests",
        "test_data",
        "MFA_modelInputsData",
        "simple_model",
        "modelReactions.csv",
    )
)

atomMappingReactions_data_I = pd.read_csv(
    os.path.join(
        "tests",
        "test_data",
        "MFA_modelInputsData",
        "simple_model",
        "atomMappingReaction2.csv",
    )
)

atomMappingMetabolite_data_I = pd.read_csv(
    os.path.join(
        "tests",
        "test_data",
        "MFA_modelInputsData",
        "simple_model",
        "atomMappingMetabolites.csv",
    )
)

measuredFluxes_data_I = pd.read_csv(
    os.path.join(
        "tests",
        "test_data",
        "MFA_modelInputsData",
        "simple_model",
        "measuredFluxes.csv",
    )
)

experimentalMS_data_I = pd.read_csv(
    os.path.join(
        "tests",
        "test_data",
        "MFA_modelInputsData",
        "simple_model",
        "experimentalMS.csv",
    )
)

tracers_data_I = pd.read_csv(
    os.path.join(
        "tests",
        "test_data",
        "MFA_modelInputsData",
        "simple_model",
        "tracers.csv",
    )
)

# generate the INCA script
inca_script = INCA.INCA_script()

simple_model_script = inca_script.script_generator(
    modelReaction_data_I,
    atomMappingReactions_data_I,
    atomMappingMetabolite_data_I,
    measuredFluxes_data_I,
    experimentalMS_data_I,
    tracers_data_I
)

simple_model_dir = os.path.join(os.getcwd(), "tests", "test_data", "MFA_modelInputsData", "simple_model")
matlab_script_filename = os.path.join(simple_model_dir, "simple_model")
runner_script_filename = os.path.join(simple_model_dir, "simple_model")

inca_script.save_INCA_script(simple_model_script, matlab_script_filename)
runner = inca_script.runner_script_generator("simple_model", 10)
inca_script.save_runner_script(runner=runner, scriptname=runner_script_filename)

# Prepare to run INCA in matlab
INCA_base_directory = dotenv.get_key(dotenv.find_dotenv(), "INCA_base_directory") # Add your INCA base directory here

# Run INCA in matlab
inca_script.run_INCA_in_MATLAB(
    INCA_base_directory,
    simple_model_dir,
    os.path.split(matlab_script_filename)[-1], # this argument does not accept absolute paths
    os.path.split(runner_script_filename)[-1] + "_runner" # this argument does not accept absolute path
)
