# generate test_data
# Last date : 15.04.2021
# By : Annette Lien (annlien@dtu.dk)
# This script is intended to generate sample data and save them into the
# test_data file. The saved objects will then be used to test the
# exometabolomics tools using unit testing.
import pickle
import pandas as pd
import pathlib
import incawrapper.exometabolomics as exometabolomics

current_dir = str(pathlib.Path(__file__).parent.absolute())

pd.set_option("mode.chained_assignment", None)
# Use pickle to save python variables
filehandler = open("test_data.obj", "wb")

# load data and assign variables needed for the functions
feature_dir = current_dir + "/../features"
df_sequence = pd.read_csv(current_dir + "/../sequence_test.csv")
dil = 2
df_DataSeries = pd.read_excel(
    current_dir + "/../Data_series.xlsx", engine="openpyxl"
)
df_Annotations = pd.read_excel(
    current_dir + "/../Annotations.xlsx", index_col=0, engine="openpyxl"
)
df_data = pd.read_csv(current_dir + "/../data_test.csv")
n_min = 4


# get_filename
feature_filename = exometabolomics.get_filename(df_sequence.iloc[1, :])
# extract_concentrations
df_conc = exometabolomics.extract_concentrations(df_sequence, feature_dir, dil)
# extract_OD600
df_OD600 = exometabolomics.extract_OD600(df_DataSeries)
# extract_muMax
df_mu = exometabolomics.extract_muMax(df_Annotations)
# extract_growthData
df_OD = exometabolomics.extract_growthData(df_DataSeries, df_Annotations)
# calculate_rates
df_rates = exometabolomics.calculate_rates(df_data, n_min)
# calculate_mean
df_results = exometabolomics.calculate_mean(df_rates)


pickle.dump(
    [
        feature_filename,
        df_conc,
        df_OD600,
        df_mu,
        df_OD,
        df_rates,
        df_results,
    ],
    filehandler,
)

filehandler.close()
