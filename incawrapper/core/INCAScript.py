#%%
from typing import Literal
import pathlib
from collections import OrderedDict


class INCAScript:
    def __init__(self):
        self.blocks = OrderedDict(
            reactions = "% REACTION BLOCK\n",
            tracers = "% TRACERS BLOCK\n",
            fluxes = "% FLUXES BLOCK\n",
            ms_fragments = "% MS_FRAGMENTS BLOCK\n",
            pool_sizes = "% POOL_SIZES BLOCK\n",
            experiments = "% EXPERIMENTAL_DATA BLOCK\n",
            model = "% MODEL BLOCK\n",
            _verify_model = (
                "m.rates.flx.val = mod2stoich(m); % make sure the fluxes are feasible"
            ),
            model_modifications = "% MODEL MODIFICATIONS BLOCK\n",
            options = "% OPTIONS BLOCK\n",
            runner = "% RUNNER BLOCK\n",
        )


    def add_to_block(
        self,
        block_name: Literal["reactions", "tracers", "fluxes", "ms_fragments", "pool_sizes", "experiments", "options", "model", "runner"],
        matlab_script_block: str,
    ):
        """Add a matlab script block to a specific block of the INCA script.
        This block workflow ensures that the structure of the INCA script is
        correct."""
        try:
            self.blocks[block_name] += matlab_script_block
        except KeyError:
            raise KeyError(
                f"Block name {block_name} not recognized. See type hints for possible block names."
            )

    @property
    def matlab_script(self):
        """Property that returns the full matlab script (all block combined) as a 
        string."""
        joint_blocks = "\n\n".join(
            [
                "clear functions",
                *self.blocks.values()
            ]
        )
        return joint_blocks


    def save_script(self, filename: pathlib.Path):
        """Save the INCA script to a file."""
        with open(filename, "w") as f:
            f.write(self.matlab_script)

    def __str__(self):
        return self.matlab_script