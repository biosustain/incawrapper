from typing import Literal
import pathlib
from collections import OrderedDict


class INCAScript:
    """Class that represents an INCA script. This class is used to create an script that contain all the
    information needed (model description, data, options, and runner) to run algorithms in INCA. The script
    is created by matlab code as strings to the individual blocks. The blocks are then combined to a full
    script. The use of blocks ensures that different parts of the script is executed in the correct order.

    Attributes
    ----------
    blocks: OrderedDict
        Dictionary that contains the blocks of the INCA script. The keys are the block names and the values are
        the matlab code as strings. Here is a list of the block names and their corresponding matlab code:

        * reactions: Here the reactions with their atom map are defined.
        * tracers: Here the tracers are defined.
        * fluxes: Here the flux measurements are defined.
        * ms_fragments: Here the mass spectrometry measurements are defined.
        * pool_sizes: Here the pool sizes measurements are defined.
        * experiments: Here the experiments are defined.
        * model: Here the model is defined.
        * model_modifications: Here the model modifications are defined.
        * options: Here the options are defined.
        * runner: Here the runner is defined.

    matlab_script: str
        Property that returns the full matlab script (all block combined) as a string.
    """

    def __init__(self):
        self.blocks = OrderedDict(
            reactions="% REACTION BLOCK\n",
            tracers="% TRACERS BLOCK\n",
            fluxes="% FLUXES BLOCK\n",
            ms_fragments="% MS_FRAGMENTS BLOCK\n",
            pool_sizes="% POOL_SIZES BLOCK\n",
            experiments="% EXPERIMENTAL_DATA BLOCK\n",
            model="% MODEL BLOCK\n",
            model_modifications="% MODEL MODIFICATIONS BLOCK\n",
            options="% OPTIONS BLOCK\n",
            _verify_model=(
                "mod2stoich(m); % make sure the fluxes are feasible"
            ),
            runner="% RUNNER BLOCK\n",
        )

    def add_to_block(
        self,
        block_name: Literal[
            "reactions",
            "tracers",
            "fluxes",
            "ms_fragments",
            "pool_sizes",
            "experiments",
            "options",
            "model",
            "model_modifications",
            "runner",
        ],
        matlab_script_block: str,
    ) -> None:
        """Add a matlab script block to a specific block of the INCA script.
        This block workflow ensures that the structure of the INCA script is
        correct.

        Parameters
        ----------
        block_name: Literal["reactions", "tracers", "fluxes", "ms_fragments", "pool_sizes", "experiments", "options", "model", "runner"]
            The name of the block to which the matlab script block should be added.
        matlab_script_block: str
            The matlab script as a string that should be added to the block.

        Returns
        -------
        None

        Raises
        ------
        KeyError
            If the block name is not recognized.
        """
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
        joint_blocks = "\n\n".join(["clear functions", *self.blocks.values()])
        return joint_blocks

    def save_script(self, filename: pathlib.Path):
        """Save the INCA script to a file."""
        with open(filename, "w") as f:
            f.write(self.matlab_script)

    def __str__(self):
        """Return the full matlab script as a string."""
        return self.matlab_script


__all__ = ["INCAScript"]
