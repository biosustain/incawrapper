import pandas as pd
import numpy as np
from BFAIR.mfa.INCA import load_matlab_file
from BFAIR.mfa.INCA.INCAModel import INCAModel
from dataclasses import dataclass
import pathlib
from typing import Literal, Dict, Iterable, Callable
import scipy.stats


@dataclass
class INCAFitData:
    """
    This class parses the output from INCA and stores the data in a dataclass. On init the class
    loads the matlab file and parses the data into several pandas dataframe, which can be accessed
    via the class attributes. The class also contains the INCAModel class, which can be accessed
    via the model attribute. This contains information about the model which was fitted.
    """

    inca_matlab_file: pathlib.Path

    def __post_init__(self):
        self.raw: Dict = load_matlab_file.load_matlab_file(self.inca_matlab_file)['f']
        """Dict: This attribute contains the raw fitdata from the INCA output."""

        self.fitted_parameters: pd.DataFrame = self._parse_fitted_parameters()
        """pd.DataFrame: This attribute contains the fitted parameters from the INCA output.
        
        The columns of the dataframe are:
        - type: type of the parameter (Flux, Pool, or MS)
        - id: id of the parameter (flux, pool, or MS)
        - eqn: reaction equation of the flux. For pools and MS this is empty
        - val: fitted value of the parameter
        - std: estimated standard deviation of the fitted value
        - lb: lower bound of the fitted value (Obtained from continuation or monte carlo simulation)
        - ub: upper bound of the fitted value (Obtained from continuation or monte carlo simulation)
        - unit: unit of the parameter
        - free: boolean indicating if the parameter was fitted or not"""

        self.measurements_and_fit_overview: pd.DataFrame = self._parse_measurements_and_fit_overview()
        """pd.DataFrame: This attribute contains an overview of the measurements and their overall fit"""

        self.measurements_and_fit_detailed: pd.DataFrame = self._parse_measurements_and_fit_detailed()
        self.alpha: float = self.raw["alf"]
        self.chi2: float = self.raw["chi2"]
        self.degrees_of_freedom: int = self.raw["dof"]
        self.expected_chi2: Iterable[float, float] = self.raw["Echi2"]


    def _parse_fitted_parameters(self):
        """
        This function parses the fitted parameters from the INCA output
        """
        df = pd.DataFrame.from_records(self.raw["par"]).reindex(
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
        overview = pd.DataFrame.from_records(self.raw["mnt"]).drop(
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
        for measurement in self.raw["mnt"]:
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

    def get_goodness_of_fit(self)->None:
        """
        Return the goodness of fit for the model. This is the chi2 value divided by the degrees of freedom
        """
        fit_accepted = self.expected_chi2[0] <= self.chi2 <= self.expected_chi2[1]

        print(
        f'''Fit accepted: {fit_accepted}
Confidence level: {self.alpha}
Chi-square value (SSR): {self.chi2}
Expected chi-square range: {self.expected_chi2}'''
        )
    
    def test_normality_of_residuals(self, test_function: Callable = scipy.stats.shapiro, alpha: float = None)->None:
        """
        Test the normality of the residuals of the model. This is done by default using the Shapiro-Wilk test.
        The user can specify a different test using the test_function argument. The test function should take
        an array of residuals as input and return a test statistic and a p-value. The p-value is compared to the
        alpha value to determine if the residuals are normally distributed. The default alpha is the overall alpha
        value for the model. This can be changed using the alpha argument.
        """
        if alpha is None:
            alpha = self.alpha
        
        residuals = self.measurements_and_fit_detailed['weighted residual']
        test_statistic, p_value = test_function(residuals)
        # The shapiro test test the null hypothsis that the data is drawn from a normal distribution
        # Therefore if the p-value is greater than the alpha value the null hypothesis is accepted, i.e. 
        # residuals are normally distributed
        print(f'Residuals are normally distributed: {p_value > alpha} on a {alpha} significance level')