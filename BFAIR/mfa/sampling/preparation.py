import copy


def find_biomass_reaction(
    model, biomass_string=["Biomass", "BIOMASS", "biomass"]
):
    """
    Identifies the biomass reaction(s) in a metabolic model.

    Parameters
    ----------
    model : cobra.Model
        Metabolic model.
    biomass_string : str or list
        String denoting at least a part of the name of the
        biomass function of the metabolic model or a list
        containing multiple possibilities to be tested.
        Preset to `["Biomass", "BIOMASS", "biomass"]`.

    Returns
    -------
    biomass_reaction_ids : list
        Reaction(s) containing the input string.
    """
    if isinstance(biomass_string, list):
        biomass = biomass_string
    else:
        biomass = list(biomass_string)
    biomass_reaction_ids = []
    for reaction in model.reactions:
        for biomass_spelling in biomass:
            if biomass_spelling in reaction.id:
                biomass_reaction_ids.append(reaction.id)
    return biomass_reaction_ids


def get_min_solution_val(fittedFluxes, biomass_string="Biomass"):
    """
    Finds the value calculated for the biomass function in the
    MFA simulation. This value can be seen as the minimum predicted
    growth rate in subsequent simulations.

    Parameters
    ----------
    fittedFluxes : pandas.DataFrame
        Dataframe (reimported output of an INCA simulation)
        that contains the confidence intervals predicted for
        the model.
    biomass_string : str
        String denoting at least a part of the name of the
        biomass function in the `fittedFluxes` DataFrame.
        Preset to `"Biomass"`.

    Returns
    -------
    min_val : float
        Value calculated for the biomass function in the INCA
        simulation.
    """
    min_val = 0
    for cnt, name in enumerate(fittedFluxes["rxn_id"]):
        if biomass_string in name:
            min_val = fittedFluxes.at[cnt, "flux"]
    return min_val


def replace_biomass_rxn_name(
    fittedFluxes,
    biomass_rxn_name,
    biomass_string="Biomass",
):
    """
    Replaces the biomass function name in the INCA simulation results
    with the biomass funciton name in the metabolic model. This is
    only relevent if a different model was used as a basis for the
    MFA simulation.

    Parameters
    ----------
    fittedFluxes : pandas.DataFrame
        Dataframe (reimported output of an INCA simulation)
        that contains the confidence intervals predicted for
        the model.
    biomass_rxn_name : str
        Name of the biomass reaction in the metabolic model;
        the name that should be assigned to the biomass function in
        `fittedFluxes`.
    biomass_string : str
        String denoting at least a part of the name of the
        biomass function in the `fittedFluxes` dataframe.
        Preset to `"Biomass"`.

    Returns
    -------
    fittedFluxes : pandas.DataFrame
        Dataframe (reimported output of an INCA simulation)
        that contains the confidence intervals predicted for
        the model. Now with same the biomass function name as in
        the metabolic model.
    """
    fittedFluxes_out = copy.deepcopy(fittedFluxes)
    for cnt, name in enumerate(fittedFluxes_out["rxn_id"]):
        if biomass_string in name:
            fittedFluxes_out.at[cnt, "rxn_id"] = biomass_rxn_name
    return fittedFluxes_out
