import unittest
import pandas as pd
import pickle
import pathlib
import BFAIR.exometabolomics as exometabolomics

current_dir = str(pathlib.Path(__file__).parent.absolute())


class test_methods(unittest.TestCase):

    # Create method to compare dataframes
    def assertDataframeEqual(self, a, b, msg):
        try:
            pd.testing.assert_frame_equal(a, b)
        except AssertionError as e:
            raise self.failureException(msg) from e

    def setUp(self):
        file_obj = open(
            current_dir
            + "/test_data/exometabolomics_Data/unittest_data/test_data.obj",
            "rb",
        )
        (
            feature_filename,
            df_conc,
            df_OD600,
            df_mu,
            df_OD,
            df_rates,
            df_results,
        ) = pickle.load(file_obj)
        file_obj.close()

        self.feature_filename = feature_filename
        self.df_conc = df_conc
        self.df_OD600 = df_OD600
        self.df_mu = df_mu
        self.df_OD = df_OD
        self.df_rates = df_rates
        self.df_results = df_results

        # Add the method to compare dataframes in the class
        self.addTypeEqualityFunc(pd.DataFrame, self.assertDataframeEqual)

    def test_get_filename(self):
        feature_filename = self.feature_filename
        df_sequence = pd.read_csv(
            current_dir + "/test_data/exometabolomics_Data/sequence_test.csv"
        )
        feature_filename_ = exometabolomics.get_filename(
            df_sequence.iloc[1, :]
        )
        self.assertEqual(feature_filename, feature_filename_)

    def test_extract_concentrations(self):
        df_conc = self.df_conc
        df_sequence = pd.read_csv(
            current_dir + "/test_data/exometabolomics_Data/sequence_test.csv"
        )
        feature_dir = current_dir + "/test_data/exometabolomics_Data/features"
        dil = 2
        df_conc_ = exometabolomics.extract_concentrations(
            df_sequence, feature_dir, dil
        )
        self.assertEqual(len(df_conc), len(df_conc_))
        self.assertEqual(len(df_conc.columns), len(df_conc_.columns))
        self.assertEqual(df_conc, df_conc_)

    def test_extract_OD600(self):
        df_OD600 = self.df_OD600
        df_DataSeries = pd.read_excel(
            current_dir + "/test_data/exometabolomics_Data/Data_series.xlsx",
            engine="openpyxl",
        )
        df_OD600_ = exometabolomics.extract_OD600(df_DataSeries)
        self.assertEqual(len(df_OD600), len(df_OD600_))
        self.assertEqual(len(df_OD600.columns), len(df_OD600_.columns))
        self.assertEqual(df_OD600, df_OD600_)

    def test_extract_muMax(self):
        df_mu = self.df_mu
        df_Annotations = pd.read_excel(
            current_dir + "/test_data/exometabolomics_Data/Annotations.xlsx",
            index_col=0,
            engine="openpyxl",
        )
        df_mu_ = exometabolomics.extract_muMax(df_Annotations)
        self.assertEqual(len(df_mu), len(df_mu_))
        self.assertEqual(len(df_mu.columns), len(df_mu_.columns))
        self.assertEqual(df_mu, df_mu_)

    def extract_growthData(self):
        df_OD = self.df_OD
        df_DataSeries = pd.read_excel(
            current_dir + "/test_data/exometabolomics_Data/Data_series.xlsx",
            engine="openpyxl",
        )
        df_Annotations = pd.read_excel(
            current_dir + "/test_data/exometabolomics_Data/Annotations.xlsx",
            index_col=0,
            engine="openpyxl",
        )
        df_OD_ = exometabolomics.extract_growthData(
            df_DataSeries, df_Annotations
        )
        self.assertEqual(len(df_OD), len(df_OD_))
        self.assertEqual(len(df_OD.columns), len(df_OD_.columns))
        self.assertEqual(df_OD, df_OD_)

    def test_calculate_rates(self):
        df_rates = self.df_rates
        df_data = pd.read_csv(
            current_dir + "/test_data/exometabolomics_Data/data_test.csv"
        )
        n_min = 4
        df_rates_ = exometabolomics.calculate_rates(df_data, n_min)
        self.assertEqual(len(df_rates), len(df_rates_))
        self.assertEqual(len(df_rates.columns), len(df_rates_.columns))
        self.assertEqual(df_rates, df_rates_)

    def calculate_mean(self):
        df_results = self.df_results
        df_rates = self.df_rates
        df_results_ = exometabolomics.calculate_mean(df_rates)
        self.assertEqual(len(df_results), len(df_results_))
        self.assertEqual(len(df_results.columns), len(df_results_.columns))
        self.assertEqual(df_results, df_results_)
