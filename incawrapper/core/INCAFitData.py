import pandas as pd
import numpy as np
from incawrapper.core import load_matlab_file
from dataclasses import dataclass
import pathlib
from typing import Dict, Iterable, Callable
import scipy.stats

@dataclass
class INCAFitData:
    """
    This class parses the output from INCA and stores the data in a dataclass. On init the class
    loads the matlab file and parses the data into several pandas dataframe, which can be accessed
    via the class attributes. This class is not intended to be used directly, but rather through
    the INCAResults class.

    Parameters
    ----------
    inca_matlab_file : pathlib.Path
        The path to the matlab file containing the INCA output.

    Attributes
    ----------
    raw
    alpha
    chi2
    degrees_of_freedom
    expected_chi2
    fitted_parameters
    measurements_and_fit_overview
    measurements_and_fit_detailed

    Notes
    -----
    The data in the this object is directly parsed from the matlab file and is not modified
    by the incawrapper package. Thus, please refer to the INCA documentation for more information
    on how they are calculated.
    """

    inca_matlab_file: pathlib.Path
    """The path to the matlab file containing the INCA output."""

    @property
    def raw(self) -> Dict:
        """Gets the raw parsed matlab structure that contains the fitting results.

        Returns
        -------
        Dict
            This attribute contains the raw fitdata from the INCA output."""
        return load_matlab_file.load_matlab_file(self.inca_matlab_file)['f']

    @property
    def alpha(self) -> float:
        """Gets the alpha value used for to obtain the confidence intervals.

        Returns
        -------
        float
            This attribute contains the alpha value used for to obtain the confidence intervals.
        """
        return self.raw["alf"]
    
    @property
    def chi2(self) -> float:
        """Gets the chi2 value of the fit.

        Returns
        -------
        float
            This attribute contains the chi2 value of the fit.
        """
        return self.raw["chi2"]
    
    @property
    def degrees_of_freedom(self) -> int:
        """Gets the degrees of freedom of the fit.

        Returns
        -------
        int
            This attribute contains the degrees of freedom of the fit.
        """

        return self.raw["dof"]
    
    @property
    def expected_chi2(self) -> Iterable[float]:
        """Gets the expected chi2 interval of the fit. The first value is the lower bound and the second
        value is the upper bound.

        Returns
        -------
        Iterable[float]
            This attribute contains the expected chi2 interval of the fit.
        """
        return self.raw["Echi2"]

    @property
    def fitted_parameters(self) -> pd.DataFrame:
        """
        Gets the fitted parameters and their associated standard error, lower bound, upper bound and other
        information. This information is equivalent to the table shown in the main window of the Flux 
        Estimation tab in the INCA GUI.
        
        Returns
        -------
        pd.DataFrame
            This attribute contains the fitted parameters from the INCA output.
            The columns of the dataframe are:
            * type: type of the parameter (Flux, Pool, or MS)
            * id: id of the parameter (flux, pool, or MS)
            * eqn: reaction equation of the flux. For pools and MS this is empty
            * val: fitted value of the parameter
            * std: estimated standard deviation of the fitted value
            * lb: lower bound of the fitted value (Obtained from continuation or monte carlo simulation)
            * ub: upper bound of the fitted value (Obtained from continuation or monte carlo simulation)
            * unit: unit of the parameter
            * free: boolean indicating if the parameter was fitted or not
            * cor: correlation vector for this parameter to the other fitted parameters. The order matches
            the order of the other parameters in the dataframe 
            * cov: covariance vector similar to the cor column
            * vals: value of the parameter of each restart of the estimation algorithm (length of vals is 
            equal to the number of fit_starts option)
            * base: don't know what this is
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
    @property
    def measurements_and_fit_overview(self):
        """
        Gets an overview of the measurements and their overall fit,
        i.e. the conbined values accross all data points in the measurement. For
        example if the same flux or fragment is measured multiple times in the same
        experiment. Further for fragements this combines all the all mass isopote
        measurements within the fragment.
        """
        overview = pd.DataFrame.from_records(self.raw["mnt"]).drop(
            columns=["res"]
        )  # drop the residuals infomation. This is accessed seperatly through the measurements_and_fit_detailed attribute
        return overview

    @property
    def measurements_and_fit_detailed(self) -> pd.DataFrame:
        """
        Gets a dataframe all measuremets, their associatted fitted value and weighted residuals.

        Returns
        -------
        pd.DataFame
            This attribute contains an overview of the measurements and their overall fit. The columns 
            of the dataframe are:
            * expt: experiment id
            * id: measurement id
            * type: measurement type (Flux, Fragment, or pool size)
            * time: time of measurement
            * data: measured data
            * std: standard deviation of the measurement
            * fit: fitted data
            * weigthed residual: residual value of the fit weighted by the standard deviation of the measurement
            * cont: contribution of the measurement to each fitted parameter.
            * base: DONT know what this is
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