import numpy as np
import math
import scipy
import scipy.stats as stats
from sklearn.neighbors import KernelDensity
import matplotlib.pyplot as plt
import seaborn as sns


def sampled_fluxes_minrange(sampled_fluxes, min_val, max_val):
    """
    Sometimes the sampled fluxes include very small predicted fluxes
    for a lot of different reactions. They might be relevant but can
    easily overwhealm plots. This function reduces the subset of
    fluxes regarded for plots.

    Parameters
    ----------
    sampled_fluxes : pandas.Dataframe
        The calculated fluxes, output of sampling. For each reaction,
        n fluxes will be calculated (n = number of samples taken).
    min_val : float, int
        Min value for excluded subset.
    max_val : float, int
        Max value for excluded subset.

    Returns
    -------
    sampled_fluxes : pandas.Dataframe
        Reduced subset of the input.
    """

    def in_between(column):
        return not all(column.between(min_val, max_val, inclusive="neither"))

    criteria = list(
        sampled_fluxes.apply(in_between, axis=0, result_type="reduce")
    )
    return sampled_fluxes[sampled_fluxes.columns[criteria]]


def show_reactions(reactions):
    """
    A function to inspect the reactions in a given subset,
    e.g. a subsytem or pathway.

    Parameters
    ----------
    reactions : list
        List of reactions, e.g. output of `get_subsytem_reactions()`.
    """
    for cnt, rxn in enumerate(reactions):
        print(f"{cnt}: {rxn}")


def _sampled_reaction_fit(sampled_values, alpha=1e-3):
    """
    Helper function to prepare the input for the sampled reaction
    fluxes plots.

    Parameters
    ----------
    sampled_values : pandas.Series
        Sampled values for one reaction.

    Returns
    -------
    sampled_reaction : list
        List of the values sampled for a given reaction.
        Sorted ascendingly.
    fit : list
        Normal distribution fit (y-Values) over the sampled
        data.
    norm_dist : boolean
        Normal distribution, yes or no
    """
    sampled_reaction = sorted(sampled_values)
    k2, p = scipy.stats.normaltest(sampled_reaction)
    if p < alpha:
        norm_dist = False
        model = KernelDensity(bandwidth=2, kernel="gaussian")
        sample = np.array(sampled_reaction)
        sample = sample.reshape((len(sample), 1))
        model.fit(sample)
        probabilities = model.score_samples(sample)
        fit = np.exp(probabilities)
    else:
        norm_dist = True
        fit = stats.norm.pdf(
            sampled_reaction,
            np.mean(sampled_reaction),
            np.std(sampled_reaction),
        )
    return sampled_reaction, fit, norm_dist


def plot_sampled_reaction_fluxes(
    sampled_fluxes, reactions, reaction_id, bins=10, alpha=1e-3
):
    """
    Plots the distribution of the sampled values for one selected
    reaction as a histogram and a normal distribution.

    Parameters
    ----------
    sampled_fluxes : pandas.Dataframe
        The calculated fluxes, output of sampling. For each reaction,
        n fluxes will be calculated (n = number of samples taken).
    reactions : list
        List of reactions, e.g. output of `get_subsytem_reactions()`.
    reaction_id : int
        ID of the reaction in the `reactions` list.
    bins : int
        Number of bins used for the histogram. Defaults to 10.

    Returns
    -------
    fig : matplotlib.Figure
        Figure of sampled value distribution for one reaction.
    """
    sampled_values = sampled_fluxes[reactions[reaction_id]]
    if all(v == 0 for v in sampled_values):
        print(f"All sample values are 0 for {reactions[reaction_id]}")
    else:
        sampled_reaction, fit, norm_dist = _sampled_reaction_fit(
            sampled_values, alpha
        )
        fig = plt.plot(
            sampled_reaction,
            fit,
            "-o",
            color=("darksalmon" if norm_dist else "darkcyan"),
        )
        plt.hist(
            sampled_reaction,
            bins=bins,
            rwidth=0.95,
            color=("darkcyan" if norm_dist else "darksalmon"),
            density=True,
        )
        plt.ylabel("Distribution [%]")
        plt.xlabel("Flux [mmol * gDCW$^{-1}$ * h$^{-1}$]")
        plt.title(reactions[reaction_id], size=20)
        return fig


def _subplot_sampled_reaction_fluxes(
    sampled_fluxes, reactions, reaction_id, bins=10, alpha=1e-3
):
    """
    Produces a subplot of the distribution of the sampled values
    for one selected reaction as a histogram and a normal distribution.

    Parameters
    ----------
    sampled_fluxes : pandas.Dataframe
        The calculated fluxes, output of sampling. For each reaction,
        n fluxes will be calculated (n = number of samples taken).
    reactions : list
        List of reactions, e.g. output of `get_subsytem_reactions()`.
    reaction_id : int
        ID of the reaction in the `reactions` list.
    bins : int
        Number of bins used for the histogram. Defaults to 10.

    Returns
    -------
    fig : matplotlib.Figure
        Figure of sampled value distribution for one reaction.
    """
    sampled_values = sampled_fluxes[reactions[reaction_id]]
    if all(v == 0 for v in sampled_values):
        fig = plt.plot(figsize=(15, 20))
        plt.axis("off")
        plt.text(
            0,
            -0.02,
            f"All sampled\nvalues are 0\nfor {reactions[reaction_id]}",
            ha="center",
            fontsize=20,
        )
    else:
        sampled_reaction, fit, norm_dist = _sampled_reaction_fit(
            sampled_values, alpha
        )
        fig = plt.plot(
            sampled_reaction,
            fit,
            "-o",
            color=("darksalmon" if norm_dist else "darkcyan"),
        )
        plt.hist(
            sampled_reaction,
            bins=bins,
            rwidth=0.95,
            color=("darkcyan" if norm_dist else "darksalmon"),
            density=True,
        )
        plt.title(reactions[reaction_id], size=20)
        return fig


def plot_all_subsystem_fluxes(sampled_fluxes, reactions, bins=10):
    """
    Plots the distribution of the sampled values for all
    reactions in a selected subsytem as a histogram and a
    normal distribution.

    Parameters
    ----------
    sampled_fluxes : pandas.Dataframe
        The calculated fluxes, output of sampling. For each reaction,
        n fluxes will be calculated (n = number of samples taken).
    reactions : list
        List of reactions, e.g. output of `get_subsytem_reactions()`.
    bins : int
        Number of bins used for the histogram. Defaults to 10.

    Returns
    -------
    fig : matplotlib.Figure
        Figure of sampled value distribution for one reaction.
    """
    rows = math.ceil(len(reactions) / 3)
    fig, ax = plt.subplots(figsize=(15, 5 * (rows / 2)))
    for i in range(0, len(reactions)):
        plt.subplot(rows, 3, i + 1)
        _subplot_sampled_reaction_fluxes(
            sampled_fluxes, reactions, reaction_id=i, bins=bins
        )
    plt.tight_layout()
    fig.text(
        0.5,
        -0.02,
        "Flux [mmol * gDCW$^{-1}$ * h$^{-1}$]",
        ha="center",
        fontsize=20,
    )
    fig.text(
        -0.02,
        0.5,
        "Distribution [%]",
        va="center",
        rotation="vertical",
        fontsize=20,
    )
    return fig


def show_subsystems(model):
    """
    Prints the names of all the subsystems in the model with
    their IDs.

    Parameters
    ----------
    model : cobra.Model
        Metabolic model.
    """
    subsystems = []
    for rxn in model.reactions:
        subsystem = rxn.subsystem
        if subsystem not in subsystems:
            subsystems.append(subsystem)
    for cnt, sub in enumerate(subsystems):
        print(f"{cnt}: {sub}")


def get_subsytem_reactions(model, subsystem_id):
    """
    Extracts the names of the reactions in a selected subsytem. Also
    outputs a list of all the subsytems in the model.

    Parameters
    ----------
    model : cobra.Model
        Metabolic model.
    subsystem_id : int
        ID of the subsystem the reactions should be extracted from.
        Can be selected after inspection using `show_subsystems()`.

    Returns
    -------
    reactions : list
        List of reactions in a selected subsytem.
    subsystems : list
        List of subsystems in a model. Input for `plot_subsystem_fluxes()`.
    """
    subsystems = []
    subsystems_reactions = {}
    for rxn in model.reactions:
        subsystem = rxn.subsystem
        if subsystem not in subsystems:
            subsystems.append(subsystem)
        subsystems_reactions[rxn.id] = subsystem
    reactions = [
        value[0]
        for value in subsystems_reactions.items()
        if value[1] == subsystems[subsystem_id]
    ]
    return reactions, subsystems


def _reduce_sampled_fluxes(sampled_fluxes, reactions):
    """
    Reduces the input dataframe of sampled fluxes to a subset of
    selected reactions.

    Parameters
    ----------
    sampled_fluxes : pandas.Dataframe
        The calculated fluxes, output of sampling. For each reaction,
        n fluxes will be calculated (n = number of samples taken).
    reactions : list
        List of reactions, e.g. output of `get_subsytem_reactions()`.

    Returns
    -------
    re_arranged_df : pandas.Dataframe
        Sampled fluxes reduced to a specified set of reactions.
    """
    reactions_mask = [
        True if col in reactions else False for col in sampled_fluxes.columns
    ]
    subsystem_df = sampled_fluxes[sampled_fluxes.columns[reactions_mask]]
    re_arranged_df = subsystem_df.stack().reset_index(
        level=[1], name="Sampled Fluxes"
    )
    re_arranged_df = re_arranged_df.rename(
        columns={"level_1": "Reaction"}
    ).reset_index(drop=True)
    return re_arranged_df


def plot_subsystem_fluxes(
    model, sampled_fluxes, subsystem_id, no_zero_cols=False
):
    """
    Visualizes the distribution of sampled fluxes in a selected
    subsytem.

    Parameters
    ----------
    model : cobra.Model
        Metabolic model.
    sampled_fluxes : pandas.Dataframe
        The calculated fluxes, output of sampling. For each reaction,
        n fluxes will be calculated (n = number of samples taken).
    subsystem_id : int
        ID of the subsystem the reactions should be extracted from.
        Can be selected after inspection using `show_subsystems()`.
    no_zero_cols : boolean
        Indicates if columns containing only 0s should be excluded.

    Returns
    -------
    fig : matplotlib.AxesSubplot
        Figure of sampled value distribution for one reaction.
    """
    if no_zero_cols:
        sampled_fluxes = sampled_fluxes.loc[
            :, (sampled_fluxes != 0).any(axis=0)
        ]
    reactions, subsystems = get_subsytem_reactions(model, subsystem_id)
    re_arranged_df = _reduce_sampled_fluxes(sampled_fluxes, reactions)
    fig = sns.boxplot(
        x="Reaction", y="Sampled Fluxes", data=re_arranged_df, orient="v"
    )
    plt.xticks(rotation=70)
    plt.title(subsystems[subsystem_id], size=20)
    return fig
