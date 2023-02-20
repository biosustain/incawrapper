import pandera as pa
ContainListsCheck = pa.Check(
    lambda x: isinstance(x, list),
    element_wise=True,
    title='Contain lists',
    description="Check if all elements of the column are lists",
    error="The column must contain python lists",
)

# experiment_id column are used in multiple schemas therefore it is defined here
ExperimentIdColumn = pa.Column(
    pa.String, 
    required=True, 
    description="ID of the experiment. Must be a valid MATLAB variable name, legal characters are a-z, A-Z, 0-9, and the underscore character.",
    checks=pa.Check.str_matches(r'[\w-]+$', error="The experiment_id must be a valid MATLAB variable name, legal characters are a-z, A-Z, 0-9, and the underscore character."),
)


# Define the schema for the model reactions
ReactionsSchema = pa.DataFrameSchema(
    # TODO: Add validation for reaction arrow
    # TODO: Add validation for id uniqueness
    columns={
        "rxn_eqn": pa.Column(pa.String, required=True),
        "rxn_id": pa.Column(pa.String, required=True),
    }
)

TracerSchema = pa.DataFrameSchema(
    # TODO: Add validation for reaction arrow
    # TODO: Add validation for id uniqueness
    columns={
        "experiment_id": ExperimentIdColumn,
        "tracer_id": pa.Column(pa.String, required=True, description="Name of the tracer"),
        "met_id": pa.Column(pa.String, required=True, description="ID of the metabolite"),
        "atom_ids": pa.Column(
            pa.String, required=True, 
            description="""List of labelled atoms in the metabolite. E.g. [1,2] or [C1,C2]. 
Currently only supports one labelling group, e.i. all labelled atoms have the same purity.""",
        ),  #  "List of labelled atoms in the metabolite. E.g. [1,2] or [C1,C2]"
        "atom_mdv": pa.Column(pa.Object, required=True, checks=ContainListsCheck),  # pandera does not support list type
        "enrichment": pa.Column(pa.Float, required=True, coerce=True),
    }
)

FluxMeasurementsSchema = pa.DataFrameSchema(
    columns={
        "experiment_id": ExperimentIdColumn,
        "rxn_id": pa.Column(pa.String, required=True),
        "flux": pa.Column(pa.Float, required=True, coerce=True),
        "flux_std_error": pa.Column(pa.Float, required=True, coerce=True),
    }
)


MSMeasurementsSchema = pa.DataFrameSchema(
    # TODO: validate that data describing the fragments are the same multiple measurements
    # of the same fragment. If grouping by ms_id colums met_id, molecular_formula and
    # labelled_atoms should only one value.
    columns={
        "experiment_id": ExperimentIdColumn,
        "met_id": pa.Column(pa.String, required=True),
        "ms_id": pa.Column(pa.String, required=True),
        "measurement_replicate": pa.Column(pa.Int, required=True, coerce=True, 
            description="Replicate number of the measurement of the same fragment in the same experiment. "
            "In most cases, the data will only have one measurement per fragment per experiment."
        ),
        "labelled_atom_ids": pa.Column(pa.Object, required=True, checks=ContainListsCheck),
        "unlabelled_atoms": pa.Column(
            pa.String, required=False, nullable=False
        ),  # nullable=True allows null values as nan or None
        "mass_isotope": pa.Column(pa.Int, required=True, coerce=True),
        "intensity": pa.Column(pa.Float, required=True, coerce=True, nullable=True),
        "intensity_std_error": pa.Column(pa.Float, required=True, coerce=True, nullable=True),
        "time": pa.Column(pa.Float, required=True, coerce=True),
    },
    checks=[
        # TODO: refactor to accomudate new long input data pa.Check(lambda row: len(row["idv"]) == len(row["labelled_atom_ids"])+1, element_wise=True, raise_warning=True, error="There is not a measurement for all mass isotopes (len(idv)<len(labelled_atom_ids)+1). This is allowed and may as well be intended, but it could be a mistake in input data."),
    ]
)