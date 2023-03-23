"""INCA tools.
Writes MATLAB scripts, executes them and reimports the data"""

from incawrapper.mfa.INCA.INCAScript_generator import (
    INCAScript,
    script_generator_descr,
)
from incawrapper.mfa.INCA.INCA_reimport import (
    INCA_reimport,
    reimport_descr,
)
from incawrapper.mfa.INCA.INCA_input_parser import parse_cobra_model

__version__ = "1.0.0"

__all__ = [
    "INCAScript",
    "INCA_reimport",
    "parse_cobra_model",
    "script_generator_descr",
    "reimport_descr",
]
