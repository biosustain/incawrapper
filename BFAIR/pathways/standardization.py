"""Standardization.

With this module, chemical compounds from varying formats can be standardized for compatibility with reaction rules.
This module borrows from the `rpchemtools <https://github.com/brsynth/rpchemtools>` toolbox by Jean-Loup Faulon's Lab.
"""

__all__ = ["standardize"]

from lazy_object_proxy import Proxy
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors

_NEUTRALIZE_PATTERNS = Proxy(
    lambda: [
        (Chem.MolFromSmarts(charged_pat), Chem.MolFromSmiles(uncharged_pat, False))
        for charged_pat, uncharged_pat in (
            ("[n+;H]", "n"),  # Imidazoles
            ("[N+;!H0]", "N"),  # Amines
            ("[$([O-]);!$([O-][#7])]", "O"),  # Carboxylic acids and alcohols
            ("[S-;X1]", "S"),  # Thiols
            ("[$([N-;X2]S(=O)=O)]", "N"),  # Sulfonamides
            ("[$([N-;X2][C,N]=C)]", "N"),  # Enamines
            ("[n-]", "[nH]"),  # Tetrazoles
            ("[$([S-]=O)]", "S"),  # Sulfoxides
            ("[$([N-]C=O)]", "N"),  # Amides
        )
    ]
)


def _transfer_props(source, target):
    # transfer properties from one molecule to another
    props = source.GetPropNames(includePrivate=False)
    if source.HasProp("_Name"):
        props.append("_Name")
    for prop in props:
        target.SetProp(prop, source.GetProp(prop))


def _commute_inchi(compound):
    # convert compound back and forth to InChI
    inchi = Chem.MolToInchi(compound, logLevel=None)
    new_compound = Chem.MolFromInchi(inchi, sanitize=False, removeHs=False, logLevel=None, treatWarningAsError=False)
    _transfer_props(compound, new_compound)
    return new_compound


def _neutralize_charge(compound):
    # neutralize charge of a compound according to predefined rules
    for charged_pat, uncharged_pat in _NEUTRALIZE_PATTERNS:
        while compound.HasSubstructMatch(charged_pat):
            compound = Chem.ReplaceSubstructs(compound, charged_pat, uncharged_pat)[0]
    compound.UpdatePropertyCache()
    Chem.SanitizeMol(compound, sanitizeOps=Chem.SanitizeFlags.SANITIZE_ALL, catchErrors=False)
    return compound


def _count_non_hs_atoms(compound):
    # counts the number of non-hydrogen atoms in a compound
    return len([atom for atom in compound.GetAtoms() if atom.GetAtomicNum() > 1])


def _strip_small_fragments(compound):
    # returns the biggest disconnected fragment from a molecule
    frags = Chem.GetMolFrags(compound, asMols=True, sanitizeFrags=False)
    if len(frags) > 1:
        # sort by number of non-hydrogen atoms and molecular weight
        biggest_frag = sorted(
            frags, key=lambda frag: (_count_non_hs_atoms(frag), Descriptors.MolWt(frag)), reverse=True
        )[0]
        _transfer_props(compound, biggest_frag)
        return biggest_frag
    return compound


def standardize(compound: AllChem.Mol, add_hs=True, remove_stereo=True, thorough=False) -> AllChem.Mol:
    """
    Standardizes an RDKit molecule by running various cleanup and sanitization operations.

    Parameters
    ----------
    compound : rdkit.Chem.rdchem.Mol
        A chemical compound.
    add_hs : bool
        If True, adds hydrogens to the compound.
    remove_stereo : bool
        If True, removes stereochemistry info from the compound.
    thorough : bool
        If True, removes charge, isotopes, and small fragments from the compound.

    Returns
    -------
    rdkit.Chem.rdchem.Mol
        The standardized compound.
    """
    # basic cleanup
    Chem.Cleanup(compound)
    Chem.SanitizeMol(compound, sanitizeOps=Chem.SanitizeFlags.SANITIZE_ALL, catchErrors=False)
    AllChem.AssignStereochemistry(compound, cleanIt=True, force=True, flagPossibleStereoCenters=True)

    # remove isotopes, neutralize charge
    if thorough:
        for atom in compound.GetAtoms():
            atom.SetIsotope(0)
        compound = _neutralize_charge(compound)
        Chem.SanitizeMol(compound, sanitizeOps=Chem.SanitizeFlags.SANITIZE_ALL, catchErrors=False)

    # remove stereochemistry
    if remove_stereo:
        Chem.RemoveStereochemistry(compound)

    # commute inchi
    compound = _commute_inchi(compound)

    # keep biggest fragment
    if thorough:
        compound = _strip_small_fragments(compound)
    Chem.SanitizeMol(compound, sanitizeOps=Chem.SanitizeFlags.SANITIZE_ALL, catchErrors=False)

    # neutralize charge
    compound = _neutralize_charge(compound)
    Chem.SanitizeMol(compound, sanitizeOps=Chem.SanitizeFlags.SANITIZE_ALL, catchErrors=False)

    # add protons
    if add_hs:
        return Chem.AddHs(compound, explicitOnly=False, addCoords=True)
    return compound
