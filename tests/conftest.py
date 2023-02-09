# This file contains fixtures used in testing of the package
# 
import pytest
import pathlib
import os 
import pandas as pd
from BFAIR.mfa.INCA.INCA_results import INCA_results
from BFAIR.mfa.INCA.INCA_script import INCA_script
current_dir = str(pathlib.Path(__file__).parent.absolute())


@pytest.fixture
def inca_results_simple_model():
    return INCA_results(os.path.join(current_dir, "test_data", "MFA_modelInputsData", "simple_model", "simple_model.mat"))


@pytest.fixture
def inca_script():
    return INCA_script()

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
            "experiment_id": ["exp1", "exp1", "exp1", "exp1"],
            "ms_id": ["ms1", "ms2", "ms3", "ms3"],
            "met_id": ["A", "B", "C", "C"],
            "labelled_atom_ids": [[1,2], ["C3","C4"], [2,3], [2,3]],
            "unlabelled_atoms": ["C7H19O", "C2H4Si", None, None],
            "idv": [[0,1.0, 0.4], [1,0,2.0], [0,3.0, 4.0], [0,1.0, 5.0]],
            "idv_std_error": [[0,0.1, 0.2], [0.2,0,0.2], [0,0.3, 0.4], [0,0.1, 0.5]],
            "time": [0, 1, 0, 0],
        }
    )

