import unittest
import pandas as pd
import pickle
import pathlib
import BFAIR.FIA_MS as fia_ms  # noqa E402

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
            current_dir + "/test_data/FIA_MS_Data/unittest_data/test_data.obj",
            "rb",
        )
        (
            intensities_triplicates,
            stats_triplicates,
            intensities_single,
            stats_single,
            intensities_standard,
            stats_standard,
        ) = pickle.load(file_obj)
        file_obj.close()

        self.intensities_triplicates = intensities_triplicates
        self.stats_triplicates = stats_triplicates
        self.intensities_single = intensities_single
        self.stats_single = stats_single
        self.intensities_standard = intensities_standard
        self.stats_standard = stats_standard

        # Add the method to compare dataframes in the class
        self.addTypeEqualityFunc(pd.DataFrame, self.assertDataframeEqual)

    def test_extractNamesAndIntensities_triplicates(self):
        intensities_triplicates = self.intensities_triplicates
        feature_dir = (
            current_dir + "/test_data/FIA_MS_Data/features_AdditionalAdducts"
        )
        sequence_triplicates = pd.read_csv(
            current_dir + "/test_data/FIA_MS_Data/sequence_EColi.csv", sep=";"
        )
        sample_names_triplicates = sequence_triplicates[
            "sample_group_name"
        ].unique()
        database_triplicates = pd.read_csv(
            current_dir
            + "/test_data/FIA_MS_Data/CHEMISTRY/iJO1366_struct.tsv",
            sep="\t",
            header=None,
        )
        intensities_triplicates_ = fia_ms.extractNamesAndIntensities(
            feature_dir, sample_names_triplicates, database_triplicates
        )
        self.assertEqual(
            len(intensities_triplicates), len(intensities_triplicates_)
        )
        self.assertEqual(
            len(intensities_triplicates.columns),
            len(intensities_triplicates_.columns),
        )
        self.assertEqual(
            intensities_triplicates,
            intensities_triplicates_
        )

    def test_calculateMeanVarRSD_triplicates(self):
        stats_triplicates = self.stats_triplicates
        intensities_triplicates = self.intensities_triplicates
        sequence_triplicates = pd.read_csv(
            current_dir + "/test_data/FIA_MS_Data/sequence_EColi.csv", sep=";"
        )
        stats_triplicates_ = fia_ms.calculateMeanVarRSD(
            intensities_triplicates,
            sequence_triplicates.drop_duplicates(
                ["sample_group_name", "replicate_group_name"]
            ),
            min_reps=3,
        )
        self.assertEqual(len(stats_triplicates), len(stats_triplicates_))
        self.assertEqual(
            len(stats_triplicates.columns),
            len(stats_triplicates_.columns),
        )
        self.assertEqual(stats_triplicates, stats_triplicates_)

    def test_extractNamesAndIntensities_single(self):
        intensities_single = self.intensities_single
        feature_dir = (
            current_dir
            + "/test_data/FIA_MS_Data/features_AdditionalAdducts"
        )
        sequence_single = pd.read_csv(
            current_dir + "/test_data/FIA_MS_Data/sequence_HumanSerum.csv",
            sep=";"
        )
        sample_names_single = sequence_single["sample_group_name"].unique()
        database_single = pd.read_csv(
            current_dir + "/test_data/FIA_MS_Data/CHEMISTRY/HMDB_struct.tsv",
            sep="\t",
            header=None,
        )
        intensities_single_ = fia_ms.extractNamesAndIntensities(
            feature_dir, sample_names_single, database_single
        )
        self.assertEqual(len(intensities_single), len(intensities_single_))
        self.assertEqual(
            len(intensities_single.columns),
            len(intensities_single_.columns)
        )
        self.assertEqual(
            intensities_single,
            intensities_single_
        )

    def test_calculateMeanVarRSD_single(self):
        stats_single = self.stats_single
        intensities_single = self.intensities_single
        sequence_single = pd.read_csv(
            current_dir + "/test_data/FIA_MS_Data/sequence_HumanSerum.csv",
            sep=';'
        )
        stats_single_ = fia_ms.calculateMeanVarRSD(
            intensities_single,
            sequence_single.drop_duplicates(
                ["sample_group_name", "replicate_group_name"]
            ),
            min_reps=1,
        )
        self.assertEqual(len(stats_single), len(stats_single_))
        self.assertEqual(
            len(stats_single.columns),
            len(stats_single_.columns)
        )
        self.assertEqual(stats_single, stats_single_)

    def test_extractNamesAndIntensities_standard(self):
        intensities_standard = self.intensities_standard
        feature_dir = (
            current_dir
            + "/test_data/FIA_MS_Data/features_AdditionalAdducts"
        )
        sequence_standard = pd.read_csv(
            current_dir + "/test_data/FIA_MS_Data/sequence_Standards.csv",
            sep=";"
        )
        sample_names_standard = sequence_standard["sample_group_name"].unique()
        database_standard = pd.read_csv(
            current_dir
            + "/test_data/FIA_MS_Data/CHEMISTRY/standard_mix_struct.tsv",
            sep="\t",
            header=None,
        )
        intensities_standard_ = fia_ms.extractNamesAndIntensities(
            feature_dir, sample_names_standard, database_standard
        )
        self.assertEqual(len(intensities_standard), len(intensities_standard_))
        self.assertEqual(
            len(intensities_standard.columns),
            len(intensities_standard_.columns)
        )
        self.assertEqual(
            intensities_standard,
            intensities_standard_
        )

    def test_calculateMeanVarRSD_standard(self):
        stats_standard = self.stats_standard
        intensities_standard = self.intensities_standard
        sequence_standard = pd.read_csv(
            current_dir + "/test_data/FIA_MS_Data/sequence_Standards.csv",
            sep=';'
        )
        stats_standard_ = fia_ms.calculateMeanVarRSD(
            intensities_standard,
            sequence_standard.drop_duplicates(
                ["sample_group_name", "replicate_group_name"]
            ),
            min_reps=1,
        )
        self.assertEqual(len(stats_standard), len(stats_standard_))
        self.assertEqual(
            len(stats_standard.columns),
            len(stats_standard_.columns)
        )
        self.assertEqual(stats_standard, stats_standard_)
