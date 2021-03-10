# generate test_data
# Last date : 03.03.2021
# By : Matthias Mattanovich (matmat@biosustain.dtu.dk)
# This script is intended to generate sample data and save them into the
# test_data file. The saved objects will then be used to test the
# FIA_MS_database_generation_tools using unit testing.
import pickle
import pandas as pd
import pathlib
import os
import cobra
import shutil
from cobra.core.formula import Formula
from BFAIR.FIA_MS.database_construction import (
    print_formula,
    zero_charge,
    is_valid,
    make_struct,
    make_mapping,
    store_struct,
    store_mapping,
    import_mapping_tsv,
    create_database,
)


current_dir = str(pathlib.Path(__file__).parent.absolute())

pd.set_option("mode.chained_assignment", None)
# Use pickle to save python variables
filehandler = open("test_data.obj", "wb")

# load data and assign variables needed for the functions
model_celegans = cobra.io.read_sbml_model(
    current_dir + "/../wormjam-20180125.sbml"
)
metabolites = model_celegans.metabolites
metabolite = metabolites[87]
formula = Formula(metabolite.formula)
elements = formula.elements

# run functions and produce output
formula_print = print_formula(elements)
formula_zero_charge = zero_charge(metabolite)
formulas = []
ids = []
for m in metabolites:
    if not is_valid(m):
        continue
    formula = zero_charge(m)
    formulas.append(str(formula))
    ids.append(m.id)
df_formulas = make_struct(formulas, ids)
df_mapping = make_mapping(df_formulas)

# create a temporary directory that will be deleted later
os.mkdir("temporary_files")

# save the output files into the temporary directory
store_struct(df_formulas, "test_store_struct", "temporary_files")
store_mapping(df_mapping, "test_store_mapping", "temporary_files")
create_database(metabolites, "test_create_database", "temporary_files")

# read the output files and save them to vaiables
store_struct_file = pd.read_csv(
    current_dir + "/temporary_files/test_store_struct_struct.tsv",
    sep="\t",
    header=None,
)
store_mapping_file1 = import_mapping_tsv(
    current_dir + "/temporary_files/test_store_mapping_mapping.tsv"
)
store_mapping_file2 = import_mapping_tsv(
    current_dir + "/temporary_files/test_store_mapping_mapping_csv.tsv"
)
create_database_struct_file = pd.read_csv(
    current_dir + "/temporary_files/test_create_database_struct.tsv",
    sep="\t",
    header=None,
)
create_database_mapping_file1 = import_mapping_tsv(
    current_dir + "/temporary_files/test_create_database_mapping.tsv"
)
create_database_mapping_file2 = import_mapping_tsv(
    current_dir + "/temporary_files/test_create_database_mapping_csv.tsv"
)

# delete the temporary directory and the included files
shutil.rmtree("temporary_files")

pickle.dump(
    [
        elements,
        formula_print,
        metabolite,
        formula_zero_charge,
        formulas,
        ids,
        df_formulas,
        df_mapping,
        metabolites,
        store_struct_file,
        store_mapping_file1,
        store_mapping_file2,
        create_database_struct_file,
        create_database_mapping_file1,
        create_database_mapping_file2,
    ],
    filehandler,
)

filehandler.close()
