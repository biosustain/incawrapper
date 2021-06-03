# generate test_data
# Last date : 27.05.2021
# By : Matthias Mattanovich (matmat@biosustain.dtu.dk)
# This script is intended to generate sample data and save them into the
# test_data file. The saved objects will then be used to test the
# MFA_visualization functions using unit testing.
import pickle
import pandas as pd
import pathlib
import cobra
from BFAIR.mfa.INCA import INCA_reimport
from BFAIR.mfa.sampling import (
    replace_biomass_rxn_name,
    add_constraints,
    bound_relaxation,
)
from BFAIR.mfa.visualization import (
    reshape_fluxes_escher,
    sampled_fluxes_minrange,
    show_reactions,
    get_subsytem_reactions,
    show_subsystems,
)

current_dir = str(pathlib.Path(__file__).parent.absolute())

pd.set_option("mode.chained_assignment", None)
# Use pickle to save python variables
filehandler = open("visualization_test_data.obj", "wb")

# prepare input data
model = cobra.io.load_json_model(
    current_dir + "/../MFA_modelInputsData/iJO1366.json")
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
fittedFluxes = replace_biomass_rxn_name(
    fittedFluxes,
    biomass_string='Biomass',
    biomass_rxn_name='BIOMASS_Ec_iJO1366_core_53p95M'
)
model = add_constraints(model, fittedFluxes)
bound_relaxation(
    model,
    fittedFluxes,
    destructive=True,
    fluxes_to_ignore=['BIOMASS_Ec_iJO1366_core_53p95M']
)
solution = model.optimize()
# Sample the relaxed model
relaxed_sampled_fluxes = cobra.sampling.sample(model, n=100)

# Generate comparison data
fluxes_relaxed = reshape_fluxes_escher(solution)
relaxed_fluxes_sampling = reshape_fluxes_escher(relaxed_sampled_fluxes)
reduced_relaxed_sampled_fluxes = sampled_fluxes_minrange(
    relaxed_sampled_fluxes, min_val=-1, max_val=1)
reactions, subsystems = get_subsytem_reactions(model, 14)
reactions_indeces = show_reactions(reactions)
subsystems_indices = show_subsystems(model)

pickle.dump(
    [
        solution,
        relaxed_sampled_fluxes,
        fluxes_relaxed,
        relaxed_fluxes_sampling,
        reduced_relaxed_sampled_fluxes,
        reactions,
        subsystems,
        reactions_indeces,
        subsystems_indices,
    ],
    filehandler,
)

filehandler.close()
