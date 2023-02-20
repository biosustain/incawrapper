import pandas as pd
import numpy as np
from BFAIR.mfa.INCA import load_matlab_file
from dataclasses import dataclass
import pathlib
from typing import Literal, Dict, List

@dataclass
class INCASimulation:
    inca_matlab_file: pathlib.Path

    def __post_init__(self):
        self.raw: Dict = load_matlab_file.load_matlab_file(self.inca_matlab_file)['s']

