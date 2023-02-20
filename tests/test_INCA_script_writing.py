import pandas as pd
import pandera as pa
import pandera.typing as pat
from typing import Iterable, Literal, Union, List
from BFAIR.mfa.INCA.INCA_script import INCA_script
from BFAIR.mfa.INCA.INCA_script_writing import define_experiment, define_reactions, define_flux_measurements, _define_measured_ms_fragments, _define_ms_measurements, define_tracers, make_experiment_data_config, define_model
import pytest


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
    expected = """% define tracers used in exp1
t_exp1 = tracer({...
'[1-13C]A: A.ext @ 1',...
'[1,2-13C]B: B @ 1 2',...
});
t_exp1.frac = [0.5,0.5 ];
t_exp1.atoms.it(:,1) = [0.02,0.98];
t_exp1.atoms.it(:,1) = [0.05,0.95];\n"""
    assert define_tracers(tracer_df_test, 'exp1') == expected

def test_tracers_wrong_type(tracer_df_test):
    tracer_df_test["enrichment"] = "[0.5, 0.5]" # modify ratio to be a string

    with pytest.raises(pa.errors.SchemaError):
        define_tracers(tracer_df_test, 'exp1')

def test_define_flux_measurements(flux_measurements_test):
    expected = """\n% define flux measurements for experiment exp1
f_exp1 = [...
data('r1', 'val', 1.0, 'std', 0.1),...
data('r2', 'val', 2.0, 'std', 0.2),...
data('r3', 'val', 3.0, 'std', 0.3),...
];\n""" 
    assert define_flux_measurements(flux_measurements_test, "exp1") == expected


def test_define_measured_ms_fragments(ms_measurements_test):
    expected = """\n% define mass spectrometry measurements for experiment exp1
ms_exp1 = [...
msdata('A1: A @ 1 2 3 4'),...
];\n"""
    assert _define_measured_ms_fragments(ms_measurements_test, "exp1") == expected

def test_define_ms_measurements(ms_measurements_test):
    """Tests that the function writes the data to the correct format. Notice that the function _define_ms_measurements
    does not automatically fill the gaps in the idv data. This is done using the fill_all_mass_isotope_gaps function, 
    which is called before _define_ms_measurements in the usual workflow."""

    expected = """\n% define mass spectrometry measurements for experiment exp1
ms_exp1{'A1'}.idvs = idv([[0.1;0.1;0.4;0.4]], 'id', {'exp1_A1_0_0_1'}, 'std', [[0.01;0.01;0.02;0.02]], 'time', 0.0)\n"""
    assert _define_ms_measurements(ms_measurements_test, "exp1") == expected


def test_make_experiment_data_config(flux_measurements_test, ms_measurements_test):
    expected = {'exp1': ['data_flx', 'data_ms'], 'exp2': ['data_ms']}
    assert make_experiment_data_config(flux_measurements_test, ms_measurements_test) == expected


def test_define_model():
    model_id = "m1"
    experiment_id = ["exp1", "exp2"]
    
    expected = "m = model(r, 'expts', [e_exp1,e_exp2]);\n"
    assert define_model(experiment_id) == expected


def test_define_experiment():
    experiment_id = "exp1"
    measurement_types = ['data_flx', 'data_ms']

    expected = "e_exp1 = experiment(t_exp1, 'id', 'exp1', 'data_flx', f_exp1, 'data_ms', ms_exp1);\n" 
    assert define_experiment(experiment_id, measurement_types) == expected