import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from incawrapper.core.INCAResults import INCAResults

def _idv_barplot(ax, grp: pd.DataFrame):
    # set width of bars
    barWidth = 0.25
    
    # set heights of bars
    data = grp['data']
    fit = grp['fit']
    
    # Set position of bar on X axis
    x_data = np.arange(len(data))
    x_fit = [x + barWidth for x in x_data]

    # error bars
    e_data = grp['std']

    # Make the plot
    ax.bar(x_data, data, width=barWidth, label='data')
    ax.bar(x_fit, fit, width=barWidth, label='fit')
    ax.errorbar(x_data, data, yerr=e_data, fmt='none', ecolor='black', capsize=3, errorevery=1, label='data std. error')

    # Add xticks on the middle of the group bars
    ax.set_xlabel('Mass isotopomer')
    ax.set_ylabel('Fraction')
    ax.set_xticks([r + barWidth/2 for r in range(len(data))], grp['peak'])
    
    return ax.legend()


def plot_idv_bar(res: INCAResults, id: str, time: int = 0, ax: plt.Axes = None):
    grp = res.fitdata.measurements_and_fit_detailed.groupby(["id", "time"]).get_group((id, time))
    
    if ax is None:
        f, ax = plt.subplots()
    ax = _idv_barplot(ax, grp)
    ax.set_title(id)
    return ax

__all__ = ["plot_idv_bar"]