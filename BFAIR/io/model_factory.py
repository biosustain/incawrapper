"""Model Factory.

This module hosts functions to load cobra models, create and adjust tFBA-ready models.
"""

__all__ = ["load_cbm", "load_data", "create_model", "models", "thermo_models"]

import logging
from pathlib import Path

from cobra import Model
from cobra.io import load_json_model
from pytfa import ThermoModel
from pytfa.io import load_thermoDB, read_lexicon, read_compartment_data, annotate_from_lexicon, apply_compartment_data
from pytfa.utils.logger import get_bistream_logger

from BFAIR.io._base import _BaseFactory
from BFAIR.io._path import static_path


class _ModelFactory(_BaseFactory):
    def __init__(self):
        super().__init__(load_cbm)
        self._list = [path.stem for path in Path(static_path()).glob("*.json")]


class _ThermoModelFactory(_BaseFactory):
    def __init__(self):
        super().__init__(create_model)
        self._list = [path.stem for path in Path(static_path()).glob("*.json") if path.with_suffix("").exists()]


def _silence_pytfa(logger_name):
    # Disables the stream logs produced by the pytfa module, keeps file logs
    logger = get_bistream_logger(logger_name)
    for handler in logger.handlers:
        if not isinstance(handler, logging.FileHandler):
            handler.setLevel(logging.ERROR)


def load_cbm(model_name) -> Model:
    """
    Load a JSON cobra model stored in the static folder.

    Parameters
    ----------
    model_name : str
        The name of the model.

    Returns
    -------
    cobra.Model
        The loaded cobra model.
    """
    return load_json_model(static_path(model_name + ".json"))


def load_data(model_name):
    """
    Loads pre-curated model-specific thermodynamic information.

    Parameters
    ----------
    model_name : str
        The name of a model.

    Returns
    -------
    thermo_data : dict
        A thermodynamic database.
    lexicon : pandas.DataFrame
        A dataframe linking metabolite IDs to SEED compound IDs.
    compartment_data : dict
        A dictionary with information about each compartment of the model.
    """
    thermo_data = load_thermoDB(static_path("thermo_data.thermodb"))
    lexicon = read_lexicon(static_path(model_name, "lexicon.csv"))
    compartment_data = read_compartment_data(static_path(model_name, "compartment_data.json"))
    return thermo_data, lexicon, compartment_data


def create_model(model_name, thermo_data=None, lexicon=None, compartment_data=None) -> ThermoModel:
    """
    Creates a tFBA-ready model.

    Parameters
    ----------
    model_name : str
        The name of a model.
    thermo_data : dict, optional
        A thermodynamic database. If specified, ``lexicon`` and ``compartment data`` are required.
    lexicon : pandas.DataFrame, optional
        A dataframe linking metabolite IDs to SEED compound IDs. If specified, ``thermo_data`` and ``compartment_data``
        are required.
    compartment_data : dict, optional
        A dictionary containing information about each compartment of the model. If specified, ``thermo_data`` and
        ``lexicon`` are required.

    Returns
    -------
    pytfa.ThermoModel
        A thermodynamic database.

    Raises
    ------
    ValueError
        If any (but not all) of ``thermo_data``, ``lexicon``, and ``compartment_data`` is None.
    """
    data_is_none = [data is None for data in [thermo_data, lexicon, compartment_data]]
    if all(data_is_none):
        thermo_data, lexicon, compartment_data = load_data(model_name)
    elif any(data_is_none):
        raise ValueError("Not all required data supplied.")

    # due to a bug on pytfa, the logger is created with "None" as name
    _silence_pytfa(f"thermomodel_{None}")
    # however, if the model ends up being copied the correct name will be used, so this logger should be silenced too
    _silence_pytfa(f"thermomodel_{model_name}")

    cmodel = load_cbm(model_name)
    tmodel = ThermoModel(thermo_data, cmodel)
    tmodel.name = model_name

    annotate_from_lexicon(tmodel, lexicon)
    apply_compartment_data(tmodel, compartment_data)

    if tmodel.solver.interface.__name__ == "optlang.gurobi_interface":
        tmodel.solver.problem.Params.NumericFocus = 3
    tmodel.solver.configuration.tolerances.feasibility = 1e-9
    tmodel.solver.configuration.presolve = True

    tmodel.prepare()
    tmodel.convert(verbose=False)

    return tmodel


models = _ModelFactory()
"""A factory class to load metabolic models.

Examples
--------
>>> from BFAIR.io import models

Use the ``dir`` function to obtain a list of available models.

>>> dir(models)
['iJO1366', 'small_ecoli', 'yeastGEM']

Models can be loaded by accessing them as class attributes.

>>> model = models.small_ecoli
>>> model.slim_optimize()
0.8109621653343296

This is equivalent to ``load_cbm("small_ecoli")``.
"""


thermo_models = _ThermoModelFactory()
"""A factory class to create pre-curated thermodynamics-based metabolic models.

Examples
--------
>>> from BFAIR.io import thermo_models

Use the ``dir`` function to obtain a list of available models.

>>> dir(models)
['iJO1366', 'small_ecoli']

Models can be loaded by accessing them as class attributes.

>>> tmodel = thermo_models.small_ecoli
>>> tmodel.slim_optimize()
0.8109972502600706

This is equivalent to ``create_model("small_ecoli")``.
"""
