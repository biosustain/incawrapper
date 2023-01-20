# This file contains fixtures used in testing of the package
# 
import pytest
import pathlib
import os 
from BFAIR.mfa.INCA.INCA_results import INCA_results

current_dir = str(pathlib.Path(__file__).parent.absolute())


@pytest.fixture
def inca_results_simple_model():
    return INCA_results(os.path.join(current_dir, "test_data", "MFA_modelInputsData", "simple_model", "simple_model.mat"))

