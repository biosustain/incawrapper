import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from incawrapper.mfa.visualization.distributions import _reduce_sampled_fluxes


def _prepare_input_fluxes(sampled_fluxes, flux):
    """
    Makes sure that the provided fluxes are in the right format
    for other functions. Input can either be a flux id or a
    cobbination of fluxes provided as a Series.

    Parameters
    ----------
    sampled_fluxes : pandas.Dataframe
        The calculated fluxes, output of sampling. For each reaction,
        n fluxes will be calculated (n = number of samples taken).
    flux : pandas.Series or str
        Either a selected column (or combination of fluxes) or the
        name of a flux.

    Returns
    -------
    flux : pandas.Series
        Selected flux in the relevant format.
    """
    if isinstance(flux, pd.Series):
        return flux
    elif isinstance(flux, str):
        flux = sampled_fluxes[flux]
        return flux
    else:
        raise TypeError(
            f"The input is a '{type(flux)}', this type of object"
            " cannot be used here, please provide a pd.Series or"
            "a column identifier (string)"
        )


def calculate_split_ratio(
    sampled_fluxes,
    influx,
    split_flux1,
    split_flux2=None,
    branch_point_name="Branch point",
):
    """
    Calculates the ratios of the in- and effluxes at a split point.

    Parameters
    ----------
    sampled_fluxes : pandas.Dataframe
        The calculated fluxes, output of sampling. For each reaction,
        n fluxes will be calculated (n = number of samples taken).
    influx : string or pandas.Series
        Name of the reaction flowing to the branch point or pre-processed
        combined flux coming to the branch point.
    split_flux1 : string or pandas.Series
        Name of flux #1 coming out of the branch point or pre-processed
        combined flux coming out of the branch point.
    split_flux2 : string or pandas.Series
        Name of flux #2 coming out of the branch point or pre-processed
        combined flux coming out of the branch point.
        Defaults to `None`.
    branch_point_name : string
        name of the branch point to be added to the output.
        Defaults to "Branch point".

    Returns
    -------
    output_df : pandas.Dataframe
        Presents the split flux ratio.
    """
    influx = _prepare_input_fluxes(sampled_fluxes, influx)
    split_flux1 = _prepare_input_fluxes(sampled_fluxes, split_flux1)
    mean_list = [np.abs(np.mean(split_flux1 / influx))]
    stdev_list = [np.std(split_flux1 / influx)]
    index_list = [influx.name + "/" + split_flux1.name]
    if split_flux2 is not None:
        split_flux2 = _prepare_input_fluxes(sampled_fluxes, split_flux2)
        mean_list.append(np.abs(np.mean(split_flux2 / influx)))
        stdev_list.append(np.std(split_flux2 / influx))
        index_list.append(influx.name + "/" + split_flux2.name)
    fluxes = {
        "Mean": mean_list,
        "Stdev": stdev_list,
    }
    output_df = pd.DataFrame(
        fluxes, columns=["Mean", "Stdev"], index=[index_list]
    )
    return output_df


def plot_split_ratio(
    sampled_fluxes,
    influx,
    split_flux1,
    split_flux2=None,
    branch_point_name="Branch point",
):
    """
    Visualization of the in- and effluxes at a split point.

    Parameters
    ----------
    sampled_fluxes : pandas.Dataframe
        The calculated fluxes, output of sampling. For each reaction,
        n fluxes will be calculated (n = number of samples taken).
    influx : string or pandas.Series
        Name of the reaction flowing to the branch point or pre-processed
        combined flux coming to the branch point.
    split_flux1 : string or pandas.Series
        Name of flux #1 coming out of the branch point or pre-processed
        combined flux coming out of the branch point.
    split_flux2 : string or pandas.Series
        Name of flux #2 coming out of the branch point or pre-processed
        combined flux coming out of the branch point.
        Defaults to `None`.
    branch_point_name : string
        name of the branch point to be added to the output.
        Defaults to "Branch point".

    Returns
    -------
    fig : matplotlib.Figure
        Figure of the sampled value distribution of the in-
        and effluxes at a split point.
    """
    influx = _prepare_input_fluxes(sampled_fluxes, influx)
    split_flux1 = _prepare_input_fluxes(sampled_fluxes, split_flux1)
    if split_flux2 is not None:
        split_flux2 = _prepare_input_fluxes(sampled_fluxes, split_flux2)
        sum_ratios = abs(split_flux1 / influx) + abs(split_flux2 / influx)
        split_df = pd.DataFrame(
            {
                "Sum": sum_ratios,
                split_flux1.name: abs(split_flux1 / influx),
                split_flux2.name: abs(split_flux2 / influx),
            }
        )
        plot_title = (
            f"{influx.name} / {split_flux1.name} vs.\n"
            f"{influx.name} / {split_flux2.name}"
        )
    else:
        split_df = pd.DataFrame({split_flux1.name: abs(split_flux1 / influx), })
        plot_title = f"{influx.name} / {split_flux1.name}"

    re_arranged_df = _reduce_sampled_fluxes(split_df, split_df.columns)

    fig = sns.boxplot(
        x="Reaction", y="Sampled Fluxes", data=re_arranged_df, orient="v"
    )
    plt.xticks(rotation=70)
    plt.title(f"{branch_point_name}:\n{plot_title}", size=15)
    return fig
