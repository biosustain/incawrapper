import pytest
import pathlib
import os 
from incawrapper.core.INCAModel import INCAModel

current_dir = str(pathlib.Path(__file__).parent.absolute())

@pytest.fixture
def inca_model():
    return INCAModel(os.path.join(current_dir,"..", "docs", "examples", "simple_model", "simple_model_quickstart.mat"))

def test_get_metabolite_ids(inca_model):
    """
    Tests if the metabolite ids are correctly extracted
    """
    expected_metabolite_ids = [
        'A', 'B', 'C', 'D', 'E', 'F'
    ]
    assert inca_model.get_metabolite_ids() == expected_metabolite_ids

def test_inca_options(inca_model):
    """
    Tests if the inca options are correctly extracted
    """
    assert type(inca_model.inca_options) == dict
    assert inca_model.inca_options['cont_alpha'] == 0.05