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

