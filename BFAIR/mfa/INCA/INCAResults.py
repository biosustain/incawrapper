import pandas as pd
import numpy as np
from BFAIR.mfa.INCA import load_matlab_file
from BFAIR.mfa.INCA.INCAModel import INCAModel
from BFAIR.mfa.INCA.INCAFitData import INCAFitData
from BFAIR.mfa.INCA.INCASimulation import INCASimulation
from dataclasses import dataclass
import pathlib
from typing import Literal, Dict, Iterable, Callable
import scipy.stats


@dataclass
class INCAResults:
    """
    This class parses the output from INCA and stores the data in three different classes (INCAModel,
    INCAFitData, and INCASimulation). The subclasses mimmick the structure in the .mat file. The purpose
    of this class is to ensure the data, model and simulation remain linked.
    """

    inca_matlab_file: pathlib.Path

    def __post_init__(self):
        self.model: INCAModel = INCAModel(self.inca_matlab_file)
        self.fitdata: INCAFitData = INCAFitData(self.inca_matlab_file)
        self.simulation: INCASimulation = INCASimulation(self.inca_matlab_file)
