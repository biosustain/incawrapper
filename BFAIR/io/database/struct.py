"""Struct.

Contains basic functions to read, merge, and write FIA MS struct files.
"""

__all__ = ["from_inchis", "from_products_dict", "merge", "read", "write"]

import re
from collections import namedtuple

import pandas as pd
from rdkit import Chem

_CHARGE_REGEX = re.compile(r"((?:\+|-)\d*)$")
FILE_COLUMNS = ["id", "formula", "unused_smiles", "unused_inchi"]

Row = namedtuple("StructRow", FILE_COLUMNS)


def from_inchis(inchi_data, inchi_label="inchi"):
    """
    Creates a struct file from InChI data.

    Parameters
    ----------
    inchi_data : pandas.DataFrame
        Dataframes containing one column of InChI depictions and an index with metabolite names/IDs.
    inchi_label : str
        Name of the column containing the InChI depictions.

    Returns
    -------
    struct : pandas.DataFrame
    """
    rows = []
    for name, inchi in inchi_data[inchi_label].items():
        mol = Chem.MolFromInchi(inchi)
        # Force remove charge from formula
        # NOTE: molecules are already neutralized, so charge that is removed here cannot be removed without altering a
        #       covalent bond (e.g., a 4-coordinate N won't have neutral charge, unless one bond is undone).
        formula = _CHARGE_REGEX.sub("", Chem.rdMolDescriptors.CalcMolFormula(mol))
        smiles = Chem.MolToSmiles(mol)
        rows.append(Row(name, formula, smiles, inchi))
    return pd.DataFrame(rows)


def from_products_dict(results, prefix="p"):
    """
    Translates raw results from rule simulations into a FIA MS struct file.

    Parameters
    ----------
    results : dict
        Dictionary of (name/ID, products) pairs. Values being the output of `RuleLibrary.list_products`.
    prefix : str
        Prefix used to create IDs for each product. IDs will take the form "prefix_id".

    Returns
    -------
    struct : pandas.DataFrame

    See Also
    --------
    RuleLibrary.list_products
    """
    flat_results = [(prefix + "_" + source_metabolite, inchi)
                    for source_metabolite, product_list in results.items()
                    for inchi in product_list]
    inchi_data = pd.DataFrame(flat_results, columns=["id", "inchi"]).set_index("id")
    return from_inchis(inchi_data, "inchi")


def merge(struct_a, struct_b):
    """
    Merges two struct files.

    Parameters
    ----------
    struct_a, struct_b : pandas.DataFrame
        Dataframes containing 4 columns of metabolite ID, formula, SMILES, and InChI.

    Returns
    -------
    struct : pandas.DataFrame
    """
    return struct_a.append(struct_b, ignore_index=True)


def rename_metabolites(struct, prefix="p"):
    """
    Renames all metabolite IDs that have the same prefix, so they can be distinguished.

    Parameters
    ----------
    struct : pandas.DataFrame
        Dataframe containing 4 columns of metabolite ID, formula, SMILES, and InChI.
    prefix : str
        Prefix. Renamed IDs will follow the format "prefix_id".

    Notes
    -----
    This operation is destructive (i.e., occurs in place).
    """
    id_colname = FILE_COLUMNS[0]
    count = (struct.groupby(id_colname).cumcount() + 1).astype(str)
    prefix_mask = struct[id_colname].str.startswith(prefix + "_")
    struct.loc[prefix_mask, id_colname] = (
        prefix + count[prefix_mask] + "_" + struct[prefix_mask][id_colname].str.slice(len(prefix_mask) + 1)
    )


def read(pathname):
    """
    Reads a FIA MS struct file.

    Parameters
    ----------
    pathname : Path or str
        Pathname corresponding to a FIA MS struct file in TSV format.

    Returns
    -------
    pandas.DataFrame
        Dataframe containing 4 columns of metabolite ID, formula, SMILES, and InChI.
    """
    return pd.read_csv(pathname, names=FILE_COLUMNS, delimiter="\t")


def write(struct, pathname):
    """
    Writes a struct file to disk.

    Parameters
    ----------
    struct : pandas.DataFrame
        Dataframe containing 4 columns of metabolite ID, formula, SMILES, and InChI.
    """
    struct.to_csv(pathname, sep="\t", index=None, header=None)
