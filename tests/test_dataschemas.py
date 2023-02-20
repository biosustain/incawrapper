import pandera as pa
import pandas as pd
from BFAIR.mfa.INCA.dataschemas import ReactionsSchema, TracerSchema, FluxMeasurementsSchema, MSMeasurementsSchema
import pytest

def test_FluxMeasurementsSchema_accepts_ints(flux_measurements_test):
    df = flux_measurements_test.copy()
    df["flux"] = pd.Series([1, 2, 3])
    validated_df = FluxMeasurementsSchema.validate(df)
    assert isinstance(validated_df["flux"][0], float)


def test_TracerSchema(tracer_df_test):
    df = tracer_df_test.copy()
    validated_df = TracerSchema.validate(df)
    assert isinstance(validated_df["atom_ids"][0], list)

def test_invalid_experiment_id(flux_measurements_test):
    df = flux_measurements_test.copy()
    df["experiment_id"] = pd.Series(["exp-1", "exp:2", "exp[1]"])
    with pytest.raises(pa.errors.SchemaError):
        FluxMeasurementsSchema.validate(df)


def test_MSMeasurementsSchema(ms_measurements_test):
    df = ms_measurements_test.copy()
    assert isinstance(MSMeasurementsSchema.validate(df), pd.DataFrame)
