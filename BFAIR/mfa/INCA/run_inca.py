import pathlib
import time
import tempfile
import matlab.engine
from BFAIR.mfa.INCA.INCA_script import INCA_script


def run_inca(
    inca_script: INCA_script,
    INCA_base_directory: pathlib.Path,
) -> None:
    """Run INCA with a given INCA script."""

    # Create a temporary folder to store the INCA script and the runner script
    # The temporary folder will be deleted after the script is run
    if type(INCA_base_directory) is not pathlib.Path:
        INCA_base_directory = pathlib.Path(INCA_base_directory)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = pathlib.Path(temp_dir)

        # Write the INCA script to a file
        script_filename = "inca_script.m"
        inca_script.save_script(temp_dir / script_filename)
        print(f"INCA script saved to {temp_dir / script_filename}.")

        # Run the INCA script
        start_time = time.time()
        print("Starting MATLAB engine...")
        eng = matlab.engine.start_matlab()
        eng.cd(str(INCA_base_directory.resolve()), nargout=0)
        eng.startup(nargout=0)
        eng.setpath(nargout=0)
        eng.cd(str(temp_dir.resolve()), nargout=0)
        _f = getattr(eng, str(script_filename.replace(".m", "")))
        _f(nargout=0)
        eng.quit()
        print("--- %s seconds -" % (time.time() - start_time))

