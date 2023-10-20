import pandas as pd
import numpy as np
from incawrapper.core import load_matlab_file
from dataclasses import dataclass
import pathlib
from typing import Literal, Dict, List

@dataclass
class INCASimulation:
    inca_matlab_file: pathlib.Path

    def __post_init__(self):
        self.raw: Dict = load_matlab_file.load_matlab_file(self.inca_matlab_file)['s']

    @property
    def simulated_data(self)->pd.DataFrame:
        """Get the simulated MDVs."""
        return self._parse_simulated_data()


    def _parse_simulated_data(self)->pd.DataFrame:
        """Parse the simulated data from the raw INCA results."""
        raw_df = pd.DataFrame.from_records(self.raw)[['expt', 'id', 'time', 'type', 'val']]

        # Determines if the simulation is steady state or not
        if 'inf' not in raw_df['time']:
            # The timeseries mdvs are stored in a matrix in the val column
            raw_df['val'] = raw_df['val'].map(lambda x: x.transpose())
            raw_df=raw_df.explode(['time', 'val'])
        
        raw_df['mass_isotope'] = raw_df['val'].map(lambda x: np.arange(0, len(x)))
        long_format = (raw_df
            .explode(['val','mass_isotope'])
            .rename(columns={'val': 'mdv'})
        )
        
        return long_format
