import pytest
import pathlib
import os 
from BFAIR.mfa.INCA.INCA_results import INCA_results

current_dir = str(pathlib.Path(__file__).parent.absolute())

# the fixtures used in the tests (e.g. inca_results) are defined in conftest.py


def test_get_metabolite_ids(inca_results):
    """
    Tests if the inca model is properly loaded and thus the metabolite ids are 
    correctly extracted from the model object.
    """
    expected_metabolite_ids = [
        'A', 'B', 'C', 'D', 'E', 'F'
    ]
    assert inca_results.model.get_metabolite_ids() == expected_metabolite_ids

def test_wrong_file_type():
    """
    Tests if the correct error is raised if the file is not a .mat file
    """
    with pytest.raises(ValueError):
        INCA_results(os.path.join(current_dir, "test_data", "MFA_modelInputsData", "simple_model", "simple_model.m"))
