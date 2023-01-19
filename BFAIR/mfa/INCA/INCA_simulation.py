import pandas as pd
import numpy as np
from BFAIR.mfa.INCA import load_matlab_file
from dataclasses import dataclass
import pathlib
from typing import Literal, Dict, List

@dataclass
class INCA_simulation:
    inca_matlab_file: pathlib.Path

    def __post_init__(self):
        raise NotImplementedError
