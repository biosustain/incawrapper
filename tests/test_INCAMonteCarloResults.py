import pytest
import pathlib
import os 
from incawrapper.core.INCAMonteCarloResults import INCAMonteCarloResults

current_dir = str(pathlib.Path(__file__).parent.absolute())


def test_load_dump_file():
    """
    Tests that the dump file is loaded correctly.
    """
    mcfile = pathlib.Path("tests/test_data/dump.mat")
    mcres = INCAMonteCarloResults(mcfile, ["A", "B", "C", "D", "E", "F", "G"])
    assert mcres.samples.shape == (100, 7)
    assert mcres.ci.shape == (2, 7)


def test_load_finished_file():
    """
    Tests that the finished file is loaded correctly.
    """
    mcfile = pathlib.Path("tests/test_data/simple_model_mc_tutorial_mc.mat")
    mcres = INCAMonteCarloResults(mcfile, ["A", "B", "C", "D", "E", "F", "G"])
    assert mcres.samples.shape == (500, 7)
    assert mcres.ci.shape == (2, 7)


def test_FileNotFound():
    """
    Tests that the FileNotFoundError is raised when the file is not found.
    """
    mcfile = pathlib.Path("tests/test_data/non_existing_file.mat")

    with pytest.raises(FileNotFoundError):
        INCAMonteCarloResults(mcfile, ["A", "B", "C", "D", "E", "F", "G"])
        