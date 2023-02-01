import pandera as pa
import pandas as pd
from BFAIR.mfa.INCA.dataschemas import model_reactions_schema, tracer_schema, flux_measurements_schema, ms_measurements_schema

def test_flux_measurement_schema_accepts_ints(flux_measurements_test):
    df = flux_measurements_test.copy()
    df["flux"] = pd.Series([1, 2, 3])
    validated_df = flux_measurements_schema.validate(df)
    assert isinstance(validated_df["flux"][0], float)

