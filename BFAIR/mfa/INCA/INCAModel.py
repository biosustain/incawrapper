import pandas as pd
import numpy as np
from BFAIR.mfa.INCA import load_matlab_file
from dataclasses import dataclass
import pathlib
from typing import Literal, Dict, List

@dataclass
class INCAModel:
    inca_matlab_file: pathlib.Path

    def __post_init__(self):
        self.raw: Dict = load_matlab_file.load_matlab_file(self.inca_matlab_file)['m']
        self.inca_options: Dict = self.raw["options"]
        self.inca_options_description: str = """The options are described in the INCA documentation. You can find it 
in your local INCA installation folder: <PATH-TO-INCA-FOLDER>/doc/inca/class/@option/option.html"""

    def get_metabolite_ids(self) -> List:
        """
        Return the metabolite ids, from the fitted model.

        Returns:
            List: List of metabolite ids
        """
        metabolites = pd.DataFrame.from_records(self.raw["mets"])
        return metabolites["id"].to_list()

    def get_states(self) -> pd.DataFrame:
        """
        Return the states, from the fitted model.

        Returns:
            pd.DataFrame: Dataframe with the states
        """
        return pd.DataFrame.from_records(self.raw["states"])