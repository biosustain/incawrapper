import unittest
import pickle
import pathlib
import matplotlib
import pandas as pd
from BFAIR.mfa.utils import (
    calculate_split_ratio,
    plot_split_ratio,
    get_observable_fluxes,
    percent_observable_fluxes,
    get_flux_precision,
)

current_dir = str(pathlib.Path(__file__).parent.absolute())


class test_methods(unittest.TestCase):

    maxDiff = None

    # Create method to compare dataframes
    def assertDataframeEqual(self, a, b, msg):
        try:
            pd.testing.assert_frame_equal(a, b)
        except AssertionError as e:
            raise self.failureException(msg) from e

    def setUp(self):
        file_obj = open(
            current_dir
            + "/test_data/MFA_sampling/utils_test_data.obj",
            "rb",
        )
        (
            fittedFluxes,
            relaxed_sampled_fluxes,
            fig_split,
            split_ratio_df,
            fig_split_combined_influx,
            split_combined_influx_df,
            observable_fluxes,
            observable_fluxes_percentage,
            flux_precision,
        ) = pickle.load(file_obj)
        file_obj.close()

        self.fittedFluxes = fittedFluxes
        self.relaxed_sampled_fluxes = relaxed_sampled_fluxes
        self.fig_split = fig_split
        self.split_ratio_df = split_ratio_df
        self.fig_split_combined_influx = fig_split_combined_influx
        self.split_combined_influx_df = split_combined_influx_df
        self.observable_fluxes = observable_fluxes
        self.observable_fluxes_percentage = observable_fluxes_percentage
        self.flux_precision = flux_precision

        # Add the method to compare dataframes in the class
        self.addTypeEqualityFunc(pd.DataFrame, self.assertDataframeEqual)

    # Some of these methods produce figures
    # The logic behind the figures is also included in separate
    # related functions
    # That is why here I will only test for the output type

    def test_calculate_split_ratio(self):
        split_ratio_df_ = calculate_split_ratio(
            self.relaxed_sampled_fluxes,
            'EX_glc__D_e',
            'G6PDH2r',
            'PGI',
            branch_point_name="Glycolysis/PPP"
        )
        self.assertEqual(self.split_ratio_df, split_ratio_df_)

    def test_plot_split_ratio(self):
        fig_split_ = plot_split_ratio(
            self.relaxed_sampled_fluxes,
            'EX_glc__D_e',
            'G6PDH2r',
            'PGI',
            branch_point_name="Glycolysis/PPP"
        )
        self.assertEqual(type(self.fig_split), type(fig_split_))
        # matplotlib.axes._subplots.SubplotBase because it is
        # an inherited class
        self.assertIsInstance(
            fig_split_,
            matplotlib.axes._subplots.SubplotBase,
        )

    def test_get_observable_fluxes(self):
        observable_fluxes_ = get_observable_fluxes(self.fittedFluxes)
        self.assertEqual(self.observable_fluxes, observable_fluxes_)

    def test_percent_observable_fluxes(self):
        observable_fluxes_percentage_ = percent_observable_fluxes(
            self.fittedFluxes,
        )
        self.assertEqual(
            self.observable_fluxes_percentage,
            observable_fluxes_percentage_,
        )

    def test_get_flux_precision(self):
        flux_precision_ = get_flux_precision(self.fittedFluxes)
        self.assertEqual(self.flux_precision, flux_precision_)


if __name__ == "__main__":
    unittest.main()
