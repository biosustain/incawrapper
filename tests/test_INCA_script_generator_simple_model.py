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
def atomMappingMetabolites_symmetric_metabolite():
    """A dataFrame which contains a symmetric metabolite used to test
    correct parsing symmetric metabolites from the atomMappingMetabolites
    file."""

    data = [
        {
            "id": 1,
            "mapping_id": "simple_model",
            "met_id": "A",
            "met_elements": "{C,C,C}",
            "met_atompositions": "{0,1,2}",
            "met_symmetry_atompositions": "{3,2,1}",
            "met_symmetry_elements": "{C,C,C}",
            "used_": True,
            "comment_": pd.NA,
            "met_mapping": pd.NA,
            "base_met_ids": pd.NA,
            "base_met_elements": pd.NA,
            "base_met_atompositions": pd.NA,
            "base_met_symmetry_elements": pd.NA,
            "base_met_symmetry_atompositions": pd.NA,
            "base_met_indices": pd.NA,
        }
    ]
    return pd.DataFrame.from_records(data)


@pytest.fixture
def atomMappingMetabolites_data_simple():
    """Load the atomMappingMetabolite_data from the simple model."""
    atomMappingMetabolite_data_I = pd.read_csv(
        os.path.join(
            "tests",
            "test_data",
            "MFA_modelInputsData",
            "simple_model",
            "atomMappingMetabolites.csv",
        )
    )
    return atomMappingMetabolite_data_I


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


@pytest.fixture
def experimentalMS_data_simple():
    """Load the the experimentalMS_data from the simple model."""
    experimentalMS_data_I = pd.read_csv(
        os.path.join(
            "tests",
            "test_data",
            "MFA_modelInputsData",
            "simple_model",
            "experimentalMS.csv",
        )
    )
    return experimentalMS_data_I


@pytest.fixture
def fragments_used_simple(
    inca_script,
    experimentalMS_data_simple,
    tracers_data_simple,
    measuredFluxes_data_simple,
    atomMappingMetabolites_data_simple,
):
    """Fragments_used is produced by the add_experimental_parameters method,
    but the .mapping() method fragements_used as an input. Therefore a separate
    fixture is produced."""
    _, fragments_used = inca_script.add_experimental_parameters(
        experimentalMS_data_simple,
        tracers_data_simple,
        measuredFluxes_data_simple,
        atomMappingMetabolites_data_simple,
    )
    return fragments_used


@pytest.fixture
def tracers_data_simple():
    """Load the tracers from the simple model."""
    tracers_data_I = pd.read_csv(
        os.path.join(
            "tests",
            "test_data",
            "MFA_modelInputsData",
            "simple_model",
            "tracers.csv",
        )
    )
    return tracers_data_I


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


def test_add_reaction_parameters(
    inca_script, modelReaction_data_simple, reaction_ids, measuredFluxes_data_simple
):

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


def test_add_experiment_parameters(
    inca_script,
    experimentalMS_data_simple,
    tracers_data_simple,
    measuredFluxes_data_simple,
    atomMappingMetabolites_data_simple,
):
    """Test the add_experiment_parameters function against a simple model.
    This function has two outputs (script and fragments_used) both of which are tested."""

    # Defines the expected experiment script.
    # NB new lines and indentation with the string is important for passing the test
    expected_script = """
% define which fragments of molecules were measured in which experiment
d = msdata({...
'F1: F @ C1 C2 C3';
});

% initialize mass distribution vector
d.idvs = idv;

% define tracers used in the experiments
t = tracer({...
'[1-13C]A: A.EX @ C1';...
});

% define fractions of tracers used
t.frac = [ 1 ];

% define experiments for fit data
f = data(' R1 ');

% add fit values
f.val = [...
100,...
];
% add fit stds
f.std = [...
0.0001,...
];

% initialize experiment with t and add f and d
x = experiment(t);
x.data_flx = f;
x.data_ms = d;

% assing all the previous values to a specific experiment
m.expts(1) = x;

m.expts(1).id = {'exp1'};
"""

    expected_fragments_used = ["F1"]

    # Calling the function
    script, fragments_used = inca_script.add_experimental_parameters(
        experimentalMS_data_simple,
        tracers_data_simple,
        measuredFluxes_data_simple,
        atomMappingMetabolites_data_simple,
    )

    assert script == expected_script
    assert fragments_used == expected_fragments_used


def test_script_generator(
    inca_script,
    modelReaction_data_simple,
    atomMappingReactions_data_simple,
    atomMappingMetabolites_data_simple,
    measuredFluxes_data_simple,
    experimentalMS_data_simple,
    tracers_data_simple,
):
    """Test the script_generator function against a simple model."""
    script = inca_script.script_generator(
        modelReaction_data_simple,
        atomMappingReactions_data_simple,
        atomMappingMetabolites_data_simple,
        measuredFluxes_data_simple,
        experimentalMS_data_simple,
        tracers_data_simple,
    )
    # Generate updated test script:
    # inca_script.save_INCA_script(script=script, scriptname="testscript_simple")
    # Run the following in the terminal: mv ../testscript_simple.m test_data/MFA_modelInputsData/simple_model

    # read the testscript_simple file
    filename = os.path.join(
        "tests",
        "test_data",
        "MFA_modelInputsData",
        "simple_model",
        "testscript_simple.m",
    )
    with open(filename, "r") as f:
        expected_script = f.read()
    assert script == expected_script


def test_symmetrical_metabolites(
    inca_script, atomMappingMetabolites_symmetric_metabolite
):
    """Test if the add_symmetric_metabolites function correctly writes the matlab script."""

    # Defines the expected experiment script.
    # NB new lines and indentation with the string is important for passing the test
    expected_script = """% take care of symmetrical metabolites
m.mets{'A'}.sym = list('rotate180', atommap('C1:C4 C2:C3 C3:C2'));

"""
    script = inca_script.symmetrical_metabolites(
        atomMappingMetabolites_symmetric_metabolite
    )
    assert script == expected_script


def test_mapping(inca_script, experimentalMS_data_simple, fragments_used_simple):
    """Test if the add_mapping function correctly writes the matlab script."""

    # Defines the expected experiment script.
    # NB new lines and indentation with the string is important for passing the test
    script = inca_script.mapping(experimentalMS_data_simple, fragments_used_simple)
    expected_script = """
% add experimental data for annotated fragments
m.expts(1).data_ms(1).idvs.id(1,1) = {'F1_0_0_exp1'};
m.expts(1).data_ms(1).idvs.time(1,1) = 0;
m.expts(1).data_ms(1).idvs.val(1,1) = 0.000100;
m.expts(1).data_ms(1).idvs.std(1,1) = 0.001;
m.expts(1).data_ms(1).idvs.val(2,1) = 0.800800;
m.expts(1).data_ms(1).idvs.std(2,1) = 0.002402;
m.expts(1).data_ms(1).idvs.val(3,1) = 0.198300;
m.expts(1).data_ms(1).idvs.std(3,1) = 0.001;
m.expts(1).data_ms(1).idvs.val(4,1) = 0.000900;
m.expts(1).data_ms(1).idvs.std(4,1) = 0.001;
"""
    assert script == expected_script
