"""INCA input parser.
Methods to prepare input data to fit the BFAIR INCA tools format.
"""

import cobra
import pandas as pd
from molmass.molmass import Formula


def parse_cobra_model(model_file_name, model_id, date):
    """
    Parses reaction- and metabolite information out of a cobra model saved
    as a .json or .sbml file and makes it compatible with the
    BFAIR.INCA tools

    Parameters
    ----------
    model_file_name : str or path + str
        Filename or path to file + filename of the cobra metabolic model
    model_id : str
        Name of the model (for downstream reference)
    date : str
        Date of model processing (for downstream reference)

    Returns
    -------
    model_data : pandas.DataFrame
        General information about the processed metabolic model
    reaction_data : pandas.DataFrame
        Information about the reactions in the metabolic model
    metabolite_data : pandas.DataFrame
        Information about the metabolites in the metabolic model

    Raises
    ------
    FileTypeError
        File provided is not a .json or a .sbml file
    """
    cobra_model = None
    # check for the file type
    if ".json" in model_file_name:
        filetype = "json"
        # Read in the json file
        cobra_model = cobra.io.load_json_model(model_file_name)
        (
            model_data,
            reaction_data,
            metabolite_data,
        ) = _parse_json_sbml_cobra_model(
            cobra_model, model_id, date, model_file_name, filetype
        )
    elif ".sbml" in model_file_name:
        filetype = "sbml"
        # Read in the sbml file and define the model conditions
        cobra_model = cobra.io.read_sbml_model(model_file_name)
        (
            model_data,
            reaction_data,
            metabolite_data,
        ) = _parse_json_sbml_cobra_model(
            cobra_model, model_id, date, model_file_name, filetype
        )
    else:
        raise TypeError("File type not supported, must be'.json' or '.sbml'.")
    return model_data, reaction_data, metabolite_data


def _parse_json_sbml_cobra_model(
    cobra_model, model_id, date, model_file_name, filetype
):
    """
    Helper function for parse_cobra_model(), parses reaction- and metabolite
    information out of an already loaded cobra model

    Parameters
    ----------
    cobra_model : cobra.Model
        Cobra metabolic model as loaded by the file type specific import
        function
    model_id : str
        Name of the model (for downstream reference)
    date : str
        Date of model processing (for downstream reference)
    model_file_name : str or path + str
        Filename or path to file + filename of the cobra metabolic model
    filetype : str
        Extension of the provided file

    Returns
    -------
    model_data : pandas.DataFrame
        General information about the processed metabolic model
    reaction_data : pandas.DataFrame
        Information about the reactions in the metabolic model
    metabolite_data : pandas.DataFrame
        Information about the metabolites in the metabolic model
    """
    # Pre-process the model file information
    with open(model_file_name, "r", encoding="utf-8") as f:
        model_file = f.read()
    # parse out model data
    model_data = pd.DataFrame(
        {
            "model_id": model_id,
            "date": date,
            "model_description": cobra_model.description,
            "model_file": model_file,
            "file_type": filetype,
        },
        index=[0],
    )
    # parse out reaction data
    reaction_data_temp = {}
    for cnt, r in enumerate(cobra_model.reactions):
        reaction_data_dict = {
            "model_id": model_id,
            "rxn_id": r.id,
            "rxn_name": r.name,
            "equation": r.build_reaction_string(),
            "subsystem": r.subsystem,
            "gpr": r.gene_reaction_rule,
            "genes": [g.id for g in r.genes],
            "reactants_stoichiometry": [
                r.get_coefficient(react.id) for react in r.reactants
            ],
            "reactants_ids": [react.id for react in r.reactants],
            "products_stoichiometry": [
                r.get_coefficient(prod.id) for prod in r.products
            ],
            "products_ids": [prod.id for prod in r.products],
            "lower_bound": r.lower_bound,
            "upper_bound": r.upper_bound,
            "objective_coefficient": r.objective_coefficient,
            "flux_units": "mmol*gDW-1*hr-1",
            "reversibility": r.reversibility,
            "used_": True,
        }
        reaction_data_temp[cnt] = reaction_data_dict
    reaction_data = pd.DataFrame.from_dict(reaction_data_temp, "index")
    # parse out metabolite data
    metabolite_data_tmp = {}
    for cnt, met in enumerate(cobra_model.metabolites):
        # Pre-process formulas using FIA-MS database methods
        if is_valid(met):
            formula = Formula(met.formula)
            formula = str(formula)
        else:
            formula = None
        # set up part of temp dict to transform into df later
        metabolite_data_dict = {
            "model_id": model_id,
            "met_name": met.name,
            "met_id": met.id,
            "formula": formula,
            "charge": met.charge,
            "compartment": met.compartment,
            "bound": met._bound,
            "annotations": met.annotation,
            "used_": True,
        }
        metabolite_data_tmp[cnt] = metabolite_data_dict
    metabolite_data = pd.DataFrame.from_dict(metabolite_data_tmp, "index")

    return model_data, reaction_data, metabolite_data


def is_valid(metabolite, INVALID_FORMULA_STR=["(", "Generic", "R", "X"]):
    """
    The validity of the input metabolites is checked. It's invalid if it
    does not have any formula annotated or if the formula includes previously
    defined invalid symbols
    Svetlana Kutozova wrote this function

    Parameters
    ----------
    metabolite : cobra.Metabolite
        A metabolite in the cobra format including additional information
        (formula, charge, elements)
    INVALID_FORMULA_STR : list
        A list of previously defined invalid symbol strings
    Returns
    -------
    boolean
        Valid or invalid metabolite
    """
    if not metabolite.formula:
        return False
    for string in INVALID_FORMULA_STR:
        if string in metabolite.formula:
            return False
    return True
