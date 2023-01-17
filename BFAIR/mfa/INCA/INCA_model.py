import pandas as pd
import numpy as np
from BFAIR.mfa.INCA import load_matlab_file
from dataclasses import dataclass
import pathlib
from typing import Literal, Dict, List

@dataclass
class INCA_model:
    inca_matlab_file: pathlib.Path

    def __post_init__(self):
        self.matlab_model_obj: Dict = load_matlab_file.load_matlab_file(self.inca_matlab_file)['m']
        self.inca_options: Dict = self.matlab_model_obj["options"]

    def get_metabolite_ids(self) -> List:
        """
        Return the metabolite ids, from the fitted model.

        Returns:
            List: List of metabolite ids
        """
        metabolites = pd.DataFrame.from_records(self.matlab_model_obj["mets"])
        return metabolites["id"].to_list()

    def get_states(self) -> pd.DataFrame:
        """
        Return the states, from the fitted model.

        Returns:
            pd.DataFrame: Dataframe with the states
        """
        return pd.DataFrame.from_records(self.matlab_model_obj["states"])