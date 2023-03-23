# generate test_data
# Last date : 27.05.2021
# By : Matthias Mattanovich (matmat@biosustain.dtu.dk)
# This script is intended to generate sample data and save them into the
# test_data file. The saved objects will then be used to test the
# MFA_sampling functions using unit testing.
import pickle
import pandas as pd
import pathlib
import cobra
from incawrapper.mfa.INCA import INCA_reimport
from incawrapper.mfa.sampling import (
    rxn_coverage,
    split_lumped_rxns,
    split_lumped_reverse_rxns,
    find_reverse_rxns,
    combine_split_rxns,
    cobra_add_split_rxns,
    model_rxn_overlap,
    add_constraints,
    add_feasible_constraints,
    find_biomass_reaction,
    get_min_solution_val,
    replace_biomass_rxn_name,
    bound_relaxation,
)

current_dir = str(pathlib.Path(__file__).parent.absolute())

pd.set_option("mode.chained_assignment", None)
# Use pickle to save python variables
filehandler = open("sampling_test_data.obj", "wb")


def get_bounds_df(model):
    # Helper function to have a way to compare the bounds
    bounds_temp = {}
    # Round to 5 decimal places to avoid issues in very low values
    for cnt, rxn in enumerate(model.reactions):
        bounds_temp[cnt] = {
            "rxn_id": rxn.id,
            "lb": rxn.lower_bound,
            "ub": rxn.upper_bound,
        }
    return pd.DataFrame.from_dict(bounds_temp, "index")


# Re-import the MFA data
filename = current_dir + "/../MFA_modelInputsData/TestFile.mat"
simulation_info = pd.read_csv(
    current_dir + "/../MFA_modelInputsData/experimentalMS_data_I.csv")
simulation_id = "WTEColi_113C80_U13C20_01"
reimport_data = INCA_reimport()
(
    fittedData,
    fittedFluxes,
    fittedFragments,
    fittedMeasuredFluxes,
    fittedMeasuredFragments,
    fittedMeasuredFluxResiduals,
    fittedMeasuredFragmentResiduals,
    simulationParameters,
) = reimport_data.reimport(filename, simulation_info, simulation_id)
# Import the conbra model
model = cobra.io.load_json_model(
    current_dir + "/../MFA_modelInputsData/iJO1366.json")
unconstraint_bounds = get_bounds_df(model)
# Copy the model in order to re-use it a few times
biomass_rxn = find_biomass_reaction(
    model, biomass_string=["Biomass", "BIOMASS", "biomass"]
)
adj_fittedFluxes = replace_biomass_rxn_name(
    fittedFluxes,
    biomass_rxn_name=biomass_rxn[1],
    biomass_string="Biomass",
)
model_preproces = model.copy()
# Pre-process the model and re-imported data
coverage = rxn_coverage(adj_fittedFluxes, model_preproces)
# Check the example notebook for details
lumped_ids = [1, 21, 26, 27, 53, 54, 67, 74, 82]
mask = []
overlap = model_rxn_overlap(adj_fittedFluxes, model_preproces)
for i in overlap.iteritems():
    if i[0] in lumped_ids:
        mask.append(True)
    else:
        mask.append(False)
lumped_rxns = model_rxn_overlap(adj_fittedFluxes, model_preproces)[mask]
fittedFluxes_split_temp = split_lumped_rxns(lumped_rxns, adj_fittedFluxes)
lumped_reverse_ids = [2, 28, 55, 68]
mask_reverse = []
for i in model_rxn_overlap(
        fittedFluxes_split_temp, model_preproces).iteritems():
    if i[0] in lumped_reverse_ids:
        mask_reverse.append(True)
    else:
        mask_reverse.append(False)
lumped_reverse_rxns = model_rxn_overlap(
    fittedFluxes_split_temp, model_preproces)[mask_reverse]
fittedFluxes_split = split_lumped_reverse_rxns(
    lumped_reverse_rxns, fittedFluxes_split_temp)
reverse_df = find_reverse_rxns(fittedFluxes_split)
fittedFluxes_split_combined, rxns_to_split = combine_split_rxns(
    fittedFluxes_split)
cobra_add_split_rxns(rxns_to_split, model_preproces)
model_preproces_bounds = get_bounds_df(model_preproces)
# Get info about the model and the biomass reactions
model_input = model.copy()
constrained_model = add_constraints(model_input, adj_fittedFluxes)
constrained_bounds = get_bounds_df(constrained_model)
min_val = get_min_solution_val(adj_fittedFluxes, biomass_string="BIOMASS")
# Only add the constraints that keep the model in the expected range
model_input = model.copy()
feasible_constrained_model, problems = add_feasible_constraints(
    model_input, adj_fittedFluxes, min_val=min_val,
)
feasible_constrained_bounds = get_bounds_df(feasible_constrained_model)
# Produce relaxation data
infeasible_model = constrained_model.copy()
cons_table = bound_relaxation(
    infeasible_model,
    adj_fittedFluxes,
    destructive=True,
    fluxes_to_ignore=[],
)
relaxed_bounds = get_bounds_df(infeasible_model)

pickle.dump(
    [
        fittedFluxes,
        unconstraint_bounds,
        biomass_rxn,
        adj_fittedFluxes,
        coverage,
        lumped_rxns,
        overlap,
        fittedFluxes_split_temp,
        lumped_reverse_rxns,
        reverse_df,
        fittedFluxes_split,
        fittedFluxes_split_combined,
        rxns_to_split,
        model_preproces_bounds,
        constrained_bounds,
        min_val,
        adj_fittedFluxes,
        problems,
        feasible_constrained_bounds,
        cons_table,
        relaxed_bounds,
    ],
    filehandler,
)

filehandler.close()
