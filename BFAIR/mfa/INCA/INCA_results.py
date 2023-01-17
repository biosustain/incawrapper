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
        self.fit_overview: pd.DataFrame = self._parse_fit_overview()
        self.fit_detailed_fluxes: pd.DataFrame = self._parse_fit_detailed_fluxes()
        self.fit_detailed_ms: pd.DataFrame = self._parse_fit_detailed_ms()


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

    def _parse_fit_overview(self):
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

    def _parse_fit_detailed_quantity(self, quantity: Literal["Flux", "MS", "Pool"]):
        """
        This function parses an overview of a specific quantity (Flux, MS, or Pool).
        It is used by specific functions to parse the fluxes, MS, and pools.

        Returns:
            df: pandas dataframe to be futher processed by the specific functions
        """
        flux_residual_info = np.array([])
        for measurement in self.matlab_obj["f"]["mnt"]:
            if measurement["type"] == quantity:
                flux_residual_info = np.append(flux_residual_info, measurement["res"])
        df = (
            pd.DataFrame.from_records(flux_residual_info)
            # drop the columns which are not needed
            # esens and msens are the sensitivity diagnostics, which are handled seperatly
            .drop(columns=["esens", "msens"]).rename(
                columns={"val": "weighted residual"}
            )
        )
        return df

    def _parse_fit_detailed_fluxes(self):
        """
        This function parses an overview of all individual flux measurements from the
        measurements (mnt) array.

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
            self._parse_fit_detailed_quantity("Flux")
            # peak is not relevant for fluxes.
            .reindex(
                columns=[
                    "type",
                    "expt",
                    "id",
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

    def _parse_fit_detailed_ms(self):
        """
        This function parses an overview of all individual MS (typical framgent) measurements from the
        measurements (mnt) array.

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
        df = self._parse_fit_detailed_quantity("MS").reindex(
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
        return df

    def _parse_fit_detailed_pools(self):
        raise (NotImplementedError)