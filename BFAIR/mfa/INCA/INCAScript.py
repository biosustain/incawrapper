#%%
from typing import Literal
import pathlib


class INCAScript:
    def __init__(self):
        self.reaction = "% REACTION BLOCK\n"
        self.tracers = "% TRACERS BLOCK\n"
        self.fluxes = "% FLUXES BLOCK\n"
        self.ms_fragments = "% MS_FRAGMENTS BLOCK\n"
        self.pool_sizes = "% POOL_SIZES BLOCK\n"
        self.experimental_data = "% EXPERIMENTAL_DATA BLOCK\n"
        self.options = "% OPTIONS BLOCK\n"
        self.model = "% MODEL BLOCK\n"

        # The user is not intented to change these blocks
        self._verify_model = (
            "m.rates.flx.val = mod2stoich(m); % make sure the fluxes are feasible"
        )
        self.runner = "% RUNNER BLOCK\n"

    def add_to_block(
        self,
        block_name: Literal["reactions", "tracers", "fluxes", "ms_fragments", "pool_sizes", "experiments", "options", "model", "runner"],
        matlab_script_block: str,
    ):
        """Add a matlab script block to a specific block of the INCA script.
        This block workflow ensures that the structure of the INCA script is
        correct."""
        if block_name == "reactions":
            self.reaction += matlab_script_block
        elif block_name == "tracers":
            self.tracers += matlab_script_block
        elif block_name == "fluxes":
            self.fluxes += matlab_script_block
        elif block_name == "ms_fragments":
            self.ms_fragments += matlab_script_block
        elif block_name == "pool_sizes":
            self.pool_sizes += matlab_script_block
        elif block_name == "experiments":
            self.experimental_data += matlab_script_block
        elif block_name == "options":
            self.options += matlab_script_block
        elif block_name == "model":
            self.model += matlab_script_block
        elif block_name == "runner":
            self.runner += matlab_script_block
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
                self.pool_sizes,
                self.experimental_data,
                self.model,
                self.options,
                self._verify_model,
                self.runner,
            ]
        )

    def save_script(self, filename: pathlib.Path):
        """Save the INCA script to a file."""
        self.generate_script()
        with open(filename, "w") as f:
            f.write(self.matlab_script)

    def __str__(self):
        self.generate_script()
        return self.matlab_script