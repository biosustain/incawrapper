# identify inversed reactions
import collections
import pandas as pd
import pandera as pa
import incawrapper.core.dataschemas as dataschemas

class Reaction():
    """Class to parse a reaction string into reactants and products. Only used for detection
    of inverse reactions."""
    def __init__(self, eqn):
        self.eqn = eqn
        self.reactants = []
        self.products = []
        self.parse_eqn()
        
    def parse_eqn(self):
        self.reactants = [r.strip() for r in self.eqn.split("->")[0].split("+")]
        self.products = [r.strip() for r in self.eqn.split("->")[1].split("+")]
        
    def __repr__(self):
        return f"{self.eqn}"
    
    def is_inverse(self, other):
        """Check if the reaction is the inverse of another reaction."""
        return (
            collections.Counter(self.reactants) == collections.Counter(other.products) and
            collections.Counter(self.products) == collections.Counter(other.reactants)
        )

@pa.check_io(dataschemas.ReactionsSchema)
def merge_reaverible_reaction(rxn_df: dataschemas.ReactionsSchema):
    """Merge reversible reactions into a single reaction. This is done by comparing
    strings separated by "+" and "->". Thus, it will not work for reactions with
    that are not specified in the same way, e.g. "2 A + B -> C" will not be merged
    with "C -> A + A + B". Similar the atom mapping has to be an exact match, e.g. 
    "A (ab) + B (cd) -> C (abcd)" will not be merged with "C (efgf) -> A (ef) + B (gh)", 
    even though these reaction actually are the reversed of one another.
    
    Parameters
    ----------
    rxn_df : pandas.DataFrame
        DataFrame with reaction equations. Must cohere to the ReactionsSchema.
    
    Returns
    -------
    pandas.DataFrame
        DataFrame with merged reversible reactions."""
    n_merged = 0
    rxn_df = rxn_df.copy()
    for i, row in rxn_df.iterrows():
        if row["rxn_eqn"] != "":
            rxn = Reaction(row["rxn_eqn"])
        else:
            continue
        for j, row2 in rxn_df[i+1:].iterrows():
            if i != j and row2["rxn_eqn"] != "":
                rxn2 = Reaction(row2["rxn_eqn"])
                if rxn.is_inverse(rxn2):
                    print(f"Found inverse reaction: {rxn} and {rxn2}")
                    rxn_df.loc[i, "rxn_eqn"] = rxn.eqn.replace("->", "<->")
                    rxn_df.loc[j, "rxn_eqn"] = ""
                    n_merged += 1
                    break
    print(f"Merged {n_merged} reactions")
    return rxn_df[rxn_df['rxn_eqn'] != '']

__all__ = ["merge_reaverible_reaction"]