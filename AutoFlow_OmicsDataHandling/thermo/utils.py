"""Utils.

Functions in this module ease the extraction of calculations from solved
models.
"""

import pandas as pd

from pytfa import ThermoModel
from pytfa.optim import DeltaG, LogConcentration


def _check_if_solved(tmodel: ThermoModel):
    # raises an exception if model has not been optimized
    if tmodel.solver.status is None:
        raise ValueError("Model must be solved first.")


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
                "flux": tmodel.variables[rxn.id].primal
                - tmodel.variables[rxn.reverse_id].primal,
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
        A 2-column table containing log concentrations and corresponding
        compartment.
    """
    _check_if_solved(tmodel)
    index = pd.Index(tmodel.log_concentration.list_attr("id"), name="metabolite")
    compartment = [
        tmodel.compartments[tmodel.metabolites.get_by_id(met_id).compartment]["name"]
        for met_id in index
    ]
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
        A relaxed cobra model with thermodynamics information
    relax_table : pandas.DataFrame
        The output table of `pytfa.relaxation.relax_dgo`

    Returns
    -------
    pandas.DataFrame
        A 2-column table containing relaxation magnitudes and corresponding
        subsystem
    """
    bound_change = relax_table["ub_change"] - relax_table["lb_change"]
    relax_table.index.name = "reaction"
    return pd.DataFrame(
        {
            "bound_change": bound_change.values,
            "subsystem": tmodel.reactions.query(
                lambda rxn_id: rxn_id in relax_table.index, "id"
            ).list_attr("subsystem"),
        },
        index=relax_table.index,
    )
