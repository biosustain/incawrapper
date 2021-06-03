def get_observable_fluxes(fittedFluxes):
    """
    Checks which calculated fluxes qualify as being 'observable'
    (flux value at least 4 times the confidence interval and 0
    not included in the confidence interval).

    Parameters
    ----------
    fittedFluxes : pandas.DataFrame
        Dataframe (reimported output of an INCA simulation)
        that contains the confidence intervals predicted for
        the model.

    Returns
    -------
    observable_fluxes : pandas.DataFrame
        Input dataframe reduced to the fluxes that qualify as
        observable fluxes.
    """
    big_enough_fluxes = fittedFluxes[
        fittedFluxes["flux"]
        / (fittedFluxes["flux_ub"] - fittedFluxes["flux_lb"])
        >= 4
    ]
    lb_below_0 = big_enough_fluxes["flux_lb"] < 0
    ub_above_0 = 0 < big_enough_fluxes["flux_lb"]
    observable_fluxes = big_enough_fluxes[~(lb_below_0 & ub_above_0)]
    return observable_fluxes


def percent_observable_fluxes(fittedFluxes, as_num=False):
    """
    Calculates the percentage of how many of the fluxes in
    the input dataframe qualify as observable fluxes.

    Parameters
    ----------
    fittedFluxes : pandas.DataFrame
        Dataframe (reimported output of an INCA simulation)
        that contains the confidence intervals predicted for
        the model.

    Returns
    -------
    percentage of observable fluxes : string
        relative to total number of fluxes.
    """
    percent_float = (
        len(get_observable_fluxes(fittedFluxes)) / len(fittedFluxes)
    ) * 100
    if as_num:
        return percent_float
    else:
        return print(round(percent_float, 2), "%")


def get_flux_precision(fittedFluxes):
    """
    Calculates the mean standard deviation of the observable
    fluxes.

    Parameters
    ----------
    fittedFluxes : pandas.DataFrame
        Dataframe (reimported output of an INCA simulation)
        that contains the confidence intervals predicted for
        the model.

    Returns
    -------
    flux precision : float
        Mean of stdev of observable fluxes.
    """
    return get_observable_fluxes(fittedFluxes)["flux_stdev"].mean()
