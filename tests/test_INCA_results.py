import pytest
import pathlib
import os 
from BFAIR.mfa.INCA.INCA_results import INCA_results

current_dir = str(pathlib.Path(__file__).parent.absolute())

@pytest.fixture
def inca_results():
    return INCA_results(os.path.join(current_dir, "test_data", "MFA_modelInputsData", "simple_model", "simple_model.mat"))

def test_get_metabolite_ids(inca_results):
    """
    Tests if the metabolite ids are correctly extracted
    """
    expected_metabolite_ids = [
        'A', 'B', 'C', 'D', 'E', 'F'
    ]
    assert inca_results.get_metabolite_ids() == expected_metabolite_ids
