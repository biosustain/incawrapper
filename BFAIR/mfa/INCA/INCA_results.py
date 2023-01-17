import pandas as pd
import numpy as np
from BFAIR.mfa.INCA import INCA_reimport
from dataclasses import dataclass
import pathlib
from scipy.io import loadmat, matlab
from typing import Literal, Dict, List


@dataclass
class INCA_results:
    """
    This class parses the output from INCA and stores the data in a dataclass. On init the class
    loads the matlab file and parses the data into several pandas dataframe, which can be accessed
    via the class attributes.
    """

    inca_matlab_file: pathlib.Path

    def __post_init__(self):
        self.matlab_obj: Dict = self._load_mat()
        self.inca_options: Dict = self.matlab_obj["m"]["options"]
        self.fitted_parameters: pd.DataFrame = self._parse_fitted_parameters()
        self.fit_overview: pd.DataFrame = self._parse_fit_overview()
        self.fit_detailed_fluxes: pd.DataFrame = self._parse_fit_detailed_fluxes()
        self.fit_detailed_ms: pd.DataFrame = self._parse_fit_detailed_ms()

    def _load_mat(self):
        """
        This function should be called instead of direct scipy.io.loadmat
        as it cures the problem of not properly recovering python dictionaries
        from mat files. It calls the function check keys to cure all entries
        which are still mat-objects

        Thanks to Jeff Lin for this solution
        From: https://stackoverflow.com/questions/48970785/complex-matlab-struct-mat-file-read-by-python
        """

        def _check_vars(d):
            """
            Checks if entries in dictionary are mat-objects. If yes
            todict is called to change them to nested dictionaries
            """
            for key in d:
                if isinstance(d[key], matlab.mat_struct):
                    d[key] = _todict(d[key])
                elif isinstance(d[key], np.ndarray):
                    d[key] = _toarray(d[key])
            return d

        def _todict(matobj):
            """
            A recursive function which constructs from matobjects nested dictionaries
            """
            d = {}
            for strg in matobj._fieldnames:
                elem = matobj.__dict__[strg]
                if isinstance(elem, matlab.mat_struct):
                    d[strg] = _todict(elem)
                elif isinstance(elem, np.ndarray):
                    d[strg] = _toarray(elem)
                else:
                    d[strg] = elem
            return d

        def _toarray(ndarray):
            """
            A recursive function which constructs ndarray from cellarrays
            (which are loaded as numpy ndarrays), recursing into the elements
            if they contain matobjects.
            """
            if ndarray.dtype != "float64":
                elem_list = []
                for sub_elem in ndarray:
                    if isinstance(sub_elem, matlab.mat_struct):
                        elem_list.append(_todict(sub_elem))
                    elif isinstance(sub_elem, np.ndarray):
                        elem_list.append(_toarray(sub_elem))
                    else:
                        elem_list.append(sub_elem)
                return np.array(elem_list)
            else:
                return ndarray

        data = loadmat(self.inca_matlab_file, struct_as_record=False, squeeze_me=True, appendmat=False)
        return _check_vars(data)

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

    def get_metabolite_ids(self) -> List:
        """
        Return the metabolite ids, from the fitted model.

        Returns:
            List: List of metabolite ids
        """
        metabolites = pd.DataFrame.from_records(self.matlab_obj["m"]["mets"])
        return metabolites["id"].to_list()

    def get_states(self) -> pd.DataFrame:
        """
        Return the states, from the fitted model.

        Returns:
            pd.DataFrame: Dataframe with the states
        """
        return pd.DataFrame.from_records(self.matlab_obj["m"]["states"])