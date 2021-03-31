"""I/O.

This module hosts functions to load cobra models and download remote data.
"""

__all__ = [
    "LOCAL_PATH",
    "create_model",
    "fetch_remote",
    "load_cbm",
    "load_data",
    "models",
    "remote_files",
    "thermo_models",
    "mapping",
    "struct"
]

from BFAIR.io.database import mapping, struct
from BFAIR.io.model_factory import load_cbm, load_data, create_model, models, thermo_models
from BFAIR.io.remote import LOCAL_PATH, fetch_remote, remote_files
