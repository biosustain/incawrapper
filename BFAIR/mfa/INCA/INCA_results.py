import pandas as pd
import numpy as np
from BFAIR.mfa.INCA import load_matlab_file
from BFAIR.mfa.INCA.INCA_model import INCA_model
from dataclasses import dataclass
import pathlib
from typing import Literal, Dict, List


@dataclass
class INCA_results:
    """
    This class parses the output from INCA and stores the data in a dataclass. On init the class
    loads the matlab file and parses the data into several pandas dataframe, which can be accessed
    via the class attributes. The class also contains the INCA_model class, which can be accessed
    via the model attribute. This contains information about the model which was fitted.
    """

    inca_matlab_file: pathlib.Path

    def __post_init__(self):
        self.matlab_obj: Dict = load_matlab_file.load_matlab_file(self.inca_matlab_file)
        self.model: INCA_model = INCA_model(self.inca_matlab_file)
        self.fitted_parameters: pd.DataFrame = self._parse_fitted_parameters()
        self.measurements_and_fit_overview: pd.DataFrame = self._parse_measurements_and_fit_overview()
        self.measurements_and_fit_detailed: pd.DataFrame = self._parse_measurements_and_fit_detailed()


    def _parse_fitted_parameters(self):
        """
        This function parses the fitted parameters from the INCA output
        """
        df = pd.DataFrame.from_records(self.matlab_obj["f"]["par"]).reindex(
            columns=[
                "type",
                "id",
                "eqn",
                "val",
                "std",
                "lb",
                "ub",
                "unit",
                "free",
                "alf",
                "chi2s",
                "cont",
                "cor",
                "cov",
                "vals",
                "base",
            ]
        )
        return df

    def _parse_measurements_and_fit_overview(self):
        """
        This function parse an overview of the measurements and their overall fit,
        i.e. the conbined values accross all data points in the measurement. For
        example if the same flux or fragment is measured multiple times in the same
        experiment. Further for fragements this combines all the all mass isopote
        measurements within the fragment.
        """
        overview = pd.DataFrame.from_records(self.matlab_obj["f"]["mnt"]).drop(
            columns=["res"]
        )  # drop the residuals infomation. This is accessed seperatly
        return overview

    def _parse_measurements_and_fit_detailed(self):
        """
        This function parses an overview of a specific quantity (Flux, MS, or Pool).
        It is used by specific functions to parse the fluxes, MS, and pools.

        Returns:
            df: pandas dataframe to be futher processed by the specific functions
        """
        detailed_info = np.array([])
        for measurement in self.matlab_obj["f"]["mnt"]:
            detailed_info = np.append(detailed_info, measurement["res"])
        df = (
            pd.DataFrame.from_records(detailed_info)
            # drop the columns which are not needed
            # esens and msens are the sensitivity diagnostics, which are handled seperatly
            .drop(
                columns=["esens", "msens", 'cont']
            ).rename(
                columns={"val": "weighted residual"}
            ).reindex(
                columns=[
                    "type",
                    "expt",
                    "id",
                    "peak",
                    "time",
                    "data",
                    "std",
                    "fit",
                    "weighted residual",
                    "cont",
                    "base",
                ]
            )
        )
        return df

    def get_measurements_and_fit_detailed(self, quantity: Literal["Flux", "Fragment", "Pool"]):
        """
        Return a copy of the measurements and fit detailed dataframe which only contain 
        the desired quantity. 

        output:
            df: pandas dataframe with the following columns:
                expt: experiment id
                id: measurement id
                type: measurement type (Flux or Fragment)
                time: time of measurement
                data: measured data
                std: standard deviation of the measurement
                fit: fitted data
                weigthed residual: residual value of the fit weighted by the standard deviation of the measurement
                cont: contribution of the measurement to each fitted parameter.
                base: DONT know what this is
        """
        df = (
            self.measurements_and_fit_detailed
            .query(f"type == '{quantity}'")
            .copy()
        )

        if quantity in ["Flux", "Pool"]:
            df = df.drop(columns=["peak"])
        return df
    