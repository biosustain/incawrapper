import pytest
import pathlib
import os 
from BFAIR.mfa.INCA.INCAMonteCarloResults import INCAMonteCarloResults

current_dir = str(pathlib.Path(__file__).parent.absolute())


def test_load_dump_file():
    """
    Tests that the dump file is loaded correctly.
    """
    mcfile = pathlib.Path("tests/test_data/dump.mat")
    mcres = INCAMonteCarloResults(mcfile, ["A", "B", "C", "D", "E", "F", "G"])
    assert mcres.samples.shape == (100, 7)
    assert mcres.ci.shape == (2, 7)

