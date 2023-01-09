# %%
import pandas as pd
from BFAIR.parsers import modelReactions_file_parser, atomMapping_reactions2_file_parser, atom_mapping_metabolites_file_parser
import dotenv
import os

# set working directory
os.chdir(dotenv.find_dotenv().replace('.env', ''))

# %% [markdown]
# ## Required input
# - [x] atomMappingReactions: data_stage02_isotopomer_atomMappingReactions2.csv 
# - [x] modelReaction_data: data_stage02_isotopomer_modelReactions.csv
# - [x] atomMappingMetabolite: data_stage02_isotopomer_atomMappingMetabolites.csv
# - [ ] measuredFluxes: data_stage02_isotopomer_measuredFluxes.csv
# - [ ] experimentalMS_data: data-1604345289079.csv
# - [x] data_stage02_isotopomer_tracers
print(os.getcwd())
# %%
# setup the input and output files
filename_input = 'tests/test_data/simple_model/reactions.csv'
reaction_data = 'tests/test_data/simple_model/modelReactions.csv'
reaction_atom_mapping = 'tests/test_data/simple_model/atomMappingReaction2.csv'
metabolite_atom_mapping = 'tests/test_data/simple_model/atomMappingMetabolites.csv'

# make reactions mapping file
bfair_reactions_input = modelReactions_file_parser(filename_input, 'simple_model', 'reaction_id', 'reaction_equation')
bfair_reactions_input.to_csv(reaction_data, index=False)

# %%
atom_map_metabolites = atom_mapping_metabolites_file_parser(filename_input, 'simple_model', 'reaction_id', 'reaction_equation')
atom_map_metabolites.to_csv(metabolite_atom_mapping, index=False)


# %%
atomMapping_reactions2_file_parser(filename_input, 'simple_model', 'reaction_id', 'reaction_equation').to_csv(reaction_atom_mapping, index=False)
