import pandas as pd
import cobra


def reshape_fluxes_escher(sampled_fluxes):
    """
    Reshapes either a cobra solution object or a pandas
    Dataframe containing the sampled fluxes for a metabolic model
    so that they can be visualized in Escher. If a dataframe is
    provided, the mean of all the predictions from each reactions
    will be calculated.

    Parameters
    ----------
    sampled_fluxes : pandas.DataFrame or cobra.Solution
        Object containing reaction fluxes.

    Returns
    -------
    fluxes_escher : dict
        Input for Escher.

    Raises
    ------
    TypeError
        If the wrong type of input was provided.
    """
    fluxes_escher = {}
    if type(sampled_fluxes) is pd.core.frame.DataFrame:
        for col in sampled_fluxes.columns:
            fluxes_escher[col] = sampled_fluxes[col].mean()
    elif type(sampled_fluxes) is cobra.core.solution.Solution:
        reactions = list(sampled_fluxes.fluxes.index)
        for cnt, row in enumerate(sampled_fluxes.fluxes):
            fluxes_escher[reactions[cnt]] = row
    else:
        raise TypeError(
            f"The input is a '{type(sampled_fluxes)}', this type of object"
            " cannot be used here"
        )
    return fluxes_escher
