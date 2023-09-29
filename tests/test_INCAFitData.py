import pandas as pd
from incawrapper.core.INCAFitData import INCAFitData

def test_init(inca_results_simple_model_filename):
    """
    Tests if the INCAFitData object is correctly initialized
    """
    data = INCAFitData(inca_results_simple_model_filename)
    assert type(data) == INCAFitData

def test_parses_fitted_parameters(inca_results_simple_model_filename):
    """
    Tests if the fitted parameters are correctly parsed
    """
    data = INCAFitData(inca_results_simple_model_filename)
    assert type(data.fitted_parameters) == pd.DataFrame
    assert data.fitted_parameters.shape[0] == 7





