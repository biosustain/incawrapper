from dataclasses import dataclass
from BFAIR.mfa.INCA.load_matlab_file import load_matlab_file
from typing import List
import pathlib
import pandas as pd


@dataclass
class INCAMonteCarloResults:
    mcfile: pathlib.Path
    parameter_names: List[str]
    
    def __post_init__(self):
        self.mc = load_matlab_file(self.mcfile)
        self.ci = pd.DataFrame(self.mc["CI"], columns = self.parameter_names, index = ["lb", "ub"])
        self.samples = pd.DataFrame(self.mc["K"], columns = self.parameter_names)
    