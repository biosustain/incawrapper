# Private module to obtain static path

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
        Path to the static folder.
    """
    # Output must be str to be compatible with cobra/pytfa
    return str(Path(static.__file__).parent.joinpath(*args))
