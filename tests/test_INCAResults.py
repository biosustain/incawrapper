import pytest
import pathlib
import os 
from incawrapper.core.INCAResults import INCAResults

current_dir = pathlib.Path(__file__).parent.absolute()

# the fixtures used in the tests (e.g. inca_results_simple_model) are defined in conftest.py


def test_get_metabolite_ids(inca_results_simple_model):
    """
    Tests if the inca model is properly loaded and thus the metabolite ids are 
    correctly extracted from the model object.
    """
    expected_metabolite_ids = [
        'A', 'B', 'C', 'D', 'E', 'F'
    ]
    assert inca_results_simple_model.model.metabolite_ids == expected_metabolite_ids

# def test_wrong_file_type():
#     """
#     Tests if the correct error is raised if the file is not a .mat file
#     """
#     with pytest.raises(ValueError):
#         INCAResults(os.path.join(current_dir, "test_data", "MFA_modelInputsData", "simple_model", "simple_model.m"))

def test_matlab_object_contains_all_parts(inca_results_simple_model):
    """Tests if the matlab object contains a model, a fit and a simulation parts."""
    assert inca_results_simple_model.model
    assert inca_results_simple_model.fitdata
    assert inca_results_simple_model.simulation


def test_load_mc_data_infer_filename():
    """
    Tests if the mc data is loaded correctly.
    """
    output_file = pathlib.Path(current_dir / "test_data" / "simple_model_mc_tutorial.mat")
    print(output_file)
    res = INCAResults(output_file, load_mc_data=True)
    assert res.mc.samples.shape == (500, 7)
    assert res.mc.ci.shape == (2, 7)


def test_load_mc_data_given_filename():
    """
    Tests if the mc data is loaded when filename is specified.
    """
    output_file = pathlib.Path(current_dir / "test_data" / "simple_model_mc_tutorial.mat")
    mcfile = pathlib.Path(current_dir / "test_data" / "simple_model_mc_tutorial_mc.mat")
    res = INCAResults(output_file, load_mc_data=mcfile)
    assert res.mc.samples.shape == (500, 7)
    assert res.mc.ci.shape == (2, 7)