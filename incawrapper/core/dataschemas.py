import pandera as pa
from typing import Optional
ContainListsCheck = pa.Check(
    lambda x: isinstance(x, list),
    element_wise=True,
    title='Contain lists',
    description="Check if all elements of the column are lists",
    error="The column must contain python lists",
)

ValidateArrowsCheck = pa.Check(
    lambda x: any(s in x for s in ("->", "<->")),
    element_wise=True,
    title='Validate arrows',
    description="Check if all elements of the column are valid reaction arrows",
    error="The column must contain valid reaction arrows: ->, <->",
)

# experiment_id column are used in multiple schemas therefore it is defined here
ExperimentIdColumn = pa.Column(
    pa.String, 
    required=True, 
    description="ID of the experiment. Must be a valid MATLAB variable name, legal characters are a-z, A-Z, 0-9, and the underscore character.",
    checks=pa.Check.str_matches(r'[\w-]+$', error="The experiment_id must be a valid MATLAB variable name, legal characters are a-z, A-Z, 0-9, and the underscore character."),
)
ReactionIDColumn = pa.Column(
    pa.String, required=True, description="The unique id of the reaction"
)


MetaboliteIdColumn = pa.Column(
    pa.String, required=True, 
    description="Metabolite ID of metabolite which is directly measured or from which the fragment is derived through a derivatization method.")

# Define the schema for the model reactions
ReactionsSchema = pa.DataFrameSchema(
    # TODO: Add validation for id uniqueness
    columns={
        "rxn_id": ReactionIDColumn,
        "rxn_eqn": pa.Column(pa.String, required=True, checks=ValidateArrowsCheck, description="The reaction equation with atom map. Allowed reaction arrows: ->, <->."),
    }
)

TracerSchema = pa.DataFrameSchema(
    # TODO: Add validation for reaction arrow
    # TODO: Add validation for id uniqueness
    columns={
        "experiment_id": ExperimentIdColumn,
        "tracer_id": pa.Column(pa.String, required=True, description="The unique id of the tracer compound."),
        "met_id": pa.Column(pa.String, required=True, description="The metabolite id of the labelled compound."),
        "atom_ids": pa.Column(
            pa.Object, required=True, 
            description="""Ids of the labelled atoms in the labelled atom group (equivalent to columns of the same name in the INCA GUI)""",
        ), 
        "atom_mdv": pa.Column(pa.Object, required=True, checks=ContainListsCheck, description="""mass/isotopomer distribution vector of the 
labelled atom group (equivalent to columns of the same name in the INCA GUI). The simplest way to use this column is to specify the purity of 
the labelling group. This is done supplying a list two numbers, e.g. [0.01, 0.99]."""
        ),  # pandera does not support list type
        "enrichment": pa.Column(pa.Float, required=True, coerce=True, description="""mass/isotopomer distribution vector of the labelled atom 
group (equivalent to columns of the same name in the INCA GUI). The simplest way to use this column is to specify the purity of the labelling 
group. This is done supplying a list two numbers, e.g. `[0.5, 0.95]` specifies 95% of the compound will be fully labelled in this labelling 
group. If different atom positions has different purity create a different labelling group for each position. For further description please 
refer to the INCA manual. Currently, the incawrapper only supports `atom_mdv` of length 2 for each labelling group."""
        ),
    }
)

FluxMeasurementsSchema = pa.DataFrameSchema(
    columns={
        "experiment_id": ExperimentIdColumn,
        "rxn_id": ReactionIDColumn,
        "flux": pa.Column(pa.Float, required=True, coerce=True, description="Measured/estimated rate typically in mmol/gDW/h"),
        "flux_std_error": pa.Column(pa.Float, required=True, coerce=True, description="Standard error of the measured/estimated rate"),
    }
)


MSMeasurementsSchema = pa.DataFrameSchema(
    # TODO: validate that data describing the fragments are the same multiple measurements
    # of the same fragment. If grouping by ms_id colums met_id, molecular_formula and
    # labelled_atoms should only one value.
    columns={
        "experiment_id": ExperimentIdColumn,
        "met_id": MetaboliteIdColumn,
        "ms_id": pa.Column(pa.String, required=True, description="ID of the measured ms fragment - often multiple fragment can be measured from the same metabolite"),
        "measurement_replicate": pa.Column(pa.Int, required=True, coerce=True, 
            description="""Replicate number of the measurement of the same fragment in the same experiment. 
"In most cases, the data will only have one measurement per fragment per experiment."""
        ),
        "labelled_atom_ids": pa.Column(pa.Object, required=True, checks=ContainListsCheck, description="""List of atom ids of the labelled atoms in the metabolite."""),
        "unlabelled_atoms": pa.Column(
            pa.String, required=False, nullable=True, coerce=True, description="""The molecular formula of the all atoms that cannot be labelled through 
the introduced labels in the tracers. This typically includes non-carbon elements of the fragment and all elements originating from derivatization agent. 
INCA uses the unlabelled atoms to correct for natural abundance."""
        ),  # nullable=True allows null values as nan or None
        "mass_isotope": pa.Column(pa.Int, required=True, coerce=True, description="""The mass isotopomer of the fragment.
E.g. M0, M+1, etc. Specified as an integer. It is allowed to have gaps in the isotopmer of a given fragment, e.g. 0, 2, 3. In this case the intensity and 
std error of missing isotopomers are filled with NaN before inserted in INCA."""
        ),
        "intensity": pa.Column(pa.Float, required=True, coerce=True, nullable=True, description="""The measured intensity of the fragment mass isotope."""
        ),
        "intensity_std_error": pa.Column(pa.Float, required=True, coerce=True, nullable=True, description="""The standard error of the measured intensity of the fragment mass isotope."""),
        "time": pa.Column(pa.Float, required=True, coerce=True, description="Time point of measurement only relevant for isotopically non-stationary MFA analysis"),
    },
    checks=[
        # TODO: refactor to accomudate new long input data pa.Check(lambda row: len(row["idv"]) == len(row["labelled_atom_ids"])+1, element_wise=True, raise_warning=True, error="There is not a measurement for all mass isotopes (len(idv)<len(labelled_atom_ids)+1). This is allowed and may as well be intended, but it could be a mistake in input data."),
    ]
)

PoolSizeMeasurementsSchema = pa.DataFrameSchema(
    columns={
        "experiment_id": ExperimentIdColumn,
        "met_id": MetaboliteIdColumn,
        "pool_size": pa.Column(pa.Float, required=True, coerce=True, description="Measured pool size typically in mmol/gDW"),
        "pool_size_std_error": pa.Column(pa.Float, required=True, coerce=True, description="Standard error of the measured pool size"),
    }
)

__all__ = [
    "ReactionsSchema",
    "TracerSchema",
    "FluxMeasurementsSchema",
    "MSMeasurementsSchema",
    "PoolSizeMeasurementsSchema",
]
