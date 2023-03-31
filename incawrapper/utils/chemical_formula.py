import re
from typing import Dict
import collections


def _create_compound_dict(
    formula: str,
) -> Dict[str, int]:
    idxs = [idx for idx in range(len(formula)) if formula[idx].isupper()]
    idxs.append(len(formula))
    compound_dict = {}
    for i in range(len(idxs) - 1):
        substring = formula[idxs[i] : idxs[i + 1]]
        element = "".join(re.split("[^a-zA-Z]*", substring))
        if any([idx for idx in range(len(substring)) if substring[idx].isnumeric()]):
            # This element has a multiplier
            multiplier = "".join(re.split("[^r'\d+']", substring))
            compound_dict[element] = int(multiplier)
        else:
            # This element has no multiplier
            compound_dict[element] = 1

    return compound_dict


def create_formula_from_dict(formula_dict: Dict[str, int]) -> str:
    formula = ""
    for element in formula_dict:
        if formula_dict[element] > 1:
            formula += f"{element}{formula_dict[element]}"
        elif formula_dict[element] == 0:
            continue
        else:
            formula += f"{element}"

    return formula


def subtract_formula(
    formula: str,
    subtract_formula: str,
):
    compound_dict = _create_compound_dict(formula)
    subtracted_dict = _create_compound_dict(subtract_formula)

    if not set(subtracted_dict.keys()).issubset(set(compound_dict.keys())):
        raise ValueError(
            "The subtracted formula contains elements that are not in the original formula"
        )

    for element in subtracted_dict:
        if element in compound_dict:
            compound_dict[element] = int(compound_dict[element]) - int(
                subtracted_dict[element]
            )
    new_formula = ""
    for element in compound_dict:
        if int(compound_dict[element]) > 1:
            new_formula += f"{element}{compound_dict[element]}"
        elif int(compound_dict[element]) == 0:
            continue
        else:
            new_formula += f"{element}"

    return new_formula


def get_unlabelled_atom_ids(molecular_formula: str, labelled_atom_ids: str) -> str:
    """
    Get the unlabelled atoms in a molecule by substrating the labelled atoms.

    Parameters
    ----------
    molecular_formula: str
        The molecular formula of the molecule.
    labelled_atom_ids: str
        The labelled atoms in the molecule.

    Returns
    -------
    unlabelled_atom_ids: str
        A molecular formula string of the unlabelled atoms.
    """

    labelled_atom_ids_formula = create_formula_from_dict(
        collections.Counter(labelled_atom_ids)
    )
    unlabelled_atom_ids_formula = subtract_formula(
        molecular_formula,
        labelled_atom_ids_formula,
    )

    return unlabelled_atom_ids_formula



__all__ = ["subtract_formula", "create_formula_from_dict", "get_unlabelled_atom_ids"]