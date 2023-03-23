import time
import functools


def timer(func):
    """
    Wrapper that reports how long it took to execute a function.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("--- start ---")
        start_time = time.time()
        output = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        min_, sec = divmod(round(elapsed_time), 60)
        hour, min_ = divmod(min_, 60)
        print(f"{func.__name__} takes {hour}h: {min_}min: {sec}sec to run")
        print("--- end ---")
        return output

    return wrapper


def _reshape_fluxes(fittedFluxes):
    """
    Reshaped the flux information from a dataframe to a dict to be used in
    constraint assigning functions.
    """
    MFA_flux_bounds = {}
    for i, rxn in fittedFluxes.iterrows():
        MFA_flux_bounds[rxn["rxn_id"]] = [rxn["flux_ub"], rxn["flux_lb"]]
    return MFA_flux_bounds


def _adjust_bounds(model, rxn, bounds):
    """
    Applied new bounds to specified reactions in a cobra model.
    """
    skip = False
    if bounds[0] < bounds[1]:  # to fix the issue with negaive values above
        try:
            model.reactions.get_by_id(rxn).lower_bound = round(bounds[0], 1)
            model.reactions.get_by_id(rxn).upper_bound = round(bounds[1], 1)
        except KeyError:
            print(f"Did not work for {rxn}")
            skip = True
    else:
        try:
            model.reactions.get_by_id(rxn).upper_bound = round(bounds[0], 1)
            model.reactions.get_by_id(rxn).lower_bound = round(bounds[1], 1)
        except KeyError:
            print(f"Did not work for {rxn}")
            skip = True
    return model, skip


def _restart_message(restart_counter):
    """
    Prints a message if `add_feasible_constraints()` had to restart.
    """
    extra_minus = "-" * len(str(restart_counter))
    print(f"--------------------------{extra_minus}")
    print(f"Total number of restarts: {restart_counter}")


@timer
def add_constraints(model_input, fittedFluxes):
    """
    Adds all the constraints defined in the input to a
    metabolic model.

    Parameters
    ----------
    model_input : cobra.Model
        Metabolic model.
    fittedFluxes : pandas.DataFrame
        Dataframe (reimported output of an INCA simulation)
        that contains the confidence intervals predicted for
        the model.

    Returns
    -------
    model : cobra.Model
        Metabolic model with adjusted constraints.
    """
    MFA_fluxes = _reshape_fluxes(fittedFluxes)
    model = model_input.copy()
    for rxn, bounds in MFA_fluxes.items():
        model, skip = _adjust_bounds(model, rxn, bounds)
    return model


@timer
def add_feasible_constraints(model_input, fittedFluxes, min_val=0):
    """
    Adds contraints to a metabolic model one by one; always checking
    that is still produces a feasible solution and that the predicted
    objective does not fall below a predefined value. If that were to
    happen, the function would restart but skip the reaction that
    caused the issue in the next iteration.

    Parameters
    ----------
    model_input : cobra.Model
        Metabolic model.
    fittedFluxes : pandas.DataFrame
        Dataframe (reimported output of an INCA simulation)
        that contains the confidence intervals predicted for
        the model.
    min_val : float
        Minimum allowed value for the optimized solution predicted for
        the objective. Preset to `0`.

    Returns
    -------
    model : cobra.Model
        Feasible metabolic model with added constraints.
    problems : list
        list of the reaction names of the reactions whose added
        constraints caused the model to fail the tests
        (feasibilty or minimum value).
    """
    no_restart = False
    problems = []
    restart_counter = 0
    MFA_fluxes = _reshape_fluxes(fittedFluxes)
    while no_restart is False:
        model = model_input.copy()
        for rxn, bounds in MFA_fluxes.items():
            if rxn in problems:
                continue
            model, skip = _adjust_bounds(model, rxn, bounds)
            if skip:
                continue
            solution_after_adj = model.optimize()
            if (
                solution_after_adj.objective_value is not None
                and solution_after_adj.objective_value >= min_val
            ):
                no_restart = True
            else:
                print(f"Solution infeasible if adding {rxn}")
                problems.append(rxn)
                no_restart = False
                restart_counter += 1
                break
    _restart_message(restart_counter)
    return model, problems
