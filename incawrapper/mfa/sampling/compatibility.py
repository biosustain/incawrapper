import re
import pandas as pd
from cobra import Reaction
import copy


def model_rxn_overlap(fittedFluxes, model):
    """
    Finds the overlapping reactions between a metabolic model
    that the calculated fluxes should be fit in to and the MFA
    output.

    Parameters
    ----------
    fittedFluxes : pandas.DataFrame
        Dataframe (reimported output of an INCA simulation)
        that contains the confidence intervals predicted for
        the model.
    model : cobra.Model
        Metabolic model.

    Returns
    -------
    overlapping reactions : pandas.Series
        Series of all the reactions found in both the model
        and the fitted fluxes.
    """
    model_rxns = []
    for rxn in model.reactions:
        model_rxns.append(rxn.id)
    INCA_rxns = fittedFluxes["rxn_id"]
    mask = []
    for rxn in INCA_rxns:
        if rxn in model_rxns:
            mask.append(False)
        else:
            mask.append(True)
    return INCA_rxns[mask]


def rxn_coverage(fittedFluxes, model):
    """
    Prints the percentage of how many of the reactions in the
    input fluxes are part of a given metabolic model.

    Parameters
    ----------
    fittedFluxes : pandas.DataFrame
        Dataframe (reimported output of an INCA simulation)
        that contains the confidence intervals predicted for
        the model.
    model : cobra.Model
        Metabolic model.
    """
    print(
        round(
            (len(model_rxn_overlap(fittedFluxes, model)) / len(fittedFluxes)),
            2,
        )
        * 100,
        "%",
    )


def split_lumped_rxns(lumped_rxns, fittedFluxes):
    """
    For data containing lumped reactions that are speparated
    by and underscore. This function separated the names and
    adds a new reaction to the dataframe that is a copy of
    the data of the lumped reaction.

    Parameters
    ----------
    lumped_rxns : pandas.Series or list
        Iterable element containing the names of the
        lumped reactions.
    fittedFluxes : pandas.DataFrame
        Dataframe (reimported output of an INCA simulation)
        that contains the confidence intervals predicted for
        the model.

    Returns
    -------
    fittedFluxes : pandas.DataFrame
        Updated version of the input, now with separated
        lumped reactions.
    """
    fittedFluxes = copy.deepcopy(fittedFluxes)
    for rxn in lumped_rxns:
        split_names = rxn.split("_")
        for index, split_name in enumerate(split_names):
            if index == 0:
                df_row_index = list(fittedFluxes["rxn_id"]).index(rxn)
                row = fittedFluxes.iloc[df_row_index]
                fittedFluxes.at[df_row_index, "rxn_id"] = split_name
                df_row_index = list(fittedFluxes["rxn_id"]).index(split_name)
            else:
                row = fittedFluxes.iloc[df_row_index]
                fittedFluxes = pd.concat([fittedFluxes, row], ignore_index=True)
                #fittedFluxes.append(row, ignore_index=True)
                fittedFluxes.at[len(fittedFluxes) - 1, "rxn_id"] = split_name
    return fittedFluxes


def split_lumped_reverse_rxns(lumped_reverse_rxns, fittedFluxes):
    """
    For data containing lumped reverse reactions that are
    speparated by and underscore. This function separated
    the names and adds a new reaction to the dataframe that
    is a copy of the data of the lumped reaction.

    Parameters
    ----------
    lumped_reverse_rxns : pandas.Series or list
        Iterable element containing the names of the
        lumped reverse reactions.
    fittedFluxes : pandas.DataFrame
        Dataframe (reimported output of an INCA simulation)
        that contains the confidence intervals predicted for
        the model.

    Returns
    -------
    fittedFluxes : pandas.DataFrame
        Updated version of the input, now with separated
        lumped reactions.
    """
    fittedFluxes = copy.deepcopy(fittedFluxes)
    for rxn in lumped_reverse_rxns:
        print(rxn)
        name = re.match(".+?(?=_reverse)", rxn)[0]
        split_names = name.split("_")
        for index, split_name in enumerate(split_names):
            if index == 0:
                df_row_index = list(fittedFluxes["rxn_id"]).index(rxn)
                row = fittedFluxes.iloc[df_row_index]
                fittedFluxes.at[df_row_index, "rxn_id"] = (
                    split_name + "_reverse"
                )
                df_row_index = list(fittedFluxes["rxn_id"]).index(
                    split_name + "_reverse"
                )
            else:
                row = fittedFluxes.iloc[df_row_index]
                fittedFluxes = pd.concat([fittedFluxes, row], ignore_index=True)
                #fittedFluxes.append(row, ignore_index=True)
                fittedFluxes.at[len(fittedFluxes) - 1, "rxn_id"] = (
                    split_name + "_reverse"
                )
    return fittedFluxes


def find_reverse_rxns(fittedFluxes):
    """
    Provides an overview over reverse- and their corresponding
    forward reactions.

    Parameters
    ----------
    fittedFluxes : pandas.DataFrame
        Dataframe (reimported output of an INCA simulation)
        that contains the confidence intervals predicted for
        the model.

    Returns
    -------
    reverse_rxns : pandas.DataFrame
        Names of reactions and their corresponding reverse
        reactions.
    """
    reverse_rxns = {}
    for cnt, rxn in enumerate(fittedFluxes["rxn_id"]):
        if "_reverse" in rxn:
            reverse_rxns[cnt] = {
                "forward": re.match(".+?(?=_reverse)", rxn)[0],
                "reverse": rxn,
            }
    reverse_rxns = pd.DataFrame.from_dict(reverse_rxns, "index")
    return reverse_rxns


def _overlaps(a, b):
    """
    Return the amount of overlap, between a and b.
    If >0, how much they overlap
    If 0,  they are book-ended
    If <0, distance

    Parameters
    ----------
    a, b : list
        lists of two numerals denoting the boarders of ranges.

    Returns
    -------
    overlap : float
        overlap as described above.

    """

    return min(a[1], b[1]) - max(a[0], b[0])


def combine_split_rxns(fittedFluxes):
    """
    Checks the flux bounds of forward and reverse rections.
    If they overlap, then they are are combined into one
    reaction with the bounds covering both forward and reverse.
    If the don't, then their names are noted in a list so
    they can be processed in a subsequent step.

    Parameters
    ----------
    fittedFluxes : pandas.DataFrame
        Dataframe (reimported output of an INCA simulation)
        that contains the confidence intervals predicted for
        the model.

    Returns
    -------
    fittedFluxes : pandas.DataFrame
        Updated version of the input, but overlapping
        forward and reverse reactions are joined.
    rxns_to_split : list
        Names of the reactions for which a corresponding
        reverse reaction should be added to the model.
    """
    fittedFluxes = copy.deepcopy(fittedFluxes)
    rxns_to_split = []
    reverse_rxns = find_reverse_rxns(fittedFluxes)
    for _, row in reverse_rxns.iterrows():
        fittedFluxes_forward = fittedFluxes[fittedFluxes["rxn_id"] == row[0]]
        forward_lb = fittedFluxes_forward["flux_lb"].values[0]
        forward_ub = fittedFluxes_forward["flux_ub"].values[0]
        forward = [forward_lb, forward_ub]
        fittedFluxes_reverse = fittedFluxes[fittedFluxes["rxn_id"] == row[1]]
        reverse_lb = fittedFluxes_reverse["flux_lb"].values[0]
        reverse_ub = fittedFluxes_reverse["flux_ub"].values[0]
        reverse = [-reverse_ub, -reverse_lb]
        if _overlaps(forward, reverse) == 0:
            fittedFluxes.at[
                fittedFluxes_forward.index[0], "flux_lb"
            ] = -fittedFluxes.at[fittedFluxes_reverse.index[0], "flux_ub"]
            fittedFluxes = fittedFluxes.drop(fittedFluxes_reverse.index[0])
        else:
            print("These reactions need to be split into two:", row[0])
            rxns_to_split.append(row[0])
    fittedFluxes = fittedFluxes.reset_index()
    return fittedFluxes, rxns_to_split


def cobra_add_split_rxns(rxns_to_split, model):
    """
    Adds inverse copies of the reactions that need a defined
    reverse reaction to the input model.

    Parameters
    ----------
    rxns_to_split : list
        Names of the reactions for which a corresponding
        reverse reaction should be added to the model.
    model : cobra.Model
        Metabolic model.
    """
    for i, rxn in enumerate(rxns_to_split):
        try:
            rxn_name = f"{rxn}_reverse"
            reaction = Reaction(rxn_name)
            reaction.name = model.reactions.get_by_id(rxn).name
            reaction.subsystem = model.reactions.get_by_id(rxn).subsystem
            reaction.lower_bound = 0.0  # This is the default
            reaction.upper_bound = 1000.0  # This is the default
            mets = [
                met.id for met in model.reactions.get_by_id(rxn).metabolites
            ]
            neg_coeff = [
                model.reactions.get_by_id(rxn).get_coefficient(met.id) * -1
                for met in model.reactions.get_by_id(rxn).metabolites
            ]
            model.add_reactions([reaction])
            model.reactions.get_by_id(rxn_name).add_metabolites(
                dict(zip(mets, neg_coeff))
            )

            genes = [g.id for g in model.reactions.get_by_id(rxn).genes]
            reaction_rule = "( "
            for gene_i, gene in enumerate(genes):
                if gene_i == 0:
                    reaction_rule += gene
                else:
                    reaction_rule += " or " + gene
            reaction_rule += " )"
            model.reactions.get_by_id(
                rxn_name
            ).gene_reaction_rule = reaction_rule
            print(f"- Added {rxn} to model")
        except KeyError:
            print(f"# Could not add {rxn} to model")
