import pytest
from incawrapper.core.INCAScript import INCAScript

def test_INCAScript_initialises():
    """Test that INCAScript initialises correctly and is an instance of INCAScript"""
    inca_script = INCAScript()
    assert isinstance(inca_script, INCAScript)


def test_order_of_blocks():
    """Test that the blocks are in the correct order. This is important for the
    the script to work as the script is generated with certain assumption about
    the order of the blocks. The blocks have to obey the following order:
    1. reactions, tracers, fluxes, ms_fragments, and pool_sizes blocks
    2. experiments block
    3. model block 
    4. model_modifications block
    5. options block
    6. runner block"""
    inca_script = INCAScript()

    def get_block_index(block_names: list)->list:
        """Get the index of the block in the OrderedDict"""
        return [list(inca_script.blocks.keys()).index(block_name) for block_name in block_names] 

    # test that the blocks are in the correct order
    assert get_block_index(["reactions", "tracers", "fluxes", "ms_fragments", "pool_sizes"]) < get_block_index(["experiments"])
    assert get_block_index(["experiments"]) < get_block_index(["model"])
    assert get_block_index(["model"]) < get_block_index(["model_modifications"])
    assert get_block_index(["model_modifications"]) < get_block_index(["options"])
    assert get_block_index(["options"]) < get_block_index(["runner"])


def test_INCAScript_matlab_script():
    """Test that the matlab script is generated."""
    inca_script = INCAScript()
    expected = """clear functions

% REACTION BLOCK


% TRACERS BLOCK


% FLUXES BLOCK


% MS_FRAGMENTS BLOCK


% POOL_SIZES BLOCK


% EXPERIMENTAL_DATA BLOCK


% MODEL BLOCK


% MODEL MODIFICATIONS BLOCK


% OPTIONS BLOCK


mod2stoich(m); % make sure the fluxes are feasible

% RUNNER BLOCK
"""
    assert  inca_script.matlab_script == expected


def test_INCAScript_add_to_block():
    """Test that the add_to_block method adds a string to the correct block"""
    inca_script = INCAScript()
    inca_script.add_to_block("reactions", "string added to block")
    expected = """% REACTION BLOCK
string added to block"""
    assert inca_script.blocks['reactions'] == expected


def test_INCAScript_add_to_block_keyerror():
    """Test that the add_to_block method raises a KeyError if an incorrect 
    block name is provided"""
    inca_script = INCAScript()
    with pytest.raises(KeyError):
        inca_script.add_to_block("not a block", "string added to block")