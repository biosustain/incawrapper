import pandera as pa

# Define the schema for the model reactions
model_reactions_schema = pa.DataFrameSchema(
    # TODO: Add validation for reaction arrow
    # TODO: Add validation for id uniqueness
    columns={
        "reaction": pa.Column(pa.String, required=True),
        "id": pa.Column(pa.String, required=True),
    }
)

tracer_schema = pa.DataFrameSchema(
    # TODO: Add validation for reaction arrow
    # TODO: Add validation for id uniqueness
    columns={
        "experiment_id": pa.Column(pa.String, required=True),
        "met_name": pa.Column(pa.String, required=True),
        "met_id": pa.Column(pa.String, required=True),
        "labelled_atoms": pa.Column(
            pa.String, required=True
        ),  #  "List of labelled atoms in the metabolite. E.g. [1,2] or [C1,C2]"
        "ratio": pa.Column(pa.Float, required=True),
    }
)

flux_measurements_schema = pa.DataFrameSchema(
    columns={
        "experiment_id": pa.Column(pa.String, required=True),
        "rxn_id": pa.Column(pa.String, required=True),
        "flux": pa.Column(pa.Float, required=True),
        "flux_std_error": pa.Column(pa.Float, required=True),
    }
)

Check_contain_lists = pa.Check(
    lambda x: isinstance(x, list),
    element_wise=True,
    description="Check if all elements of the column are lists",
)
ms_measurements_schema = pa.DataFrameSchema(
    # TODO: validate that data describing the fragments are the same multiple measurements
    # of the same fragment. If grouping by ms_id colums met_id, molecular_formula and
    # labelled_atoms should only one value.
    columns={
        "experiment_id": pa.Column(pa.String, required=True),
        "met_id": pa.Column(pa.String, required=True),
        "ms_id": pa.Column(pa.String, required=True),
        "molecular_formula": pa.Column(
            pa.String, required=True, nullable=True
        ),  # nullable=True allows null values as nan or None
        "labelled_atoms": pa.Column(pa.String, required=True),
        "idv": pa.Column(
            pa.Object, required=True, checks=Check_contain_lists
        ),  # pandera does not support list type
        "idv_std_error": pa.Column(
            pa.Object, required=True, checks=Check_contain_lists
        ),  # pandera does not support list type
    }
)