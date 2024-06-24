import pytest
import altair as alt
import matplotlib.pyplot as plt
import pathlib
from typing import Tuple

current_dir = str(pathlib.Path(__file__).parent.absolute())

import incawrapper.visualization as incaviz


def test_plot_residuals_vs_fitted(inca_results_simple_model):
    """
    Tests if the plot_residuals_vs_fitted function runs without errors
    and returns an altair chart
    """
    assert type(incaviz.plot_residuals_vs_fitted(inca_results_simple_model)) == alt.Chart

def test_plot_norm_prob_standard_plot(inca_results_simple_model):
    """
    Tests if the plot_norm_prob function runs without errors and 
    returns a matplotlib figure
    """
    assert type(incaviz.plot_norm_prob(inca_results_simple_model)[0]) == plt.Figure

def test_plot_norm_prob_interactive_plot(inca_results_simple_model):
    """
    Tests if the plot_norm_prob with interactive option function
    runs without errors and returns an altair chart
    """

    assert type(incaviz.plot_norm_prob(inca_results_simple_model, interactive=True)) == alt.LayerChart