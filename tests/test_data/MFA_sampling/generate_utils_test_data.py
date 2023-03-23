# generate test_data
# Last date : 27.05.2021
# By : Matthias Mattanovich (matmat@biosustain.dtu.dk)
# This script is intended to generate sample data and save them into the
# test_data file. The saved objects will then be used to test the
# MFA_utils functions using unit testing.
import pickle
import pandas as pd
import pathlib
import cobra
from incawrapper.core import INCA_reimport
from incawrapper.mfa.sampling import (
    replace_biomass_rxn_name,
    add_constraints,
    bound_relaxation,
)
from incawrapper.mfa.utils import (
    calculate_split_ratio,
    plot_split_ratio,
    get_observable_fluxes,
    percent_observable_fluxes,
    get_flux_precision,
)

current_dir = str(pathlib.Path(__file__).parent.absolute())

pd.set_option("mode.chained_assignment", None)
# Use pickle to save python variables
filehandler = open("utils_test_data.obj", "wb")

# Get the necessary input from other modules
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
model.optimize()
# Sample the relaxed model
relaxed_sampled_fluxes = cobra.sampling.sample(model, n=100)

# Caluclate the output of the custom functions
fig_split = plot_split_ratio(
    relaxed_sampled_fluxes,
    'EX_glc__D_e',
    'G6PDH2r',
    'PGI',
    branch_point_name="Glycolysis/PPP"
)
split_ratio_df = calculate_split_ratio(
    relaxed_sampled_fluxes,
    'EX_glc__D_e',
    'G6PDH2r',
    'PGI',
    branch_point_name="Glycolysis/PPP"
)
glycolysis = (
    abs(relaxed_sampled_fluxes['ACALD'])
    + abs(relaxed_sampled_fluxes['PFL'])
    + abs(relaxed_sampled_fluxes['PDH'])
)
glycolysis.name = 'Glycolysis'
fig_split_combined_influx = plot_split_ratio(
    relaxed_sampled_fluxes,
    glycolysis,
    'PTAr',
    'CS',
    branch_point_name="TCA/acetate secretion"
)
split_combined_influx_df = calculate_split_ratio(
    relaxed_sampled_fluxes,
    glycolysis,
    'PTAr',
    'CS',
    branch_point_name="TCA/acetate secretion"
)
observable_fluxes = get_observable_fluxes(fittedFluxes)
observable_fluxes_percentage = percent_observable_fluxes(fittedFluxes)
flux_precision = get_flux_precision(fittedFluxes)

pickle.dump(
    [
        fittedFluxes,
        relaxed_sampled_fluxes,
        fig_split,
        split_ratio_df,
        fig_split_combined_influx,
        split_combined_influx_df,
        observable_fluxes,
        observable_fluxes_percentage,
        flux_precision,
    ],
    filehandler,
)

filehandler.close()
