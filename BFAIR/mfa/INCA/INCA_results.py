import pandas as pd
import numpy as np
from BFAIR.mfa.INCA import load_matlab_file
from BFAIR.mfa.INCA.INCA_model import INCA_model
from BFAIR.mfa.INCA.INCA_fitdata import INCA_fitdata
from BFAIR.mfa.INCA.INCA_simulation import INCA_simulation
from dataclasses import dataclass
import pathlib
from typing import Literal, Dict, Iterable, Callable
import scipy.stats


@dataclass
class INCA_results:
    """
    This class parses the output from INCA and stores the data in three different classes (INCA_model,
    INCA_fitdata, and INCA_simulation). The subclasses mimmick the structure in the .mat file. The purpose
    of this class is to ensure the data, model and simulation remain linked.
    """

    inca_matlab_file: pathlib.Path

    def __post_init__(self):
        self.model: INCA_model = INCA_model(self.inca_matlab_file)
        self.fitdata: INCA_fitdata = INCA_fitdata(self.inca_matlab_file)
        self.simulation: INCA_simulation = INCA_simulation(self.inca_matlab_file)
