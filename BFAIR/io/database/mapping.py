"""Mapping.

Contains basic functions to read, merge, and write FIA MS mapping files.
"""

__all__ = ["from_struct", "merge", "read", "write"]

import csv
from collections import Iterable, namedtuple

import pandas as pd

from BFAIR.io.database.struct import FILE_COLUMNS as STRUCT_FILE_COLUMNS

FILE_COLUMNS = ["unused_mass", "formula", "ids"]

Row = namedtuple("MappingRow", FILE_COLUMNS)


def _get_metadata(df, attr_name):
    # Extracts metadata from a dataframe and raises exception if not found.
    try:
        return df.attrs[attr_name]
    except KeyError:
        raise ValueError(f"Attribute '{attr_name}' missing.")


def from_struct(struct, database_name=None, database_version=None):
    """
    Creates a mapping file from a struct file.

    Parameters
    ----------
    struct : pandas.DataFrame
        Dataframe containing 4 columns of metabolite ID, formula, SMILES, and InChI.
    database_name : str
        Name of the mapping file.
    database_version : str
        Version of the mapping file.

    Returns
    -------
    mapping : pandas.DataFrame
    """
    mapping = pd.DataFrame([
        Row(0, formula, group[STRUCT_FILE_COLUMNS[0]].tolist())
        for formula, group in struct.groupby(FILE_COLUMNS[1])
    ])
    if database_name is not None:
        mapping.attrs["database_name"] = database_name
    if database_version is not None:
        mapping.attrs["database_version"] = database_version
    return mapping


def merge(mapping_a, mapping_b):
    """
    Merges two mapping files.

    Parameters
    ----------
    mapping_a, mapping_b : pandas.DataFrame
        Dataframes containing 3 columns of mass, formula, and metabolite IDs.

    Returns
    -------
    pandas.DataFrame
    """
    mapping_merged = mapping_a.merge(mapping_b.iloc[:, 1:], how="outer", on=FILE_COLUMNS[1])
    rows = []
    dup_colname = FILE_COLUMNS[2]
    for left_list, right_list in zip(
        mapping_merged[dup_colname + "_x"], mapping_merged[dup_colname + "_y"]
    ):
        row = []
        if isinstance(left_list, Iterable):
            row.extend(left_list)
        if isinstance(right_list, Iterable):
            row.extend([item for item in right_list if item not in row])
        rows.append(row)
    mapping_merged[FILE_COLUMNS[0]] = 0
    mapping_merged[dup_colname] = rows
    return mapping_merged[FILE_COLUMNS]


def read(pathname):
    """
    Reads a FIA MS mapping file.

    Parameters
    ----------
    pathname : Path or str
        Pathname corresponding to a FIA MS mapping file in TSV format.

    Returns
    -------
    pandas.DataFrame
        Dataframe containing 3 columns of mass, formula, and metabolite IDs.
    """
    database_name = ""
    database_version = ""
    rows = []
    with open(pathname, "r") as file:
        reader = csv.reader(file, delimiter="\t")
        database_name = next(reader)[1]
        database_version = next(reader)[1]
        for line in reader:
            # elements 2 onwards are metabolite IDs
            ids = [*filter(bool, line[2:])]
            rows.append([0, line[1], ids])
    mapping = pd.DataFrame(rows, columns=FILE_COLUMNS)
    mapping.attrs["database_name"] = database_name
    mapping.attrs["database_version"] = database_version
    return mapping


def write(mapping, pathname, database_name=None, database_version=None):
    """
    Writes a mapping file to disk.

    Parameters
    ----------
    mapping : pandas.DataFrame
        Dataframe containing 3 columns of mass, formula, and metabolite IDs.
    pathname : Path or str
        Destination pathname.
    database_name : str
        Name of the mapping file.
    database_version : str
        Version of the mapping file.

    Raises
    ------
    ValueError
        If `database_name` or `database_version` are not provided and cannot be found as metadata attributes of the
        input dataframe.
    """
    if database_name is None:
        database_name = _get_metadata(mapping, "database_name")
    if database_version is None:
        database_version = _get_metadata(mapping, "database_version")
    with open(pathname, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter="\t")
        writer.writerow(["database_name", database_name])
        writer.writerow(["database_version", database_version])
        for row in mapping.itertuples(index=False, name=None):
            writer.writerow([*row[:2], *row[2]])
