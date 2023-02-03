import pandera as pa
Check_contain_lists = pa.Check(
    lambda x: isinstance(x, list),
    element_wise=True,
    description="Check if all elements of the column are lists",
)


# Define the schema for the model reactions
model_reactions_schema = pa.DataFrameSchema(
    # TODO: Add validation for reaction arrow
    # TODO: Add validation for id uniqueness
    columns={
        "rxn_eqn": pa.Column(pa.String, required=True),
        "rxn_id": pa.Column(pa.String, required=True),
    }
)

tracer_schema = pa.DataFrameSchema(
    # TODO: Add validation for reaction arrow
    # TODO: Add validation for id uniqueness
    columns={
        "experiment_id": pa.Column(pa.String, required=True),
        "tracer_id": pa.Column(pa.String, required=True, description="Name of the tracer"),
        "met_id": pa.Column(pa.String, required=True, description="ID of the metabolite"),
        "atom_ids": pa.Column(
            pa.String, required=True, 
            description="""List of labelled atoms in the metabolite. E.g. [1,2] or [C1,C2]. 
Currently only supports one labelling group, e.i. all labelled atoms have the same purity.""",
        ),  #  "List of labelled atoms in the metabolite. E.g. [1,2] or [C1,C2]"
        "atom_mdv": pa.Column(pa.Object, required=True, checks=Check_contain_lists),  # pandera does not support list type
        "enrichment": pa.Column(pa.Float, required=True, coerce=True),
    }
)

flux_measurements_schema = pa.DataFrameSchema(
    columns={
        "experiment_id": pa.Column(pa.String, required=True),
        "rxn_id": pa.Column(pa.String, required=True),
        "flux": pa.Column(pa.Float, required=True, coerce=True),
        "flux_std_error": pa.Column(pa.Float, required=True, coerce=True),
    }
)


ms_measurements_schema = pa.DataFrameSchema(
    # TODO: validate that data describing the fragments are the same multiple measurements
    # of the same fragment. If grouping by ms_id colums met_id, molecular_formula and
    # labelled_atoms should only one value.
    columns={
        "experiment_id": pa.Column(pa.String, required=True),
        "met_id": pa.Column(pa.String, required=True),
        "ms_id": pa.Column(pa.String, required=True),
        "labelled_atom_ids": pa.Column(pa.Object, required=True, checks=Check_contain_lists),
        "unlabelled_atoms": pa.Column(
            pa.String, required=False, nullable=True
        ),  # nullable=True allows null values as nan or None
        "idv": pa.Column(
            pa.Object, required=True, checks=Check_contain_lists
        ),  # pandera does not support list type
        "idv_std_error": pa.Column(
            pa.Object, required=True, checks=Check_contain_lists
        ),  # pandera does not support list type
        "time": pa.Column(pa.Float, required=True, coerce=True),
    }
)