import typing
import pandas as pd
import pandera as pa
from typing import List
from IPython.display import display, HTML


def fetch_column_attributes(
    schema: pa.DataFrameSchema, column_name: str, attributes: typing.List
) -> typing.List[str]:
    """Fetches the values of attributes from a column from a pandera DataFrameSchema"""
    out = []
    for attribute in attributes:
        out.append(getattr(schema.columns[column_name], attribute))
    return out


def schema_overview_df(schema: pa.DataFrameSchema, attributes: typing.List):
    """Fetch the column attributes from a pandera DataFrameSchema and creates a pandas
    DataFrame with the column name in the first column and an additional column for each attribute."""
    schema_overview_dict = {}

    for column in schema.columns:
        schema_overview_dict[column] = fetch_column_attributes(
            schema, column, attributes
        )
    df = (
        pd.DataFrame.from_dict(schema_overview_dict, orient="index", columns=attributes)
        .reset_index()
        .rename(columns={"index": "column name"})
    )
    return df


def present_schema_overview(
    schema: pa.DataFrameSchema,
    attributes: List = ["dtype", "required", "nullable", "description"],
) -> None:
    """Display schema as html for jupyter notebooks. Used for easy documentation."""

    df = schema_overview_df(schema, attributes)
    display(HTML(df.to_html()))

__all__ = ["present_schema_overview"]