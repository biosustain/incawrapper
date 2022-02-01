"""Utils.

Functions in this module ease the extraction of calculations from solved
models.
"""

__all__ = [
    "adjust_model",
    "get_flux",
    "get_log_concentration",
    "get_delta_g",
    "get_mass_action_ratio",
]

import numpy as np
import pandas as pd

from pytfa import ThermoModel
from pytfa.optim import DeltaG, LogConcentration


def _check_if_solved(tmodel: ThermoModel):
    # raises an exception if model has not been optimized
    if tmodel.solver.status is None:
        raise ValueError("Model must be solved first.")


def adjust_model(tmodel: ThermoModel, rxn_bounds, lc_bounds):
    """
    Adjusts the flux bounds and log concentration of a tFBA-ready model.

    Parameters
    ----------
    tmodel : str
        A cobra model with thermodynamic information.
    rxn_bounds : pandas.DataFrame
        A 3-column table containing reaction IDs and flux bounds. The table must have the following columns: ``id``,
        ``lb``, and ``ub``.
    lc_bounds : pandas.DataFrame
        A 3-column table containing metabolite IDs and log concentration bounds. The table must have the following
        columns: ``id``, ``lb``, and ``ub``.
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


def get_flux(tmodel: ThermoModel):
    """
    Returns calculated fluxes from a solved pytfa model.

    Parameters
    ----------
    tmodel : pytfa.ThermoModel
        A solved cobra model with thermodynamics information.

    Returns
    -------
    pandas.DataFrame
        A 2-column table containing fluxes and corresponding subsystem.
    """
    _check_if_solved(tmodel)

    index = pd.Index(tmodel.reactions.list_attr("id"), name="reaction")
    return pd.DataFrame(
        [
            {
                "flux": tmodel.variables[rxn.id].primal - tmodel.variables[rxn.reverse_id].primal,
                "subsystem": rxn.subsystem,
            }
            for rxn in tmodel.reactions
        ],
        index=index,
    )


def get_delta_g(tmodel: ThermoModel):
    """
    Returns calculated free energies from a solved pytfa model.

    Parameters
    ----------
    tmodel : pytfa.ThermoModel
        A solved cobra model with thermodynamics information.

    Returns
    -------
    pandas.DataFrame
        A 2-column table containing free energies and corresponding subsystem.
    """
    _check_if_solved(tmodel)

    index = pd.Index(tmodel.delta_g.list_attr("id"), name="reaction")
    subsystem = [tmodel.reactions.get_by_id(rxn_id).subsystem for rxn_id in index]
    return pd.DataFrame(
        {"delta_g": tmodel.get_primal(DeltaG).values, "subsystem": subsystem},
        index=index,
    )


def get_log_concentration(tmodel: ThermoModel):
    """
    Returns calculated log concentrations from a solved pytfa model.

    Parameters
    ----------
    tmodel : pytfa.ThermoModel
        A solved cobra model with thermodynamics information.

    Returns
    -------
    pandas.DataFrame
        A 2-column table containing log concentrations and corresponding compartment.
    """
    _check_if_solved(tmodel)

    index = pd.Index(tmodel.log_concentration.list_attr("id"), name="metabolite")
    compartment = [tmodel.compartments[tmodel.metabolites.get_by_id(met_id).compartment]["name"] for met_id in index]
    return pd.DataFrame(
        {
            "log_concentration": tmodel.get_primal(LogConcentration).values,
            "compartment": compartment,
        },
        index=index,
    )


def get_dgo_bound_change(tmodel: ThermoModel, relax_table):
    """
    Returns the magnitudes of bound relaxation of standard Gibbs free energy.

    Parameters
    ----------
    tmodel : pytfa.ThermoModel
        A relaxed cobra model with thermodynamics information.
    relax_table : pandas.DataFrame
        The output table of `pytfa.relaxation.relax_dgo`.

    Returns
    -------
    pandas.DataFrame
        A 2-column table containing relaxation magnitudes and corresponding subsystem.
    """
    bound_change = relax_table["ub_change"] - relax_table["lb_change"]
    relax_table.index.name = "reaction"
    return pd.DataFrame(
        {
            "bound_change": bound_change.values,
            "subsystem": tmodel.reactions.query(lambda rxn_id: rxn_id in relax_table.index, "id").list_attr(
                "subsystem"
            ),
        },
        index=relax_table.index,
    )


def get_mass_action_ratio(tmodel: ThermoModel):
    """
    Returns calculated mass action ratios from a solved pytfa model.

    Parameters
    ----------
    tmodel : pytfa.ThermoModel
        A solved cobra model with thermodynamics information.

    Returns
    -------
    pandas.DataFrame
        A 2-column table containing mass action ratios and corresponding subsystem.
    """
    _check_if_solved(tmodel)

    # exclude protons and water from mass action ratio calculation
    excl_metabolites = [f"{name}_{compartment}" for name in ["h", "h2o"] for compartment in tmodel.compartments]

    index = pd.Index(tmodel.delta_g.list_attr("id"), name="reaction")
    data = []
    for rxn_id in index:
        rxn = tmodel.reactions.get_by_id(rxn_id)
        # calculate ratio as product of each metabolite's concentration to the power of its coefficient
        ratio = np.prod(
            [
                np.exp(tmodel.log_concentration.get_by_id(met.id).variable.primal) ** coeff
                for met, coeff in rxn.metabolites.items()
                if met.id not in excl_metabolites
            ]
        )
        data.append((ratio, rxn.subsystem))
    return pd.DataFrame(data, index=index, columns=["mass_action_ratio", "subsystem"])
