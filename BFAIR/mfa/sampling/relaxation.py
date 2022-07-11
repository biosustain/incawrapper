from BFAIR.mfa.sampling.constraints import timer, _reshape_fluxes
import pandas as pd
import re
from cobra.exceptions import Infeasible

try:
    from gurobipy import Model as GRBModel
except ModuleNotFoundError:
    pass


@timer
def bound_relaxation(
    infeasible_model, fittedFluxes, destructive=True, fluxes_to_ignore=[]
):
    """
    Relaxation function for cobra metabolic models. By making use of the
    Gurobi solver, this functions figures out which bounds have to be
    relaxed by how much in order to make the model solution feasible.
    If `destructive=True`, then these changes are automatically applied.

    Parameters
    ----------
    infeasible_model : cobra.Model
        A metabolic model with constraints that lead to an infeasible
        solution.
    fittedFluxes : pandas.DataFrame
        Dataframe (reimported output of an INCA simulation)
        that contains the confidence intervals predicted for
        the model.
    destructive : bool
        Preset to `True`. If True, then the calculated fluxes will be
        applied to the model.
    fluxes_to_ignore : list
        A list of fluxes that should not be relaxed. Preset to `[]`.

    Returns
    -------
    cons_table : pandas.DataFrame
        A dataframe listing the reactions that have to be relaxed and
        the changes that need to be applied.

    Raises
    ------
    ModuleNotFoundError
        If Gurobi is not the solver of the input model.
    Infeasible
        If the feasibility relaxation fails.
    """
    model = infeasible_model
    if model.solver.interface.__name__ != "optlang.gurobi_interface":
        raise ModuleNotFoundError("Requires Gurobi solver.")

    # copy Gurobi model
    grb_model: GRBModel = model.solver.problem.copy()
    MFA_fluxes = _reshape_fluxes(fittedFluxes)
    reactions_to_relax = list(MFA_fluxes.keys())

    # remove fluxes to ignore
    if fluxes_to_ignore:
        for flux_to_ignore in fluxes_to_ignore:
            reactions_to_relax.remove(flux_to_ignore)

    # There are no metabolites to relax to we leave relax_cons empty
    relax_cons = []

    # Get forward and reverse reaction separately
    relax_vars = [
        grb_model.getVarByName(con.id)
        for con in model.reactions
        if con.id in reactions_to_relax
    ]
    relax_vars_reverse = [
        grb_model.getVarByName(con.reverse_id)
        for con in model.reactions
        if con.id in reactions_to_relax
    ]

    # Combine the lists
    relax_vars = relax_vars + relax_vars_reverse

    cons_penalties = relax_cons
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
    if relax_obj <= 0:
        raise Infeasible("Failed to create the feasibility relaxation!")
    grb_model.optimize()

    # transfer/record the lower/upper bound changes to the cobra model
    if relax_vars:
        variables = [var.VarName for var in relax_vars]
        rows = []
        violations = _extract_bound_violations(
            grb_model, variables, "ArtL_", "ArtU_"
        )
        for rxn_id, lb_change, ub_change in violations:
            try:
                subsystem = model.reactions.get_by_id(rxn_id).subsystem
            except KeyError:
                subsystem = model.reactions.get_by_id(
                    re.match(".+?(?=_reverse_)", rxn_id)[0]
                ).subsystem
            rows.append(
                {
                    "reaction": rxn_id,
                    "lb_change": lb_change,
                    "ub_change": ub_change,
                    "subsystem": subsystem,
                }
            )
            if destructive:
                if "_reverse_" in rxn_id:
                    # reverse reactions are only temporary for optimization,
                    # so we have to adjust the corresponding original reaction
                    rxn_id = re.match(".+?(?=_reverse_)", rxn_id)[0]
                    lb_change, ub_change = -ub_change, -lb_change
                lb = model.reactions.get_by_id(rxn_id).lower_bound
                ub = model.reactions.get_by_id(rxn_id).upper_bound
                model.reactions.get_by_id(rxn_id).lower_bound = lb + lb_change
                model.reactions.get_by_id(rxn_id).upper_bound = ub + ub_change

        cons_table = pd.DataFrame.from_records(rows, index="reaction")
    else:
        cons_table = None

    return cons_table


def _extract_bound_violations(
    grb_model, variables, negative_slack_prefix, positive_slack_prefix
):
    """
    Extracts the lower and upper bound changes that have to applied to
    the input model in order to make its solution feasible.
    """
    # Extracts the magnitude of the bound violations on the relaxed
    # Gurobi model
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
