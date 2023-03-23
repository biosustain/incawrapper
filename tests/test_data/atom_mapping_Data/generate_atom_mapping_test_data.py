import pickle
import os
import pandas as pd
import pathlib
from incawrapper.mfa.INCA import INCA_input_parser
from incawrapper.atom_mapping import (MolfileDownloader,
                                write_rxn_files,
                                obtain_atom_mappings,
                                parse_reaction_mappings,
                                parse_metabolite_mappings,
                                generate_INCA_mapping_input,
                                clean_output,
                                )

original_wd = os.getcwd()
current_dir = str(pathlib.Path(__file__).parent.absolute())
os.chdir(current_dir)

# Load e_coli_core model
model, reaction_data, metabolite_data = INCA_input_parser.parse_cobra_model(
    'e_coli_core.json', 'e_coli_core', '2021-07-15')

# Subset handpicked reactions
model_reaction_df = pd.DataFrame()
model_reaction_df = model_reaction_df.append(
    reaction_data[reaction_data['rxn_id'] == 'PFK'])
model_reaction_df = model_reaction_df.append(
    reaction_data[reaction_data['rxn_id'] == 'BIOMASS_Ecoli_core_w_GAM'])
model_reaction_df = model_reaction_df.append(
    reaction_data[reaction_data['rxn_id'] == 'EX_pyr_e'])
model_reaction_df = model_reaction_df.append(
    reaction_data[reaction_data['rxn_id'] == 'ICL'])

# And metabolites from these reactions
model_metabolite_df = pd.DataFrame()
model_metabolite_df = model_metabolite_df.append(
    metabolite_data[metabolite_data['met_id'] == 'atp_c'])
model_metabolite_df = model_metabolite_df.append(
    metabolite_data[metabolite_data['met_id'] == 'f6p_c'])
model_metabolite_df = model_metabolite_df.append(
    metabolite_data[metabolite_data['met_id'] == 'adp_c'])
model_metabolite_df = model_metabolite_df.append(
    metabolite_data[metabolite_data['met_id'] == 'fdp_c'])
model_metabolite_df = model_metabolite_df.append(
    metabolite_data[metabolite_data['met_id'] == 'h_c'])
model_metabolite_df = model_metabolite_df.append(
    metabolite_data[metabolite_data['met_id'] == 'pyr_e'])
model_metabolite_df = model_metabolite_df.append(
    metabolite_data[metabolite_data['met_id'] == 'icit_c'])
model_metabolite_df = model_metabolite_df.append(
    metabolite_data[metabolite_data['met_id'] == 'succ_c'])
model_metabolite_df = model_metabolite_df.append(
    metabolite_data[metabolite_data['met_id'] == 'glx_c'])

# Obtain all required files
# Metabolite Molfiles
downloader = MolfileDownloader(model_metabolite_df)
downloader.generate_molfile_database()

# Rxn files
write_rxn_files(model_reaction_df)

# Mapped Rxn files
obtain_atom_mappings()

# Parsed dataframes of mappings
reaction_df = parse_reaction_mappings()
metabolite_df = parse_metabolite_mappings()

# CSV outputs of these dataframes
generate_INCA_mapping_input(reaction_df, metabolite_df)


# Load all the generated files in Python
# Molfiles in a single list.
# All numerics converted to floats.
metabolites = os.listdir('metabolites')
for i, molfile in enumerate(metabolites):
    with open(f'metabolites/{molfile}', 'r') as f:
        metabolites[i] = f.readlines()
        for j, met in enumerate(metabolites[i]):
            metabolites[i][j] = metabolites[i][j].split()
            for k, val in enumerate(metabolites[i][j]):
                try:
                    metabolites[i][j][k] = float(val)
                except BaseException:
                    pass

# Rxn files in a single list.
# All numerics converted to floats.
unmapped_rxns = os.listdir('unmappedRxns')
for i, rxn_file in enumerate(unmapped_rxns):
    with open(f'unmappedRxns/{rxn_file}', 'r') as f:
        unmapped_rxns[i] = f.readlines()
        for j, line in enumerate(unmapped_rxns[i]):
            unmapped_rxns[i][j] = unmapped_rxns[i][j].split()
            for k, val in enumerate(unmapped_rxns[i][j]):
                try:
                    unmapped_rxns[i][j][k] = float(val)
                except BaseException:
                    pass

# Mapped Rxn files in a single list
mapped_rxns = os.listdir('mappedRxns/rxnFiles')
for i, rxn_file in enumerate(mapped_rxns):
    with open(f'mappedRxns/rxnFiles/{rxn_file}', 'r') as f:
        lines = f.readlines()
        atom_rows = []
        for j, line in enumerate(lines):
            if len(line.split()) in (15, 16):
                # Only append rows containing atom mappings
                atom_rows.append(line.split())
        mapped_rxns[i] = atom_rows

# CSV outputs of parsed mapping data
reaction_df_csv = pd.read_csv('MappingReactions.csv')
metabolite_df_csv = pd.read_csv('MappingMetabolites.csv')

# Pickle all the variables using pickle
filehandler = open("test_data.obj", "wb")

pickle.dump(
    [
        metabolites,
        unmapped_rxns,
        mapped_rxns,
        reaction_df,
        metabolite_df,
        reaction_df_csv,
        metabolite_df_csv,
        model_reaction_df,
        model_metabolite_df,
    ],
    filehandler
)

filehandler.close()

clean_output()

os.chdir(original_wd)
