#%%
from typing import Literal
import pathlib


class INCA_script:
    def __init__(self):
        self.reaction = "% REACTION BLOCK\n"
        self.tracers = "% TRACERS BLOCK\n"
        self.fluxes = "% FLUXES BLOCK\n"
        self.ms_fragments = "% MS_FRAGMENTS BLOCK\n"
        self.experimental_data = "% EXPERIMENTAL_DATA BLOCK\n"
        self.options = "% OPTIONS BLOCK\n"
        self.model = "% MODEL BLOCK\n"

        # The user is not intented to change these blocks
        self._verify_model = (
            "m.rates.flx.val = mod2stoich(m); % make sure the fluxes are feasible"
        )

    def add_to_block(
        self,
        matlab_script_block: str,
        block_name: Literal["reactions", "tracers", "fluxes", "ms_fragments", "experiments", "options"],
    ):
        """Add a matlab script block to a specific block of the INCA script.
        This block workflow ensures that the structure of the INCA script is
        correct. The blocks are: reaction, tracers, ms_fragments, experimental_data, options."""
        if block_name == "reactions":
            self.reaction += matlab_script_block
        elif block_name == "tracers":
            self.tracers += matlab_script_block
        elif block_name == "fluxes":
            self.fluxes += matlab_script_block
        elif block_name == "ms_fragments":
            self.ms_fragments += matlab_script_block
        elif block_name == "experiments":
            self.experimental_data += matlab_script_block
        elif block_name == "options":
            self.options += matlab_script_block
        elif block_name == "model":
            self.model += matlab_script_block
        else:
            print(
                f"Block name {block_name} not recognized. See type hints for possible block names."
            )

    def generate_script(self):
        """Generate the INCA script."""
        self.matlab_script = "\n\n".join(
            [
                "clear functions",
                self.reaction,
                self.tracers,
                self.fluxes,
                self.ms_fragments,
                self.experimental_data,
                self.options,
                self.model,
                self._verify_model,
            ]
        )

    def _generate_runner_script(
        self,
        output_filename: pathlib.Path,
        run_estimate: bool = True,
        run_simulation: bool = True,
        run_continuation: bool = False,
        run_montecarlo: bool = False,
    ) -> None:
        """
        Generate a MATLAB script that specifies operations to be performed with the model defined in the INCA script.

        Parameters
        ----------
        output_filename : pathlib.Path
            Path to the output file. The output file will be a .mat file.
        run_continuation : bool, optional
            Whether to run parameter continuation with the settings defined in the INCA script, default True.
        run_simulation : bool, optional
            Whether to run a simulation with the settings defined in the INCA script, default True.
            This is necessary for a fluxmap to be loaded into INCA.

        Returns
        -------
        None
        """
        if run_montecarlo:
            raise NotImplementedError("Monte Carlo sampling is not implemented yet.")

        estimation = "f = estimate(m);\n" if run_estimate else ""
        continuation = "f=continuate(f,m);\n" if run_continuation else ""
        simulation = (
            "s=simulate(m);\n" if run_simulation else ""
        )  # For a fluxmap to be loaded into INCA, the .mat file must have a simulation
        output = f"filename = '{output_filename}';\n"

        saving = "save(filename, "
        if run_estimate:
            saving += "'f', "
        if run_simulation:
            saving += "'s', "

        saving += "'m');\n"

        self.runner_script = estimation + continuation + simulation + output + saving

    def save_script(self, filename: pathlib.Path):
        """Save the INCA script to a file."""
        with open(filename, "w") as f:
            f.write(self.matlab_script)

    def save_runner_script(self, filename: pathlib.Path):
        """Save the INCA runner script to a file."""
        with open(filename, "w") as f:
            f.write(self.runner_script)
