'''This is a test script that can be used to test that INCA is actually able to execute 
the script created by the incawrapper. Since the script is executed in matlab, this test
requires that matlab and INCA is installed on the system, which not possible on the
github actions CI. Thus, this test is not run as part of the CI.

The script is based on the simple model example, similar to the quick start tutorial.'''
import os
import pandas as pd
import pathlib
import incawrapper
from incawrapper import run_inca
import pytest
import ast

work_dir = pathlib.Path(__file__).parents[1]

# Load the data
data_folder = work_dir / "docs" / "examples" / "Literature data" / "simple model"
tracers_data = pd.read_csv(data_folder / "tracers.csv", 
   converters={'atom_mdv':ast.literal_eval, 'atom_ids':ast.literal_eval} # a trick to read lists from csv
)
reactions_data = pd.read_csv(data_folder / "reactions.csv")
flux_data = pd.read_csv(data_folder / "flux_measurements.csv")
ms_data = pd.read_csv(data_folder / "ms_measurements.csv", 
   converters={'labelled_atom_ids': ast.literal_eval} # a trick to read lists from csv
)

# %%
output_file = work_dir / "tests" / "simple_model_quikstart.mat"
script = incawrapper.create_inca_script_from_data(reactions_data, tracers_data, flux_data, ms_data, experiment_ids=["exp1"])
script.add_to_block("options", incawrapper.define_options(fit_starts=5,sim_na=False))
script.add_to_block("runner", incawrapper.define_runner(output_file, run_estimate=True, run_simulation=True, run_continuation=True))

# %%
import dotenv
inca_directory = pathlib.Path(str(dotenv.get_key(dotenv.find_dotenv(), "INCA_base_directory")))
incawrapper.run_inca(script, INCA_base_directory=inca_directory)

# %%
res = incawrapper.INCAResults(output_file)

# %%
res.fitdata.fitted_parameters

## tests

### Testing consistency of the results
assert res.fitdata.fitted_parameters.loc[5, 'val'] == pytest.approx(8.042115, 0.01)
assert res.fitdata.fitted_parameters.loc[5, 'lb'] == pytest.approx(7.97, 0.01)

### Testing that the model is correct
assert len(res.model.metabolite_ids) == 6, "Number of metabolites is not correct in model"

print("INCA execution test passed")

# %%
## Cleanup
print("Cleaning up...")
os.remove(output_file)