from dataclasses import dataclass
from incawrapper.core import load_matlab_file
from typing import List
import pathlib
import pandas as pd


@dataclass
class INCAMonteCarloResults:
    mcfile: pathlib.Path
    parameter_names: List[str]
    
    def __post_init__(self):
        self.mc = load_matlab_file.load_matlab_file(self.mcfile)

        if "CI" in self.mc.keys(): # test if the mc file is a finished mc file
            self.ci = pd.DataFrame(self.mc["CI"], columns = self.parameter_names, index = ["lb", "ub"])
            self.samples = pd.DataFrame(self.mc["K"], columns = self.parameter_names)
        
        # parsing samples from dump file
        elif "ci0" in self.mc.keys(): # test if the mc file is a dump file
            samples = {}

            # if the mc sampling has been interrupted early, i.e. only 1 iteration has finished, the shape 
            # of the k matrix is (n_samples, n_parameters), and not (n_iterations, n_samples, n_parameters)
            # this is a quick fix to make sure that the shape is always (n_iterations, n_samples, n_parameters)
            if len(self.mc['k'].shape) == 2:
                self.mc['k'] = self.mc['k'].reshape(1, self.mc['k'].shape[0], self.mc['k'].shape[1])

            for idx, name in enumerate(self.parameter_names):
                samples[name] = (self.mc['k'][:,:,idx]).flatten()
            self.samples = pd.DataFrame.from_dict(samples)
            self.ci = pd.DataFrame(self.mc["ci0"], columns = self.parameter_names, index = ["lb", "ub"])
        else:
            raise TypeError("The mc file is not a valid mc file")
             