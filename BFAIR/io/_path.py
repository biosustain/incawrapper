# Private module to obtain static path

__all__ = []

from pathlib import Path

from BFAIR.io import static


def static_path(*args) -> str:
    """
    Returns the path to the static folder.

    Parameters
    ----------
    *args
        Paths to append to the output.

    Returns
    -------
    str
    """
    # Output must be str to be compatible with cobra/pytfa
    return str(Path(static.__file__).parent.joinpath(*args))
