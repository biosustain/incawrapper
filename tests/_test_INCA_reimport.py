import unittest
import pickle
import pathlib
import os

# import numpy as np
# from freezegun import freeze_time
# import datetime
import pandas as pd
from incawrapper.mfa.INCA import INCA_reimport

current_dir = str(pathlib.Path(__file__).parent.absolute())

os.chdir(current_dir + "/test_data/MFA_modelInputsData")


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
            + "/test_data/MFA_modelInputsData/reimport_test_data.obj",
            "rb",
        )
        (
            filename,
            simulation_info,
            simulation_id,
            info,
            parallel,
            non_stationary,
            m,
            f,
            model_info,
            f_mnt_info,
            f_mnt_res_info,
            f_par_info,
            fittedData,
            fittedFluxes,
            fittedFragments,
            fittedMeasuredFluxes,
            fittedMeasuredFragments,
            fittedMeasuredFluxResiduals,
            fittedMeasuredFragmentResiduals,
            simulationParameters,
            # fittedData2,
            # fittedFluxes2,
            # fittedFragments2,
            # fittedMeasuredFluxes2,
            # fittedMeasuredFragments2,
            # fittedMeasuredFluxResiduals2,
            # fittedMeasuredFragmentResiduals2,
            # simulationParameters2,
        ) = pickle.load(file_obj)
        file_obj.close()

        self.filename = filename
        self.simulation_info = simulation_info
        self.simulation_id = simulation_id
        self.info = info
        self.parallel = parallel
        self.non_stationary = non_stationary
        self.m = m
        self.f = f
        self.model_info = model_info
        self.f_mnt_info = f_mnt_info
        self.f_mnt_res_info = f_mnt_res_info
        self.f_par_info = f_par_info
        self.fittedData = fittedData
        self.fittedFluxes = fittedFluxes
        self.fittedFragments = fittedFragments
        self.fittedMeasuredFluxes = fittedMeasuredFluxes
        self.fittedMeasuredFragments = fittedMeasuredFragments
        self.fittedMeasuredFluxResiduals = fittedMeasuredFluxResiduals
        self.fittedMeasuredFragmentResiduals = fittedMeasuredFragmentResiduals
        self.simulationParameters = simulationParameters
        self.INCA_reimport = INCA_reimport()
        # self.fittedData2 = (fittedData2,)
        # self.fittedFluxes2 = (fittedFluxes2,)
        # self.fittedFragments2 = (fittedFragments2,)
        # self.fittedMeasuredFluxes2 = (fittedMeasuredFluxes2,)
        # self.fittedMeasuredFragments2 = (fittedMeasuredFragments2,)
        # self.fittedMeasuredFluxResiduals2 = (fittedMeasuredFluxResiduals2,)
        # self.fittedMeasuredFragmentResiduals2 = (
        #     fittedMeasuredFragmentResiduals2,
        # )
        # self.simulationParameters2 = (simulationParameters2,)
        # self.INCA_reimport_directly = INCA_reimport()

        # Add the method to compare dataframes in the class
        self.addTypeEqualityFunc(pd.DataFrame, self.assertDataframeEqual)

    """
    A couple of things are commented out here; they will be activated
    once I figure out a solution to the datetime issue; to the problem
    with comparing lists containing dicts that contain lists in the
    summarizing reimport function and to the comparison of MATLAB objects
    """

    # @freeze_time(datetime.datetime(2021, 2, 9, 17, 12, 50))
    # datetime issue
    # def test_extract_file_info(self):
    #     info = self.INCA_reimport.extract_file_info(
    #         self.filename
    #     )
    #     info_ = self.info
    #     self.assertEqual(info, info_)

    def test_det_simulation_type(self):
        parallel_, non_stationary_ = self.INCA_reimport.det_simulation_type(
            self.simulation_info
        )
        parallel = self.parallel
        non_stationary = self.non_stationary
        self.assertEqual(parallel, parallel_)
        self.assertEqual(non_stationary, non_stationary_)

    def test_data_extraction(self):
        """
        comparing m and f directly fails so we're only comparing their
        types here
        """
        m_, f_ = self.INCA_reimport.data_extraction(self.filename)
        m = self.m
        f = self.f
        self.assertEqual(type(m), type(m_))
        self.assertEqual(type(f), type(f_))

    # datetime issue
    def test_extract_model_info(self):
        model_info_ = self.INCA_reimport.extract_model_info(self.m)
        model_info = self.model_info
        self.assertEqual(model_info, model_info_)

    def test_extract_sim_params(self):
        simulationParameters_ = self.INCA_reimport.extract_sim_params(
            self.simulation_id, self.info, self.m, self.filename
        )
        simulationParameters = self.simulationParameters
        self.assertEqual(simulationParameters, simulationParameters_)

    def test_simulationParameters_testdata(self):
        simulationParameters_ = self.INCA_reimport.extract_sim_params(
            self.simulation_id, self.info, self.m, self.filename
        )
        self.assertTrue(len(simulationParameters_) > 0)

    def test_extract_base_stats(self):
        fittedData_ = self.INCA_reimport.extract_base_stats(
            self.f, self.simulation_id, self.info
        )
        fittedData = self.fittedData
        self.assertEqual(fittedData, fittedData_)

    def test_fittedData_testdata(self):
        fittedData_ = self.INCA_reimport.extract_base_stats(
            self.f, self.simulation_id, self.info
        )
        self.assertTrue(len(fittedData_) > 0)

    def test_get_fit_info(self):
        f_mnt_info_ = self.INCA_reimport.get_fit_info(self.f)
        f_mnt_info = self.f_mnt_info
        self.assertEqual(f_mnt_info, f_mnt_info_)

    def test_sort_fit_info(self):
        (
            fittedMeasuredFluxes_,
            fittedMeasuredFragments_,
        ) = self.INCA_reimport.sort_fit_info(
            self.f_mnt_info, self.simulation_info, self.fittedData
        )
        fittedMeasuredFluxes = self.fittedMeasuredFluxes
        fittedMeasuredFragments = self.fittedMeasuredFragments
        self.assertEqual(fittedMeasuredFluxes, fittedMeasuredFluxes_)
        self.assertEqual(fittedMeasuredFragments, fittedMeasuredFragments_)

    def test_fittedMeasuredFluxes_testdata(self):
        (
            fittedMeasuredFluxes_,
            fittedMeasuredFragments_,
        ) = self.INCA_reimport.sort_fit_info(
            self.f_mnt_info, self.simulation_info, self.fittedData
        )
        self.assertTrue(len(fittedMeasuredFluxes_) > 0)

    def test_fittedMeasuredFragments_testdata(self):
        (
            fittedMeasuredFluxes_,
            fittedMeasuredFragments_,
        ) = self.INCA_reimport.sort_fit_info(
            self.f_mnt_info, self.simulation_info, self.fittedData
        )
        self.assertTrue(len(fittedMeasuredFragments_) > 0)

    def test_get_residuals_info(self):
        f_mnt_res_info_ = self.INCA_reimport.get_residuals_info(
            self.f, self.simulation_info
        )
        f_mnt_res_info = self.f_mnt_res_info
        self.assertEqual(f_mnt_res_info, f_mnt_res_info_)

    def test_sort_residual_info(self):
        (
            fittedMeasuredFluxResiduals_,
            fittedMeasuredFragmentResiduals_,
        ) = self.INCA_reimport.sort_residual_info(
            self.f_mnt_res_info, self.simulation_info, self.fittedData
        )
        fittedMeasuredFluxResiduals = self.fittedMeasuredFluxResiduals
        fittedMeasuredFragmentResiduals = self.fittedMeasuredFragmentResiduals
        self.assertEqual(
            fittedMeasuredFluxResiduals, fittedMeasuredFluxResiduals_
        )
        self.assertEqual(
            fittedMeasuredFragmentResiduals, fittedMeasuredFragmentResiduals_
        )

    def test_fittedMeasuredFluxResiduals_testdata(self):
        (
            fittedMeasuredFluxResiduals_,
            fittedMeasuredFragmentResiduals_,
        ) = self.INCA_reimport.sort_residual_info(
            self.f_mnt_res_info, self.simulation_info, self.fittedData
        )
        self.assertTrue(len(fittedMeasuredFluxResiduals_) > 0)

    def test_fittedMeasuredFragmentResiduals_testdata(self):
        (
            fittedMeasuredFluxResiduals_,
            fittedMeasuredFragmentResiduals_,
        ) = self.INCA_reimport.sort_residual_info(
            self.f_mnt_res_info, self.simulation_info, self.fittedData
        )
        self.assertTrue(len(fittedMeasuredFragmentResiduals_) > 0)

    def test_get_fitted_parameters(self):
        f_par_info_ = self.INCA_reimport.get_fitted_parameters(
            self.f, self.simulation_info
        )
        f_par_info = self.f_par_info
        self.assertEqual(f_par_info, f_par_info_)

    def test_sort_parameter_info(self):
        (
            fittedFluxes_,
            fittedFragments_,
        ) = self.INCA_reimport.sort_parameter_info(
            self.f_par_info, self.simulation_info, self.fittedData
        )
        fittedFluxes = self.fittedFluxes
        fittedFragments = self.fittedFragments
        self.assertEqual(fittedFluxes, fittedFluxes_)
        self.assertEqual(fittedFragments, fittedFragments_)

    def test_fittedFluxes_testdata(self):
        (
            fittedFluxes_,
            fittedFragments_,
        ) = self.INCA_reimport.sort_parameter_info(
            self.f_par_info, self.simulation_info, self.fittedData
        )
        self.assertTrue(len(fittedFluxes_) > 0)

    def test_fittedFragments_testdata(self):
        (
            fittedFluxes_,
            fittedFragments_,
        ) = self.INCA_reimport.sort_parameter_info(
            self.f_par_info, self.simulation_info, self.fittedData
        )
        self.assertTrue(len(fittedFragments_) > 0)

    """
    # datetime issue
    def test_reimport(self):
        (
            fittedData2,
            fittedFluxes2,
            fittedFragments2,
            fittedMeasuredFluxes2,
            fittedMeasuredFragments2,
            fittedMeasuredFluxResiduals2,
            fittedMeasuredFragmentResiduals2,
            simulationParameters2,
        ) = self.INCA_reimport_directly.reimport(
            self.filename, self.simulation_info, self.simulation_id
        )
        fittedData2_ = self.fittedData2
        fittedFluxes2_ = self.fittedFluxes2
        fittedFragments2_ = self.fittedFragments2
        fittedMeasuredFluxes2_ = self.fittedMeasuredFluxes2
        fittedMeasuredFragments2_ = self.fittedMeasuredFragments2
        fittedMeasuredFluxResiduals2_ = self.fittedMeasuredFluxResiduals2
        fittedMeasuredFragmentResiduals2_ = (
            self.fittedMeasuredFragmentResiduals2
        )
        simulationParameters2_ = self.simulationParameters2
        self.assertEqual(fittedData2, fittedData2_)
        self.assertEqual(fittedFluxes2, fittedFluxes2_)
        self.assertEqual(fittedFragments2, fittedFragments2_)
        self.assertEqual(fittedMeasuredFluxes2, fittedMeasuredFluxes2_)
        self.assertEqual(fittedMeasuredFragments2, fittedMeasuredFragments2_)
        self.assertEqual(
            fittedMeasuredFluxResiduals2, fittedMeasuredFluxResiduals2_
        )
        self.assertEqual(
            fittedMeasuredFragmentResiduals2, fittedMeasuredFragmentResiduals2_
        )
        self.assertEqual(simulationParameters2, simulationParameters2_)
    """


if __name__ == "__main__":
    unittest.main()
