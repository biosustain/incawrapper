"""Utils.

Toolbox of functions to parse chemical compounds and calculate similarity scores between them.
"""

__all__ = ["get_compound", "get_molecular_fingerprint", "calculate_similarity", "standardize"]

from rdkit import Chem
from rdkit.Chem import AllChem

from BFAIR.pathways.standardization import standardize


def get_compound(input_compound, input_type="inchi", **kwargs) -> AllChem.Mol:
    """
    Returns a standardized chemical compound.

    Parameters
    ----------
    input_compound : str or rdkit.Chem.rdchem.Mol
        String representation of a chemical compound or a RDKit molecule object.
    input_type : {'inchi', 'smiles', 'rdkit'}
        Type of notation describing the input compound.
    **kwargs
        Standardization parameters applied to the input compound, see `standardize`.

    Returns
    -------
    rdkit.Chem.rdchem.Mol
        A chemical compound.

    Raises
    ------
    ValueError
        If an unsupported input type is supplied.

    See Also
    --------
    standardize
    """
    if input_type == "inchi":
        compound = Chem.MolFromInchi(input_compound, sanitize=False)
    elif input_type == "smiles":
        compound = Chem.MolFromSmiles(input_compound, sanitize=False)
    elif input_type == "rdkit":
        if kwargs:
            compound = input_compound
        else:
            return input_compound
    else:
        raise ValueError(f"Unsupported input type: {input_type}. Must be InChI, SMILES or an RDKit molecule object.")
    return standardize(compound, **kwargs)


def get_molecular_fingerprint(input_compound, input_type="inchi", **kwargs):
    """
    Returns the extended-connectivity fingerprint of a compound.

    Parameters
    ----------
    input_compound : str or rdkit.Chem.rdchem.Mol
        String representation of a chemical compound or a RDKit molecule object.
    input_type : {'inchi', 'smiles', 'rdkit'}
        Type of notation describing the input compound.
    **kwargs
        Standardization parameters applied to the input compound, see `standardize`.

    Returns
    -------
    list of int
        A molecular fingerprint, represented as a list of indexes corresponding to present substructural features.


    See Also
    --------
    standardize
    """
    compound = get_compound(input_compound, input_type, **kwargs)
    return [
        *AllChem.GetMorganFingerprintAsBitVect(compound, 2, 1024, useFeatures=False, useChirality=False).GetOnBits()
    ]


def calculate_similarity(a_fingerprint, another_fingerprint):
    """
    Calculates the structural similarity score between two molecules.

    Parameters
    ----------
    a_fingerprint, another_fingerprint : list
        Input molecular fingerprints of two molecules.

    Returns
    -------
    float
        The Tanimoto coefficient, ranging from 0.0 to 1.0 (in which case both molecules are identical).
    """
    a, b = tuple(map(set, [a_fingerprint, another_fingerprint]))
    return len(a.intersection(b)) / len(a.union(b))
