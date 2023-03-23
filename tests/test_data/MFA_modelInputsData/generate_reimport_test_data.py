# generate test_data
# Last date : 12.02.2021
# By : Matthias Mattanovich (matmat@biosustain.dtu.dk)
# This script is intended to generate sample data and save them into the
# test_data file. The saved objects will then be used to test the
# INCA_reimport using unit testing.
import pickle
import pandas as pd

# import pathlib
# import os
from incawrapper.core import INCA_reimport


pd.set_option("mode.chained_assignment", None)
# Use pickle to save python variables
filehandler = open("reimport_test_data.obj", "wb")

# INCA_reimport_directly = INCA_reimport()
INCA_reimport = INCA_reimport()

# Load the data
filename = "TestFile.mat"
simulation_info = pd.read_csv("Re-import/experimentalMS_data_I.csv")
simulation_id = "WTEColi_113C80_U13C20_01"


# Generate variables to save
# Succession of functions
info = INCA_reimport.extract_file_info(filename)
parallel, non_stationary = INCA_reimport.det_simulation_type(simulation_info)
m, f = INCA_reimport.data_extraction(filename)
model_info = INCA_reimport.extract_model_info(m)
simulationParameters = INCA_reimport.extract_sim_params(
    simulation_id, info, m, filename
)
fittedData = INCA_reimport.extract_base_stats(f, simulation_id, info)
f_mnt_info = INCA_reimport.get_fit_info(f)
fittedMeasuredFluxes, fittedMeasuredFragments = INCA_reimport.sort_fit_info(
    f_mnt_info, simulation_info, fittedData
)
f_mnt_res_info = INCA_reimport.get_residuals_info(f, simulation_info)
(
    fittedMeasuredFluxResiduals,
    fittedMeasuredFragmentResiduals,
) = INCA_reimport.sort_residual_info(
    f_mnt_res_info, simulation_info, fittedData
)
f_par_info = INCA_reimport.get_fitted_parameters(f, simulation_info)
fittedFluxes, fittedFragments = INCA_reimport.sort_parameter_info(
    f_par_info, simulation_info, fittedData
)

# (fittedData2, fittedFluxes2, fittedFragments2, fittedMeasuredFluxes2,
#     fittedMeasuredFragments2, fittedMeasuredFluxResiduals2,
#     fittedMeasuredFragmentResiduals2, simulationParameters2) = \
#     INCA_reimport_directly.reimport(filename, simulation_info, simulation_id)

pickle.dump(
    [
        filename,
        simulation_info,
        simulation_id,
        info,
        parallel,
        non_stationary,
        m,
        f,
        model_info,
        f_mnt_info,
        f_mnt_res_info,
        f_par_info,
        fittedData,
        fittedFluxes,
        fittedFragments,
        fittedMeasuredFluxes,
        fittedMeasuredFragments,
        fittedMeasuredFluxResiduals,
        fittedMeasuredFragmentResiduals,
        simulationParameters,
        # fittedData2,
        # fittedFluxes2,
        # fittedFragments2,
        # fittedMeasuredFluxes2,
        # fittedMeasuredFragments2,
        # fittedMeasuredFluxResiduals2,
        # fittedMeasuredFragmentResiduals2,
        # simulationParameters2
    ],
    filehandler,
)

filehandler.close()
