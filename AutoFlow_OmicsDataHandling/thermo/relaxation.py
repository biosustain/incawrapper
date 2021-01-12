"""Relaxation.

Includes function to relax the bounds of a constraint-based model with
thermodynamic information.
"""

import pandas as pd

from cobra.exceptions import Infeasible
from pytfa import ThermoModel
from pytfa.optim.relaxation import relax_dgo as relax_dgo_
from pytfa.utils.numerics import BIGM

try:
    from gurobipy import Model as GRBModel
except ModuleNotFoundError:
    pass

from AutoFlow_OmicsDataHandling.thermo.utils import get_dgo_bound_change


def relax_dgo(tmodel: ThermoModel, reactions_to_ignore=[]):
    """
    Uses the pytfa algorithm to relax the standard Gibbs free energy bounds.

    Parameters
    ----------
    tmodel : pytfa.ThermoModel
        A cobra model with thermodynamics information.
    reactions_to_ignore : list
        A list of reaction IDs that will be ignored by the relaxation
        algorithm.

    Returns
    -------
    relaxed_model : pytfa.ThermoModel
        The model with the relaxations applied to it.
    relax_table : pandas.DataFrame
        A 2-column table containing bound violation magnitudes.
    """
    relaxed_model, _, relax_table = relax_dgo_(tmodel, reactions_to_ignore)
    if relax_table is None:
        raise Infeasible("Failed to create the feasibility relaxation!")
    relaxed_model.optimize()
    relax_table = get_dgo_bound_change(relaxed_model, relax_table)
    return relaxed_model, relax_table


def relax_lc(tmodel: ThermoModel, metabolites_to_ignore=[], destructive=True):
    """
    Uses the Gurobi subroutines to relax the log concentration bounds.

    Parameters
    ----------
    tmodel : pytfa.ThermoModel
        A cobra model with thermodynamics information.
    metabolites_to_ignore : list
        A list of metabolite IDs that will be ignored by the relaxation
        algorithm.
    destructive : bool
        If True, apply bound changes to input model. If False, leave input
        model intact.

    Returns
    -------
    relax_table : pandas.DataFrame
        A 2-column table containing bound violation magnitudes.
    """
    if tmodel.solver.interface.__name__ != "optlang.gurobi_interface":
        raise ModuleNotFoundError("Requires Gurobi.")

    # copy Gurobi model
    grb_model: GRBModel = tmodel.solver.problem.copy()

    # get the Gurobi log concentration variables
    lc_vars = [
        grb_model.getVarByName(var.name)
        for var in tmodel.log_concentration
        if var.id not in metabolites_to_ignore
    ]
    vars_penalties = [1] * len(lc_vars)

    # perform relaxation of variable bounds
    relax_obj = grb_model.feasRelax(
        relaxobjtype=0,
        minrelax=True,
        vars=lc_vars,
        lbpen=vars_penalties,
        ubpen=vars_penalties,
        constrs=None,
        rhspen=None,
    )

    # check if relaxation was successful
    if relax_obj < 0:
        raise Infeasible("Failed to create the feasibility relaxation!")

    epsilon = tmodel.solver.configuration.tolerances.feasibility

    grb_model.optimize()

    # transfer the bound changes from Gurobi Model to ThermoModel
    rows = []
    metabolites = tmodel.log_concentration.list_attr("id")
    for met_id in metabolites:
        # get the auxiliary LB/UB change variables
        lb_change = -grb_model.getVarByName("ArtL_LC_" + met_id).X
        ub_change = grb_model.getVarByName("ArtU_LC_" + met_id).X

        # check if the auxiliary variables are not 0
        # (indicating a bound change)
        if lb_change < 0 or ub_change > 0:

            # set new bounds on the original log concentration variable
            if destructive:
                var = tmodel.log_concentration.get_by_id(met_id).variable
                var.set_bounds(
                    lb=max(-BIGM, min(BIGM, var.lb + lb_change - epsilon)),
                    ub=max(-BIGM, min(BIGM, var.ub + ub_change + epsilon)),
                )

            rows.append(
                {
                    "metabolite": met_id,
                    "bound_change": lb_change + ub_change,
                    "compartment": tmodel.compartments[
                        tmodel.metabolites.get_by_id(met_id).compartment
                    ]["name"],
                }
            )

    tmodel.optimize()

    # return table of relaxed variables
    return pd.DataFrame.from_records(rows, index="metabolite")
