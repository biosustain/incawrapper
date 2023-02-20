# This file contains fixtures used in testing of the package
# 
import pytest
import pathlib
import os 
import pandas as pd
import numpy as np
from BFAIR.mfa.INCA.INCAResults import INCAResults
from BFAIR.mfa.INCA.INCAScript import INCAScript
current_dir = str(pathlib.Path(__file__).parent.absolute())


@pytest.fixture
def inca_results_simple_model():
    return INCAResults(os.path.join(current_dir, "test_data", "MFA_modelInputsData", "simple_model", "simple_model.mat"))


@pytest.fixture
def inca_script():
    return INCAScript()

@pytest.fixture
def reaction_test():
    return pd.DataFrame(
        {
            "rxn_eqn": ["A.ext (C1:a C2:b) -> A (C1:a C2:b)", "A (C1:a C2:b) -> B (C1:b C2:a)", "B -> C", "C -> D"],
            "rxn_id": ["r1", "r2", "r3", "r4"],
        }
    )

@pytest.fixture
def tracer_df_test():
    return pd.DataFrame(
        {
            "experiment_id": ["exp1", "exp1"],
            "tracer_id": ["[1-13C]A", "[1,2-13C]B"],
            "met_id": ["A.ext", "B"],
            "atom_ids": [[1], [1,2]],
            "atom_mdv" : [[0.02, 0.98], [0.05, 0.95]],
            "enrichment": [0.5, 0.5],
        }
    )

@pytest.fixture
def flux_measurements_test():
    return pd.DataFrame(
        {
            "experiment_id": ["exp1", "exp1", "exp1"],
            "rxn_id": ["r1", "r2", "r3"],
            "flux": [1.0, 2.0, 3.0],
            "flux_std_error": [0.1, 0.2, 0.3],
        }
    )

@pytest.fixture
def ms_measurements_test():
    return pd.DataFrame(
        {
            "experiment_id": np.repeat(["exp1", "exp2"], 4),
            "met_id": np.repeat(["A"], 8),
            "ms_id": np.repeat(["A1"], 8),
            "labelled_atom_ids": [list([1,2,3,4]) for _ in range(8)],
            "measurement_replicate": np.repeat([1], 8),
            "unlabelled_atoms": np.repeat([""], 8),
            "mass_isotope": [0, 2, 3, 4, 1,2,3,4],
            "intensity": np.repeat([0.1, 0.4, 0.3, 0.2], 2),
            "intensity_std_error": np.repeat([0.01, 0.02, 0.03, 0.04], 2),
            "time": np.repeat([0], 8),
        }
    )
