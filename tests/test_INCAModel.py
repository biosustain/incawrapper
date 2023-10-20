import pandas as pd
from incawrapper.core.INCAModel import INCAModel, _convert_reactions_to_net_exch_format

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
    assert model.metabolite_ids == expected_metabolite_ids

def test_inca_options(inca_results_simple_model_filename):
    """
    Tests if the inca options are correctly extracted
    """
    model = INCAModel(inca_results_simple_model_filename)
    assert type(model.inca_options) == dict
    assert model.inca_options['cont_alpha'] == 0.05


def test_states(inca_results_simple_model_filename):
    """
    Tests if the states property is correctly extracted
    """
    model = INCAModel(inca_results_simple_model_filename)
    assert type(model.states) == pd.DataFrame
    assert model.states.shape[0] == 6


def test_convert_reactions_to_net_exch_format():
    input_data = pd.DataFrame.from_dict(
        {
            'rxn': ['A', 'B', 'B', 'C'],
            'dir': ['f', 'f', 'b', 'f'],
            'val': [1, 2, 1, 3]
        }
    )

    expected_output = pd.DataFrame.from_dict(
        {
            'rxn_id': ['A', 'B net', 'B exch', 'C'],
            'flux': [1, 1, 1, 3]
        }
    )
    converted = _convert_reactions_to_net_exch_format(input_data)

    assert pd.testing.assert_frame_equal(converted, expected_output) is None
