import pathlib
import time
import tempfile
import matlab.engine
from incawrapper.mfa.INCA.INCAScript import INCAScript


def run_inca(
    inca_script: INCAScript,
    INCA_base_directory: pathlib.Path,
    execution_directory: pathlib.Path = None,
) -> None:
    """Run INCA with a given INCA script in either a temporary directory or a specified directory.
    
    Parameters
    ----------
    inca_script : INCAScript
        The INCA script to run.
    INCA_base_directory : pathlib.Path
        The path to the INCA base directory, i.e. the directory that contains the INCA executable.
    exercution_directory : pathlib.Path, optional
        The path to the directory where the INCA script will be run. If None, the script will be run in a temporary directory, by default None.
        If a directory is specified, the INCA script along with other output files (e.g. montecarlo dump.mat) will be saved in the directory.
    
    Returns
    -------
    None"""

    # Check if the INCA base directory is a pathlib.Path object
    if type(INCA_base_directory) is not pathlib.Path:
        INCA_base_directory = pathlib.Path(INCA_base_directory)

    if execution_directory is None:
        # Run the INCA script in a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = pathlib.Path(temp_dir)
            _exercute_inca(inca_script, INCA_base_directory, temp_dir)
    else:
        # Check if the exercution directory is a pathlib.Path object
        if type(execution_directory) is not pathlib.Path:
            execution_directory = pathlib.Path(execution_directory)
        
        # Run the INCA script in the specified directory
        _exercute_inca(inca_script, INCA_base_directory, execution_directory)


def _exercute_inca(inca_script: INCAScript, INCA_base_directory:pathlib.Path, dir: pathlib.Path):
    """Run INCA with a given INCA script in a specified directory. This function is not intended to be called directly, 
    but rather through the run_inca function."""

    # Write the INCA script to a file
    script_filename = "inca_script.m"
    inca_script.save_script(dir / script_filename)
    print(f"INCA script saved to {dir / script_filename}.")

    # Run the INCA script
    start_time = time.time()
    print("Starting MATLAB engine...")
    eng = matlab.engine.start_matlab()
    eng.cd(str(INCA_base_directory.resolve()), nargout=0)
    eng.startup(nargout=0)
    eng.setpath(nargout=0)
    eng.cd(str(dir.resolve()), nargout=0)
    _f = getattr(eng, str(script_filename.replace(".m", "")))
    _f(nargout=0)
    eng.quit()
    print("--- %s seconds -" % (time.time() - start_time))