from incawrapper.core.load_matlab_file import load_matlab_file
from incawrapper.core.INCAModel import INCAModel
from incawrapper.core.INCAFitData import INCAFitData
from incawrapper.core.INCASimulation import INCASimulation
from incawrapper.core.INCAMonteCarloResults import INCAMonteCarloResults
from dataclasses import dataclass
import pathlib
from typing import Union


@dataclass
class INCAResults:
    """
    This class parses the output from INCA and stores the data in three different classes (INCAModel,
    INCAFitData, and INCASimulation). The subclasses mimmick the structure in the .mat file. The purpose
    of this class is to ensure the data, model and simulation remain linked.

    Parameters
    ----------
    inca_matlab_file : pathlib.Path
        path to the .mat file containing the INCA output
    load_mc_data : bool or pathlib.Path, optional
        If True, the Monte Carlo results will be loaded and the file name will be inferred from the
        inca_matlab_file. If a pathlib.Path object is passed, the Monte Carlo results will be loaded
        from the specified file. If False, the Monte Carlo results will not be loaded. Default is False.
    """

    inca_matlab_file: pathlib.Path
    load_mc_data: Union[bool,pathlib.Path] = False
    
    def __post_init__(self):
        self._inca_matlab_file = self._coerce_pathlib(self.inca_matlab_file)
        self.model: INCAModel = INCAModel(self._inca_matlab_file)
        self.fitdata: INCAFitData = INCAFitData(self._inca_matlab_file)
        self.simulation: INCASimulation = INCASimulation(self._inca_matlab_file)
        self.mc: INCAMonteCarloResults = self._load_mc_results() 

    def _coerce_pathlib(self, path):
        """Convert a path to a pathlib.Path object if it is not already one. Required because we suspect
        that some users may pass a string instead of a pathlib.Path object."""
        if isinstance(path, pathlib.Path):
            return path
        else:
            return pathlib.Path(path)
    
    def _load_mc_results(self):
        """Load the Monte Carlo results from the .mat file. If load_mc_data is False, return None.
        If load_mc_data is a pathlib.Path object, load the Monte Carlo results from the specified file.
        If load_mc_data is True, load the Monte Carlo results from the file inferred from the
        inca_matlab_file."""

        if not self.load_mc_data:
            return None

        if isinstance(self.load_mc_data, bool):
            mcfile = self.inca_matlab_file.with_name(self._inca_matlab_file.stem + "_mc.mat")
            parameter_names = self.fitdata.fitted_parameters['id'].tolist()
            return INCAMonteCarloResults(mcfile, parameter_names)


        self.load_mc_data = self._coerce_pathlib(self.load_mc_data)
        if isinstance(self.load_mc_data, pathlib.Path):
            parameter_names = self.fitdata.fitted_parameters['id'].tolist()
            return INCAMonteCarloResults(self.load_mc_data, parameter_names)


__all__ = ["INCAResults"]