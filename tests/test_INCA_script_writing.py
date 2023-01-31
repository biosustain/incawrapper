import pandas as pd
import pandera as pa
import pandera.typing as pat
from typing import Iterable, Literal, Union, List
from BFAIR.mfa.INCA.INCA_script import INCA_script
from BFAIR.mfa.INCA.INCA_script_writing import define_experiment, define_reactions, define_flux_measurements, define_possible_ms_fragments, define_ms_measurements, define_tracers, make_experiment_data_config
import pytest


@pytest.fixture
def inca_script():
    return INCA_script()

@pytest.fixture
def reaction_test():
    return pd.DataFrame(
        {
            "reaction": ["A.ext (C1:a C2:b) -> A (C1:a C2:b)", "A (C1:a C2:b) -> B (C1:b C2:a)", "B -> C", "C -> D"],
            "id": ["r1", "r2", "r3", "r4"],
        }
    )

@pytest.fixture
def tracer_df_test():
    return pd.DataFrame(
        {
            "experiment_id": ["exp1", "exp1"],
            "met_name": ["[1-13C]A", "[1,2-13C]B"],
            "met_id": ["A.ext", "B"],
            "labelled_atoms": ["[1]", "[1,2]"],
            "ratio": [0.5, 0.5],
        }
    )

@pytest.fixture
def flux_measurements_test():
    return pd.DataFrame(
        {
            "experiment_id": ["exp1", "exp1", "exp1"],
            "rxn_id": ["r1", "r2", "r3"],
            "flux": [1.0, 2.0, 3.0],
            "flux_std_error": [0.1, 0.2, 0.3],
        }
    )

@pytest.fixture
def ms_measurements_test():
    return pd.DataFrame(
        {
            "experiment_id": ["exp1", "exp1", "exp1", "exp1"],
            "ms_id": ["ms1", "ms2", "ms3", "ms3"],
            "met_id": ["A", "B", "C", "C"],
            "labelled_atoms": ["[1,2]", "[C3,C4]", "[3]", "[3]"],
            "molecular_formula": ["C7H19O", "C2H4Si", None, None],
            "idv": [[1.0, 0.4], [2.0], [3.0, 4.0], [1.0, 5.0]],
            "idv_std_error": [[0.1, 0.2], [0.2], [0.3, 0.4], [0.1, 0.5]],
            "time": [0, 1, 0, 0],
        }
    )


def test_define_reactions(reaction_test):
    expected = """% Create reactions
r = [...
reaction('A.ext (C1:a C2:b) -> A (C1:a C2:b)', ['id'], ['r1']),...
reaction('A (C1:a C2:b) -> B (C1:b C2:a)', ['id'], ['r2']),...
reaction('B -> C', ['id'], ['r3']),...
reaction('C -> D', ['id'], ['r4']),...
];"""

    assert define_reactions(reaction_test) == expected


def test_define_tracers(tracer_df_test):
    expected = """% define tracers used in the experiments
t_exp1 = tracer({...
'[1-13C]A: A.ext @ 1',...
'[1,2-13C]B: B @ 1 2',...
});

% define fractions of tracers_subset used
t_exp1.frac = [0.5,0.5 ];"""
    assert define_tracers(tracer_df_test, 'exp1') == expected

def test_tracers_wrong_type(tracer_df_test):
    tracer_df_test["ratio"] = ["0.5", "0.5"] # modify ratio to be a string

    with pytest.raises(pa.errors.SchemaError):
        define_tracers(tracer_df_test, 'exp1')

def test_define_flux_measurements(flux_measurements_test):
    expected = """% define flux measurements for experiment exp1
f_exp1 = [...
data('r1', 'val', 1.0, 'std', 0.1),...
data('r2', 'val', 2.0, 'std', 0.2),...
data('r3', 'val', 3.0, 'std', 0.3),...
];""" 
    return define_flux_measurements(flux_measurements_test, "exp1") == expected


def test_define_possible_ms_fragments(ms_measurements_test):
    expected = """% define mass spectrometry measurements for experiment exp1
ms_exp1 = [...
msdata('ms1: A @ 1 2', 'more', 'C7H19O'),...
msdata('ms2: B @ C3 C4', 'more', 'CH4Si'),...
msdata('ms3: C @ 3'),...
];"""
    return define_possible_ms_fragments(ms_measurements_test, "exp1") == expected

def test_define_ms_measurements(ms_measurements_test):
    expected = """% define mass spectrometry measurements for experiment exp1
ms_exp1{'ms1'}.idvs = idv([[1.0;0.4]], 'id', {'exp1_ms1_0_1'}, 'std', [[0.1;0.2]], 'time', 0)
ms_exp1{'ms2'}.idvs = idv([[2.0]], 'id', {'exp1_ms2_1_1'}, 'std', [[0.2]], 'time', 1)
ms_exp1{'ms3'}.idvs = idv([[3.0;4.0],[1.0;5.0]], 'id', {'exp1_ms3_0_1','exp1_ms3_0_2'}, 'std', [[0.3;0.4],[0.1;0.5]], 'time', 0)"""
    return define_ms_measurements(ms_measurements_test, "exp1") == expected


def test_make_experiment_data_config(ms_measurements_test, flux_measurements_test):
    expected = {'exp1': ['data_flx', 'data_ms']}
    assert make_experiment_data_config(ms_measurements_test, flux_measurements_test) == expected