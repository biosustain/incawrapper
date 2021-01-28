import unittest
import pickle
import pathlib
import pandas as pd
import BFAIR.normalization as normalization

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
            current_dir + "/test_data/normalization_Data/test_data.obj", "rb"
        )
        (
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
        ) = pickle.load(file_obj)
        file_obj.close()

        self.df = df
        self.biomass_df = biomass_df
        self.biomass_value = biomass_value
        self.amino_acids = amino_acids
        self.min_max = min_max
        self.tsi = tsi
        self.biomass_tsi = biomass_tsi
        self.biomass_formula_tsi = biomass_formula_tsi
        self.amino_acid_tsi = amino_acid_tsi
        self.pqn = pqn

        # Add the method to compare dataframes in the class
        self.addTypeEqualityFunc(pd.DataFrame, self.assertDataframeEqual)

    def test_min_max(self):
        min_max = self.min_max
        df = self.df
        min_max_ = normalization.min_max_norm(
            df, columnname="Intensity", groupname_colname="sample_group_name"
        )
        self.assertEqual(min_max, min_max_)

    def test_tsi(self):
        tsi = self.tsi
        df = self.df
        tsi_ = normalization.tsi_norm(
            df, columnname="Intensity", groupname_colname="sample_group_name"
        )
        self.assertEqual(tsi, tsi_)

    def test_tsi_logic(self):
        df = self.df
        tsi_ = normalization.tsi_norm(
            df, columnname="Intensity", groupname_colname="sample_group_name"
        )
        num_samples = len(tsi_["sample_group_name"].unique())
        sum_samples = sum(tsi_["Intensity"])
        self.assertAlmostEqual(sum_samples, num_samples)

    def test_biomass_tsi(self):
        biomass_tsi = self.biomass_tsi
        biomass_df = self.biomass_df
        df = self.df
        biomass_tsi_ = normalization.lim_tsi_norm(
            biomass_df['Metabolite'],
            df,
            columnname="Intensity",
            groupname_colname="sample_group_name",
        )
        self.assertEqual(biomass_tsi, biomass_tsi_)

    def test_biomass_formula_tsi(self):
        biomass_formula_tsi = self.biomass_formula_tsi
        biomass_df = self.biomass_df
        biomass_value = self.biomass_value
        df = self.df
        biomass_formula_tsi_ = normalization.lim_tsi_norm(
            biomass_df,
            df,
            biomass_value=biomass_value,
            columnname="Intensity",
            groupname_colname="sample_group_name",
        )
        self.assertEqual(biomass_formula_tsi, biomass_formula_tsi_)

    def test_amino_acid_tsi(self):
        amino_acid_tsi = self.amino_acid_tsi
        amino_acids = self.amino_acids
        df = self.df
        amino_acid_tsi_ = normalization.lim_tsi_norm(
            amino_acids,
            df,
            columnname="Intensity",
            groupname_colname="sample_group_name",
        )
        self.assertEqual(amino_acid_tsi, amino_acid_tsi_)

    def test_pqn(self):
        pqn = self.pqn
        df = self.df
        pqn_ = normalization.pqn_norm(
            df,
            groupname_colname="sample_group_name",
            value_colname="Intensity",
            corr_type="median",
            qc_vector=None,
        )
        self.assertEqual(pqn, pqn_)
