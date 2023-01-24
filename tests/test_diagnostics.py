import pytest
import altair as alt
import matplotlib.pyplot as plt
import pathlib
from typing import Tuple

current_dir = str(pathlib.Path(__file__).parent.absolute())

from BFAIR.mfa.visualization.diagnositics import plot_residuals_vs_fitted, plot_norm_probplot


def test_plot_residuals_vs_fitted(inca_results_simple_model):
    """
    Tests if the plot_residuals_vs_fitted function runs without errors
    and returns an altair chart
    """
    assert type(plot_residuals_vs_fitted(inca_results_simple_model)) == alt.Chart

def test_plot_norm_probplot_standard_plot(inca_results_simple_model):
    """
    Tests if the plot_norm_probplot function runs without errors and 
    returns a matplotlib figure
    """
    assert type(plot_norm_probplot(inca_results_simple_model)[0]) == plt.Figure

def test_plot_norm_probplot_interactive_plot(inca_results_simple_model):
    """
    Tests if the plot_norm_probplot with interactive option function
    runs without errors and returns an altair chart
    """

    assert type(plot_norm_probplot(inca_results_simple_model, interactive=True)) == alt.LayerChart