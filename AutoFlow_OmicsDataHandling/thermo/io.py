"""I/O.

This module hosts functions to load cobra models, create and adjust tFBA-ready
models.
"""

import os.path

from cobra.io import load_json_model
from pytfa import ThermoModel
from pytfa.io import (
    load_thermoDB,
    read_lexicon,
    read_compartment_data,
    annotate_from_lexicon,
    apply_compartment_data,
)

from AutoFlow_OmicsDataHandling.thermo import static


def _path(filename):
    # Returns the path to a file in the static folder
    return os.path.join(os.path.dirname(static.__file__), filename)


def load_cbm(model_name):
    """
    Load a JSON cobra model stored in the static folder.

    Parameters
    ----------
    model_name : str
        The name of the model.

    Returns
    -------
    cobra.Model
        The loaded cobra model.
    """
    return load_json_model(_path(model_name + ".json"))


def load_data(model_name):
    """
    Loads pre-curated model-specific thermodynamic information.

    Parameters
    ----------
    model_name : str
        The name of a model.

    Returns
    -------
    thermo_data : dict
        A thermodynamic database.
    lexicon : pandas.DataFrame
        A dataframe linking metabolite IDs to SEED compound IDs.
    compartment_data : dict
        A dictionary with information about each compartment of the model.
    """
    thermo_data = load_thermoDB(_path("thermo_data.thermodb"))
    lexicon = read_lexicon(_path(os.path.join(model_name, "lexicon.csv")))
    compartment_data = read_compartment_data(
        _path(os.path.join(model_name, "compartment_data.json"))
    )
    return thermo_data, lexicon, compartment_data


def create_model(model_name, thermo_data, lexicon, compartment_data) -> ThermoModel:
    """
    Creates a tFBA-ready model.

    Parameters
    ----------
    model_name : str
        The name of a model
    thermo_data : dict
        A thermodynamic database
    lexicon : pandas.DataFrame
        A dataframe linking metabolite IDs to SEED compound IDs
    compartment_data : dict
        A dictionary containing information about each compartment of the model

    Returns
    -------
    pytfa.ThermoModel : dict
        A thermodynamic database
    """
    model = load_cbm(model_name)
    tmodel = ThermoModel(thermo_data, model)
    tmodel.name = model_name

    annotate_from_lexicon(tmodel, lexicon)
    apply_compartment_data(tmodel, compartment_data)

    if tmodel.solver.interface.__name__ == "optlang.gurobi_interface":
        tmodel.solver.problem.Params.NumericFocus = 3
    tmodel.solver.configuration.tolerances.feasibility = 1e-9
    tmodel.solver.configuration.presolve = True

    tmodel.prepare()
    tmodel.convert(verbose=False)

    return tmodel


def adjust_model(tmodel: ThermoModel, rxn_bounds, lc_bounds):
    """
    Adjusts the flux bounds and log concentration of a tFBA-ready model.

    Parameters
    ----------
    tmodel : str
        A cobra model with thermodynamic information.
    rxn_bounds : pandas.DataFrame
        A 3-column table containing reaction IDs and flux bounds. The table
        must have the following columns: ``id``, ``lb``, and ``ub``.
    lc_bounds : pandas.DataFrame
        A 3-column table containing metabolite IDs and log concentration
        bounds. The table must have the following columns: ``id``, ``lb``,
        and ``ub``.
    """
    # constrain reactions (e.g., growth rate, uptake/secretion rates)
    for rxn_id, lb, ub in zip(rxn_bounds["id"], rxn_bounds["lb"], rxn_bounds["ub"]):
        if tmodel.reactions.has_id(rxn_id):
            tmodel.parent.reactions.get_by_id(rxn_id).bounds = lb, ub
            tmodel.reactions.get_by_id(rxn_id).bounds = lb, ub
    # constrain log concentrations
    for met, lb, ub in zip(lc_bounds["id"], lc_bounds["lb"], lc_bounds["ub"]):
        for compartment in tmodel.compartments:
            met_id = met + "_" + compartment
            if tmodel.log_concentration.has_id(met_id):
                (tmodel.log_concentration.get_by_id(met_id).variable.set_bounds(lb, ub))
