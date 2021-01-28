# generate test_data
# Last date : 26.01.2021
# By : Matthias Mattanovich (matmat@biosustain.dtu.dk)
# This script is intended to generate sample data and save them into the
# test_data file. The saved objects will then be used to test the
# normalization module using unit testing.
import pickle
import pandas as pd
import pathlib
import BFAIR.normalization as normalization

current_dir = str(pathlib.Path(__file__).parent.absolute())

pd.set_option("mode.chained_assignment", None)
# Use pickle to save python variables
filehandler = open("test_data.obj", "wb")

with open("Ecoli_intensities_linearity.txt", "rb") as handle:
    df = pickle.loads(handle.read())
# hardcoded for now, should be changed in future versions
# only valid for E. coli
biomass_mets = [
    "phe__L_c",
    "mlthf_c",
    "oaa_c",
    "lys__L_c",
    "atp_c",
    "ser__L_c",
    "g3p_c",
    "tyr__L_c",
    "pep_c",
    "met__L_c",
    "g6p_c",
    "akg_c",
    "glu__L_c",
    "gln__L_c",
    "r5p_c",
    "f6p_c",
    "pyr_c",
    "gly_c",
    "thr_c",
    "asp__L_c",
    "nadph_c",
    "cys__L_c",
    "3pg_c",
    "val__L_c",
    "ala__L_c",
    "ile__L_c",
    "asn__L_c",
    "his__L_c",
    "leu__L_c",
    "accoa_c",
    "arg__L_c",
    "pro__L_c",
    "trp__L_c",
    "nadh_c",
]
bm_vals = [
    0.176,
    0.443,
    0.34,
    0.326,
    33.247,
    0.205,
    0.129,
    0.131,
    0.051,
    0.146,
    0.205,
    0.087,
    0.25,
    0.25,
    0.754,
    0.071,
    0.083,
    0.582,
    0.241,
    0.229,
    5.363,
    0.087,
    0.619,
    0.402,
    0.488,
    0.276,
    0.229,
    0.09,
    0.428,
    2.51,
    0.281,
    0.21,
    0.054,
    -1.455,
]
biomass_value = 39.68
biomass_df = pd.DataFrame()
biomass_df["Metabolite"] = biomass_mets
biomass_df["Value"] = bm_vals
amino_acids = [
    "ala__L_c",
    "arg__L_c",
    "asn__L_c",
    "asp__L_c",
    "cys__L_c",
    "glu__L_c",
    "gln__L_c",
    "gly_c",
    "his__L_c",
    "ile__L_c",
    "leu__L_c",
    "lys__L_c",
    "met__L_c",
    "phe__L_c",
    "pro__L_c",
    "ser__L_c",
    "thr_c",
    "trp__L_c",
    "tyr__L_c",
    "val__L_c",
]


min_max = normalization.min_max_norm(
    df, columnname="Intensity", groupname_colname="sample_group_name"
)
tsi = normalization.tsi_norm(
    df, columnname="Intensity", groupname_colname="sample_group_name"
)
biomass_tsi = normalization.lim_tsi_norm(
    biomass_df['Metabolite'], df, columnname="Intensity"
)
biomass_formula_tsi = normalization.lim_tsi_norm(
    biomass_df,
    df,
    biomass_value=biomass_value,
    columnname="Intensity",
)
amino_acid_tsi = normalization.lim_tsi_norm(
    amino_acids, df, columnname="Intensity"
)
pqn = normalization.pqn_norm(
    df,
    groupname_colname="sample_group_name",
    value_colname="Intensity",
    corr_type="median",
    qc_vector=None,
)

pickle.dump(
    [
        df,
        biomass_df,
        biomass_value,
        amino_acids,
        min_max,
        tsi,
        biomass_tsi,
        biomass_formula_tsi,
        amino_acid_tsi,
        pqn,
    ],
    filehandler,
)

filehandler.close()
