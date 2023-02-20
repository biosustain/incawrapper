# generate test_data
# Last date : 09.12.2020
# By : Matthias Mattanovich (matmat@biosustain.dtu.dk)
# This script is intended to generate sample data and save them into the
# test_data file. The saved objects will then be used to test the
# INCAScript_generator using unit testing.
import pickle
import pandas as pd
from BFAIR.mfa.INCA import INCAScript


pd.set_option("mode.chained_assignment", None)
# Use pickle to save python variables
filehandler = open("test_data.obj", "wb")

INCAScript = INCAScript()

# measured fragments/MS data, tracers and measured fluxes should be limited to
# one experiment

atomMappingReactions_data_I = pd.read_csv(
    "data_stage02_isotopomer_atomMappingReactions2.csv"
)
modelReaction_data_I = pd.read_csv(
    "data_stage02_isotopomer_modelReactions.csv"
)
atomMappingMetabolite_data_I = pd.read_csv(
    "data_stage02_isotopomer_atomMappingMetabolites.csv"
)
measuredFluxes_data_I = pd.read_csv(
    "data_stage02_isotopomer_measuredFluxes.csv"
)
experimentalMS_data_I = pd.read_csv("Re-import/experimentalMS_data_I.csv")
tracer_I = pd.read_csv("data_stage02_isotopomer_tracers.csv")

# The files need to be limited by model id and mapping id, I picked
# "ecoli_RL2013_02" here
atomMappingReactions_data_I = INCAScript.limit_to_one_model(
    atomMappingReactions_data_I, "mapping_id", "ecoli_RL2013_02"
)
modelReaction_data_I = INCAScript.limit_to_one_model(
    modelReaction_data_I, "model_id", "ecoli_RL2013_02"
)
atomMappingMetabolite_data_I = INCAScript.limit_to_one_model(
    atomMappingMetabolite_data_I, "mapping_id", "ecoli_RL2013_02"
)
measuredFluxes_data_I = INCAScript.limit_to_one_model(
    measuredFluxes_data_I, "model_id", "ecoli_RL2013_02"
)

# Limiting fluxes, fragments and tracers to one experiment
measuredFluxes_data_I = INCAScript.limit_to_one_experiment(
    measuredFluxes_data_I, "experiment_id", "WTEColi_113C80_U13C20_01"
)
experimentalMS_data_I = INCAScript.limit_to_one_experiment(
    experimentalMS_data_I, "experiment_id", "WTEColi_113C80_U13C20_01"
)
tracer_I = INCAScript.limit_to_one_experiment(
    tracer_I, "experiment_id", "WTEColi_113C80_U13C20_01"
)

# Generate variables to save

initiated_MATLAB_script = INCAScript.initiate_MATLAB_script()
# the following function depends on prepare_input() and reaction_mapping()
model_reactions, model_rxn_ids = INCAScript.add_reactions_to_script(
    modelReaction_data_I, atomMappingReactions_data_I
)

initialized_model = INCAScript.initialize_model()

symmetrical_metabolites_script = INCAScript.symmetrical_metabolites(
    atomMappingMetabolite_data_I
)

# this one does not have an output in this set up, change for future version
unbalanced_reactions_script = INCAScript.unbalanced_reactions(
    atomMappingMetabolite_data_I,
)

reaction_parameters = INCAScript.add_reaction_parameters(
    modelReaction_data_I,
    measuredFluxes_data_I,
    model_rxn_ids,
    fluxes_present=True,
)

verify_and_estimate_script = INCAScript.verify_and_estimate()

(
    experimental_parameters,
    fragments_used,
) = INCAScript.add_experimental_parameters(
    experimentalMS_data_I,
    tracer_I,
    measuredFluxes_data_I,
    atomMappingMetabolite_data_I,
)

mapping_script = INCAScript.mapping(experimentalMS_data_I, fragments_used)

# Don't know how to test these two yet
# save_INCAScript(script, scriptname) don't know how to test that
# save_runner_script(runner, scriptname) SAME HERE

# run_INCA_in_MATLAB(INCA_base_directory, script_folder, matlab_script,
# runner_script) can't run MATLAB through CircleCI

script = INCAScript.script_generator(
    modelReaction_data_I,
    atomMappingReactions_data_I,
    atomMappingMetabolite_data_I,
    measuredFluxes_data_I,
    experimentalMS_data_I,
    tracer_I,
)
runner = INCAScript.runner_script_generator("TestFile", n_estimates=10)

pickle.dump(
    [
        modelReaction_data_I,
        atomMappingReactions_data_I,
        atomMappingMetabolite_data_I,
        measuredFluxes_data_I,
        experimentalMS_data_I,
        tracer_I,
        initiated_MATLAB_script,
        model_reactions,
        model_rxn_ids,
        initialized_model,
        symmetrical_metabolites_script,
        unbalanced_reactions_script,
        reaction_parameters,
        verify_and_estimate_script,
        experimental_parameters,
        fragments_used,
        mapping_script,
        script,
        runner,
    ],
    filehandler,
)

filehandler.close()
