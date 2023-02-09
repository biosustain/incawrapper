import pandera as pa
import pandas as pd
from BFAIR.mfa.INCA.dataschemas import model_reactions_schema, tracer_schema, flux_measurements_schema, ms_measurements_schema
import pytest

def test_flux_measurement_schema_accepts_ints(flux_measurements_test):
    df = flux_measurements_test.copy()
    df["flux"] = pd.Series([1, 2, 3])
    validated_df = flux_measurements_schema.validate(df)
    assert isinstance(validated_df["flux"][0], float)


def test_tracers_schema(tracer_df_test):
    df = tracer_df_test.copy()
    validated_df = tracer_schema.validate(df)
    assert isinstance(validated_df["atom_ids"][0], list)

def test_invalid_experiment_id(flux_measurements_test):
    df = flux_measurements_test.copy()
    df["experiment_id"] = pd.Series(["exp-1", "exp:2", "exp[1]"])
    with pytest.raises(pa.errors.SchemaError):
        flux_measurements_schema.validate(df)


def test_ms_measuremnts_schema(ms_measurements_test):
    df = ms_measurements_test.copy()
    assert isinstance(ms_measurements_schema.validate(df), pd.DataFrame)


def test_invalid_length_idv_std_error(ms_measurements_test):
    df = ms_measurements_test.copy()
    df.loc[[0],'idv_std_error']= pd.Series([[0.1, 0.2, 0.3,0.4]]) # the [] around 0 is required
    with pytest.raises(pa.errors.SchemaError, match="The length of idv and idv_std_error must be the same"):
        ms_measurements_schema.validate(df)


def test_short_idv_raises_warning(ms_measurements_test):
    """Test that a warning is raised if the length of idv is shorter than the length of labelled_atom_ids"""
    df = ms_measurements_test.copy()
    df.loc[0,'idv'] = [0.1]
    df.loc[0,'idv_std_error'] = [0.1]
    with pytest.warns(UserWarning):
        ms_measurements_schema.validate(df)

