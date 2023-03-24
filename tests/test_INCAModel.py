import pytest
import pathlib
import os 
from incawrapper.core.INCAModel import INCAModel

def test_init(inca_results_simple_model_filename):
    """
    Tests if the INCAModel object is correctly initialized
    """
    model = INCAModel(inca_results_simple_model_filename)
    assert type(model) == INCAModel

def test_get_metabolite_ids(inca_results_simple_model_filename):
    """
    Tests if the metabolite ids are correctly extracted
    """
    model = INCAModel(inca_results_simple_model_filename)
    expected_metabolite_ids = [
        'A', 'B', 'C', 'D', 'E', 'F'
    ]
    assert model.get_metabolite_ids() == expected_metabolite_ids

def test_inca_options(inca_results_simple_model_filename):
    """
    Tests if the inca options are correctly extracted
    """
    model = INCAModel(inca_results_simple_model_filename)
    assert type(model.inca_options) == dict
    assert model.inca_options['cont_alpha'] == 0.05