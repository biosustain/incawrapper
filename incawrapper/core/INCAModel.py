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
    def rates(self)->pd.DataFrame:
        """Extract the reaction ids from the raw model data. Reactions that are reversible has two ids
        one for the forward and one for exchange direction.""" 
        rates_collector = []
        for rate in self.raw['rates']:
            if type(rate['flx']) == dict:
                rates_collector.append(_clean_flx_dict(rate['flx']))
            if type(rate['flx']) == np.ndarray:
                for direction in rate['flx']:
                    rates_collector.append(_clean_flx_dict(direction))
        return pd.DataFrame.from_records(rates_collector)
    
    @property
    def rates_in_net_exch_format(self) -> pd.DataFrame:
        return _convert_reactions_to_net_exch_format(self.rates)


def _convert_reactions_to_net_exch_format(df)->pd.DataFrame:
    """In INCA the reversible reactions are stored as a forward and backward reaction. However,
    sometimes INCA represents the reactions as a net and exchange reaction. This function converts
    the reversible reactions to net and exchange reactions. The method for convertion is found in
    the INCA Manual.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with the reactions. The dataframe must have the columns `rxn_id` and `flux`.
        Usually obtain from the `reactions` property of the `INCAModel` class.
    
    Returns
    -------
    pd.DataFrame
        Dataframe with the reactions in net and exchange format.
    
    Notes
    -----
    This function is separeted from the `INCAModel` class, to ease testing.
    """
    df=df.copy()

    new_reactions_df = pd.DataFrame()
    for rxn_id, dat in df.groupby('rxn'):
        if dat.shape[0] == 2:
            forward_flux = dat[dat['dir'] == 'f']['val'].values[0]
            backward_flux = dat[dat['dir'] == 'b']['val'].values[0]

            net_flux = forward_flux - backward_flux
            exch_flux = min([forward_flux, backward_flux])
            rxn_df = pd.DataFrame.from_dict(
                {
                    'rxn_id': [f'{rxn_id} net', f'{rxn_id} exch'],
                    'flux': [net_flux, exch_flux],
                }
            ) 

            new_reactions_df = pd.concat([
                new_reactions_df,
                rxn_df 
            ])
        else:
            new_reactions_df = pd.concat([
                new_reactions_df,
                dat[['rxn', 'val']].rename(columns={'rxn': 'rxn_id', 'val': 'flux'})
            ])

    return new_reactions_df.reset_index(drop=True)

def _clean_flx_dict(flx_dict):
    """Cleans the flux dictionary. Removes the keys that are not needed.

    Parameters
    ----------
    flx_dict : Dict
        Dictionary with the flux information.
    
    Returns
    -------
    Dict
        Dictionary with the parsed flux information.
    """
    # remove the keys that are not needed
    flx_dict.pop('prod', None)
    flx_dict.pop('sub', None)
    flx_dict.pop('base', None)

    return flx_dict