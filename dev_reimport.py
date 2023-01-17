#%%
import pandas as pd
import numpy as np
from BFAIR.mfa.INCA import INCA_reimport
import os
import dotenv
import logging 
from BFAIR.mfa.INCA import load_matlab_file

# Set working directory
os.chdir(dotenv.find_dotenv().replace('.env', ''))

# setup logging 
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Setup data paths 
filename = os.path.join("tests", "test_data", "MFA_modelInputsData", "simple_model", "simple_model.mat")
filename2 = os.path.join("tests", "test_data", "MFA_modelInputsData", "TestFile.mat")
simulation_info = pd.read_csv(os.path.join("tests", "test_data", "MFA_modelInputsData", "simple_model", "experimentalMS.csv"), index_col=0)
simulation_id = 'exp1'

#reimport_data = INCA_reimport()

#%%
#fittedData2, fittedFluxes2, fittedFragments2, fittedMeasuredFluxes2, fittedMeasuredFragments2, fittedMeasuredFluxResiduals2, fittedMeasuredFragmentResiduals2, simulationParameters2 = reimport_data.reimport(filename, simulation_info, simulation_id)
# %%


#%%
from dataclasses import dataclass, field
import pathlib
from scipy.io import loadmat, matlab
from typing import Literal
# INCA_output object

@dataclass
class INCA_results:
    """
    This class parses the output from INCA and stores the data in a dataclass.
    """
    inca_matlab_file: pathlib.Path
    matlab_obj: dict = field(init=False)
    fittedParameters: pd.DataFrame = field(init=False)

    def __post_init__(self):
        self.matlab_obj = self._load_mat()
        self.fittedParameters = pd.DataFrame.from_records(self.matlab_obj['f']['par'])
        self.fit_overview = self._parse_fit_overview()
        self.fit_detailed_fluxes = self._parse_fit_detailed_fluxes()
        self.fit_detailed_ms = self._parse_fit_detailed_ms()

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
            if ndarray.dtype != 'float64':
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

        data = loadmat(self.inca_matlab_file, struct_as_record=False, squeeze_me=True)
        return _check_vars(data)

    def _parse_fit_overview(self):
        """
        This function parse an overview of the measurements and their overall fit,
        i.e. the conbined values accross all data points in the measurement. For 
        example if the same flux or fragment is measured multiple times in the same 
        experiment. Further for fragements this combines all the all mass isopote 
        measurements within the fragment.
        """
        overview = (pd.DataFrame.from_records(self.matlab_obj['f']['mnt'])
            .drop(columns=['res']) # drop the residuals infomation. This is accessed seperatly
        )
        return overview
        
    def _parse_fit_detailed_quantity(self, quantity: Literal['Flux', 'MS', 'Pool']):
        """
        This function parses an overview of a specific quantity (Flux, MS, or Pool).
        It is used by specific functions to parse the fluxes, MS, and pools.

        Returns:
            df: pandas dataframe to be futher processed by the specific functions
        """
        flux_residual_info = np.array([])
        for measurement in self.matlab_obj['f']['mnt']:
            if measurement['type'] == quantity:
                flux_residual_info = np.append(flux_residual_info, measurement['res'])
        df = (pd.DataFrame.from_records(flux_residual_info) 
            # drop the columns which are not needed
            # esens and msens are the sensitivity diagnostics, which are handled seperatly
            .drop(columns=['esens', 'msens'])
            .rename(columns={'val': 'weighted residual'})
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
        df = (self._parse_fit_detailed_quantity('Flux')
            # peak is not relevant for fluxes.
            .reindex(columns=[ 'type' ,'expt', 'id', 'time', 'data', 'std', 'fit', 'weighted residual', 'cont', 'base'])
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
        df = (self._parse_fit_detailed_quantity('MS')
            .reindex(columns=['type', 'expt', 'id', 'peak', 'time', 'data', 'std', 'fit', 'weighted residual', 'cont', 'base'])
        )
        return df        

    def _parse_fit_detailed_pools(self):
        raise(NotImplementedError)
# %%
res = INCA_results(filename)
res2 = INCA_results(filename2)

#%%
res.matlab_obj['f']['mnt']
# %%
# matlab_obj['f']['par']
# This is an array which holds a dictionary for each parameters (reaction) in the model
# Some of the keys contain lists and I believe chi2s, and vals these are one for each restart,
# while cor and cov contains one for each reaction.

# matlab_obj['f']['mnt']
# This is an array which holds a dictionary for each measurement in the model (both fluxes and fragments)

# For fluxes the the dict is straight forward to understand. It is worth moticing that the input data
# is stored in the 'data' key and the fitted data is stored in the 'fit' key. I'm not sure if the 'data'
# is the values corrected natural abundance or the raw values.

# The fragments are a bit more complicated. The dictionary immediately contain overall value e.g. sres and 
# cont, which the contribution of the full fragement to each of the fitted parameters (reactions). The 'res'
# key contains a list of dictionaries, one for each fragment. The 'val' is the weighted residual ((fit - data)/std)