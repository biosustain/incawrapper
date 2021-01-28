"""Relaxation.

Includes function to relax the bounds of a constraint-based model with
thermodynamic information.
"""

import pandas as pd

from cobra.exceptions import Infeasible
from pytfa import ThermoModel

try:
    from gurobipy import Model as GRBModel
except ModuleNotFoundError:
    pass

from BFAIR.thermo.utils import get_dgo_bound_change


def _extract_bound_violations(grb_model, variables, negative_slack_prefix, positive_slack_prefix):
    # Extracts the magnitude of the bound violations on the relaxed Gurobi model
    epsilon = grb_model.Params.FeasibilityTol

    violations = []

    for var in variables:
        lb_change = -grb_model.getVarByName(negative_slack_prefix + var).X
        ub_change = grb_model.getVarByName(positive_slack_prefix + var).X

        if lb_change < -epsilon:
            violations.append((var, lb_change - epsilon, 0))
        elif ub_change > epsilon:
            violations.append((var, 0, ub_change + epsilon))

    return violations


def relax(tmodel: ThermoModel, reactions_to_relax, metabolites_to_relax, destructive=True):
    """
    Uses the Gurobi subroutines to relax the standard Gibbs free energy and log concentration bounds.

    Parameters
    ----------
    tmodel : pytfa.ThermoModel
        A cobra model with thermodynamics information.
    reactions_to_relax : list
        A list of reaction IDs whose standard Gibbs free energy bounds are allowed to be violated.
    metabolites_to_relax : list
        A list of metabolite IDs whose log concentration bounds are allowed to be violated.
    destructive : bool
        If True, apply bound changes to input model. If False, leave input model intact.

    Returns
    -------
    cons_table : pandas.DataFrame
        A 2-column table containing bound violation magnitudes of standard Gibbs free energy variables.
    vars_table : pandas.DataFrame
        A 2-column table containing bound violation magnitudes of log concentration variables.

    Raises
    ------
    ModuleNotFoundError
        If Gurobi is not the solver of the input model.
    Infeasible
        If the feasibility relaxation fails.
    """
    if tmodel.solver.interface.__name__ != "optlang.gurobi_interface":
        raise ModuleNotFoundError("Requires Gurobi.")

    # copy Gurobi model
    grb_model: GRBModel = tmodel.solver.problem.copy()

    relax_cons = [
        grb_model.getConstrByName(con.name) for con in tmodel.negative_delta_g if con.id in reactions_to_relax
    ]
    relax_vars = [
        grb_model.getVarByName(var.name) for var in tmodel.log_concentration if var.id in metabolites_to_relax
    ]
    cons_penalties = [1] * len(relax_cons)
    vars_penalties = [1] * len(relax_vars)

    # perform relaxation of variable bounds
    relax_obj = grb_model.feasRelax(
        relaxobjtype=0,
        minrelax=True,
        vars=relax_vars,
        lbpen=vars_penalties,
        ubpen=vars_penalties,
        constrs=relax_cons,
        rhspen=cons_penalties,
    )

    # check if relaxation was successful
    if relax_obj < 0:
        raise Infeasible("Failed to create the feasibility relaxation!")

    grb_model.optimize()

    # transfer/record the standard dG changes to the ThermoModel
    if relax_cons:
        rows = []
        violations = _extract_bound_violations(grb_model, tmodel.delta_gstd.list_attr("id"), "ArtN_G_", "ArtP_G_")
        for rxn_id, lb_change, ub_change in violations:
            if destructive:
                var = tmodel.delta_gstd.get_by_id(rxn_id).variable
                var.set_bounds(lb=var.lb + lb_change, ub=var.lb + ub_change)
            rows.append(
                {
                    "reaction": rxn_id,
                    "bound_change": lb_change + ub_change,
                    "subsystem": tmodel.reactions.get_by_id(rxn_id).subsystem,
                }
            )
        cons_table = pd.DataFrame.from_records(rows, index="reaction")
    else:
        cons_table = None

    # transfer/record the log concentration changes to the ThermoModel
    if relax_vars:
        rows = []
        violations = _extract_bound_violations(
            grb_model, tmodel.log_concentration.list_attr("id"), "ArtL_LC_", "ArtU_LC_"
        )
        for met_id, lb_change, ub_change in violations:
            if destructive:
                var = tmodel.log_concentration.get_by_id(met_id).variable
                var.set_bounds(lb=var.lb + lb_change, ub=var.lb + ub_change)
            rows.append(
                {
                    "metabolite": met_id,
                    "bound_change": lb_change + ub_change,
                    "compartment": tmodel.compartments[tmodel.metabolites.get_by_id(met_id).compartment]["name"],
                }
            )
        vars_table = pd.DataFrame.from_records(rows, index="metabolite")
    else:
        vars_table = None

    # solve relaxed model
    if destructive:
        tmodel.optimize()

    return cons_table, vars_table


def relax_dgo(tmodel: ThermoModel, reactions_to_ignore=[], destructive=True):
    """
    Uses the Gurobi subroutines to relax the standard Gibbs free energy bounds.

    Parameters
    ----------
    tmodel : pytfa.ThermoModel
        A cobra model with thermodynamics information.
    reactions_to_ignore : list
        A list of reaction IDs that will be ignored by the relaxation algorithm.
    destructive : bool
        If True, apply bound changes to input model. If False, leave input model intact.

    Returns
    -------
    relax_table : pandas.DataFrame
        A 2-column table containing bound violation magnitudes.

    Raises
    ------
    ModuleNotFoundError
        If Gurobi is not the solver of the input model.
    Infeasible
        If the feasibility relaxation fails.
    """
    reactions_to_relax = [con.id for con in tmodel.negative_delta_g if con.id not in reactions_to_ignore]
    metabolites_to_relax = []

    relax_table, _ = relax(tmodel, reactions_to_relax, metabolites_to_relax, destructive)

    return relax_table


def relax_lc(tmodel: ThermoModel, metabolites_to_ignore=[], destructive=True):
    """
    Uses the Gurobi subroutines to relax the log concentration bounds.

    Parameters
    ----------
    tmodel : pytfa.ThermoModel
        A cobra model with thermodynamics information.
    metabolites_to_ignore : list
        A list of metabolite IDs that will be ignored by the relaxation algorithm.
    destructive : bool
        If True, apply bound changes to input model. If False, leave input model intact.

    Returns
    -------
    relax_table : pandas.DataFrame
        A 2-column table containing bound violation magnitudes.

    Raises
    ------
    ModuleNotFoundError
        If Gurobi is not the solver of the input model.
    Infeasible
        If the feasibility relaxation fails.
    """
    reactions_to_relax = []
    metabolites_to_relax = [var.id for var in tmodel.log_concentration if var.id not in metabolites_to_ignore]

    _, relax_table = relax(tmodel, reactions_to_relax, metabolites_to_relax, destructive)

    return relax_table


def pytfa_relax_dgo(tmodel: ThermoModel, reactions_to_ignore=[]):
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

    Raises
    ------
    Infeasible
        If the feasibility relaxation fails.
    """
    from pytfa.optim.relaxation import relax_dgo

    relaxed_model, _, relax_table = relax_dgo(tmodel, reactions_to_ignore)
    if relax_table is None:
        raise Infeasible("Failed to create the feasibility relaxation!")
    relaxed_model.optimize()
    relax_table = get_dgo_bound_change(relaxed_model, relax_table)
    return relaxed_model, relax_table
