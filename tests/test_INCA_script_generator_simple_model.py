import sys
import pathlib
import pandas as pd
import os
import dotenv
import logging
import pytest

os.chdir(dotenv.find_dotenv().replace(".env", ""))

from BFAIR.mfa.INCA import INCA_script  # noqa E402

# setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def inca_script():
    """Create an instance of the INCA_script class."""
    inca_script = INCA_script()
    return inca_script


@pytest.fixture
def modelReaction_data_simple():
    """Load the modelReaction_data_simple from the simple model."""
    modelReaction_data_I = pd.read_csv(
        os.path.join(
            "tests",
            "test_data",
            "MFA_modelInputsData",
            "simple_model",
            "modelReactions.csv",
        )
    )
    return modelReaction_data_I


@pytest.fixture
def atomMappingReactions_data_simple():
    """Load the atomMappingReactions_data from the simple model."""
    atomMappingReactions_data_I = pd.read_csv(
        os.path.join(
            "tests",
            "test_data",
            "MFA_modelInputsData",
            "simple_model",
            "atomMappingReaction2.csv",
        )
    )
    return atomMappingReactions_data_I


@pytest.fixture
def reaction_ids(
    inca_script, modelReaction_data_simple, atomMappingReactions_data_simple
):
    """The reaction ids are produced by the add_reactions_to_script function, 
    which is tested benieth, but they are also a require input for 
    .add_reaction_parameters therefore this fixture is produced."""
    _, reaction_ids = inca_script.add_reactions_to_script(
        modelReaction_data_simple, atomMappingReactions_data_simple
    )
    return reaction_ids

@pytest.fixture
def measuredFluxes_data_simple():
    """Load the measuredFluxes_data from the simple model."""
    measuredFluxes_data_I = pd.read_csv(
        os.path.join(
            "tests",
            "test_data",
            "MFA_modelInputsData",
            "simple_model",
            "measuredFluxes.csv",
        )
    )
    return measuredFluxes_data_I

def test_add_reactions_to_script(
    inca_script, modelReaction_data_simple, atomMappingReactions_data_simple
):
    """Test the add_reactions_to_script function against a simple model."""

    # Defines the expected reaction strings.
    # NB new lines and indentation with the string is important for passing the test
    expected_reaction_script = """r = reaction({... % define reactions
'1.0*A (C1:a C2:b C3:c) -> 1.0*B (C1:a C2:b C3:c) ';...
'1.0*B (C1:a C2:b C3:c) -> 1.0*D (C1:a C2:b C3:c) ';...
'1.0*B (C1:a C2:b C3:c) -> 1.0*C (C1:b C2:c) + 1.0*E (C1:a) ';...
'1.0*B (C1:a C2:b C3:c) + 1.0*C (C1:d C2:e) -> 1.0*D (C1:b C2:c C3:d) + 1.0*E (C1:a) + 1.0*E (C1:e) ';...
'1.0*D (C1:a C2:b C3:c) -> 1.0*F (C1:a C2:b C3:c) ';...
});\n\n"""

    expected_reaction_ids = ["R1", "R2", "R3", "R4", "R5"]

    reaction_script, reaction_ids = inca_script.add_reactions_to_script(
        modelReaction_data_I=modelReaction_data_simple,
        atomMappingReactions_data_I=atomMappingReactions_data_simple,
    )

    assert reaction_script == expected_reaction_script
    assert reaction_ids == expected_reaction_ids


def test_add_reaction_parameters(inca_script, modelReaction_data_simple, reaction_ids, measuredFluxes_data_simple):
    
    expected_script = """
% define lower bounds
m.rates.flx.lb = [...
99,...
0,...
0,...
0,...
0,...
];

%define upper bounds
m.rates.flx.ub = [...
101,...
1000,...
1000,...
1000,...
1000,...
];

% define flux vals
m.rates.flx.val = [...
100,...
0,...
0,...
0,...
0,...
];

% include/exclude reactions
m.rates.on = [...
true,...
true,...
true,...
true,...
true,...
];

% define reaction ids
m.rates.id = {...
'R1',...
'R2',...
'R3',...
'R4',...
'R5',...
};
"""

    script = inca_script.add_reaction_parameters(
        modelReaction_data_I=modelReaction_data_simple,
        measuredFluxes_data_I=measuredFluxes_data_simple,
        model_rxn_ids=reaction_ids,
    )

    assert script == expected_script

