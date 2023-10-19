import pandas as pd
import numpy as np
from incawrapper.core import load_matlab_file
from dataclasses import dataclass
import pathlib
from typing import Dict, List

@dataclass
class INCAModel:
    """A class to represent the INCA model. This class is used to extract the model information from
    the .mat file produced by INCA. The class holds a few methods to extract information from the model,
    thus is can be used to inspect what model was fitted.
    
    The INCAModel class is used by the INCAResults class, and is not intended to be used directly.
    
    Parameters
    -----------
    inca_matlab_file : pathlib.Path
        Path to the .mat file produced by INCA.

    Attributes
    -----------
    raw
    inca_options
    metabolite_ids
    states
    """

    inca_matlab_file: pathlib.Path

    @property
    def raw(self) -> Dict:
        """Load the raw data from the .mat file. This is a nested dictionary that contains all the
        information about the model. It can be diffucult to navigate, but it is possible to find
        that is not possible to extract from the class methods or attributes.
        
        Returns
        -------
        Dict
            Dictionary with the model information
        """
        return load_matlab_file.load_matlab_file(self.inca_matlab_file)['m']

    @property
    def inca_options(self) -> Dict:
        """Get the settings used in INCA during the run.
        
        Notes
        -----
        The options are described in the INCA documentation. You can find it 
        in your local INCA installation folder: `<PATH-TO-INCA-FOLDER>/doc/inca/class/@option/option.html`

        Returns
        -------
        Dict
            Dictionary with the INCA options 
        """

        return self.raw["options"]

    @property
    def metabolite_ids(self) -> List:
        """
        Gets a list of the metabolite ids, from the fitted model.

        Returns
        -------
        List 
            List of metabolite ids
        """
        metabolites = pd.DataFrame.from_records(self.raw["mets"])
        return metabolites["id"].to_list()

    @property
    def states(self) -> pd.DataFrame:
        """
        Get a data frame with the metabolites and associated information, e.g. their source/sink status or
        balanced/unbalanced status.

        Returns
        -------
        pd.DataFrame
            Dataframe with the states
        """
        return pd.DataFrame.from_records(self.raw["states"])
    
    @property
    def reactions(self) -> pd.DataFrame:
        """
        Get a data frame with the reactions and the set flux value. For estimation proceedures the set flux
        value is the initial guess, and for simulation it is the value used for the simulation. 

        Returns
        -------
        pd.DataFrame
            Dataframe with the reactions
        """
        ids = self._extract_reaction_ids()
        fluxes = self._extra_set_flux_values()
        return pd.DataFrame(
            {'rxn_id': ids, 'flux': fluxes}
        )

    def _extract_reaction_ids(self)->List[str]:
        """Extract the reaction ids from the raw model data. Reactions that are reversible has two ids
        one for the forward and one for exchange direction.""" 
        reaction_ids = []
        for rate in self.raw['rates']:
            if type(rate['flx']) == dict:
                reaction_ids.append(rate['id'])
            if type(rate['flx']) == np.ndarray:
                for direction in rate['flx']:
                    reaction_ids.append(direction['id'])
        return reaction_ids

    def _extra_set_flux_values(self):
        """Extra the set fluxes from a inca model rates object. A vector of all the set fluxes
        is stored in each rate object. Here we simply extract the information from the first. 
        The order of the fluxes is the same as the order of the reaction ids."""
        return self.raw['rates'][0]['flx']['val']

