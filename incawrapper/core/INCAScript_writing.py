import pandas as pd
import pandera as pa
import pandera.typing as pat
from typing import Dict, Iterable, Literal, Union, List, Optional
import pathlib
import time
import tempfile
import ast
import incawrapper.utils.chemical_formula as chemical_formula
import collections
from incawrapper.core.INCAScript import INCAScript
from incawrapper.core.dataschemas import ReactionsSchema, TracerSchema, FluxMeasurementsSchema, MSMeasurementsSchema, PoolSizeMeasurementsSchema
import logging
import warnings

@pa.check_input(ReactionsSchema)
def define_reactions(model_reactions: pd.DataFrame) -> str:
    def create_reaction(reaction_equation: str, reaction_id: str) -> str:
        """Parse a reaction string into a function call of the INCA reaction."""
        return f"reaction('{reaction_equation}', ['id'], ['{reaction_id}'])"

    reaction_func_calls = model_reactions.apply(
        lambda row: create_reaction(row["rxn_eqn"], row["rxn_id"]), axis=1
    )

    script = "% Create reactions\nr = [...\n"
    for reaction in reaction_func_calls:
        script += f"{reaction},...\n"
    script += "];"

    return script


@pa.check_input(TracerSchema)
def define_tracers(tracers: pd.DataFrame, experiment_id: str) -> str:
    """Define the tracers used in one experiment. Multiple experiments
    are handled in the define_experiments function."""

    def create_tracer(tracer_id: str, met_id: str, atom_ids: List) -> str:
        """Parse a tracer into a string format readable by INCA."""
        atom_ids_string = " ".join(str(x) for x in atom_ids)
        return f"'{tracer_id}: {met_id} @ {atom_ids_string}'"


    tracer_groups = (tracers
        .query(f"experiment_id == '{experiment_id}'")
        .groupby(['met_id', 'tracer_id','enrichment'])
    )

    # Initialize strings for tracer definition
    tracer_definition_str = f"t_{experiment_id}" + " = tracer({...\n" 
    enrichment_definition_lst = []
    mdv_definition_str = ""
    for grp, df in tracer_groups:
        # unpacking the group name, notice order is the same as in the groupby
        # This gives on one value for the data that is common for all rows in the group
        met_id, tracer_id, enrichment = grp

        # Iterate over the labelling groups
        labelling_group_count = 0
        for df_index, row in df.iterrows():

            # Create the tracer definitions
            tracer_string = create_tracer(
                tracer_id,
                met_id,
                row["atom_ids"],
            )
            tracer_definition_str += f"{tracer_string},...\n"

            # Create the tracer enrichments
            enrichment_definition_lst.append(str(enrichment))

            # collect atom mdvs (purity)
            labelling_group_count += 1
            mdv_definition_str += f"t_{experiment_id}.atoms.it(:,{labelling_group_count}) = ["
            mdv_definition_str += ",".join(str(x) for x in row["atom_mdv"])
            mdv_definition_str += "];\n"

    tracer_definition_str += "});\n"
    
    # Finalize the enrichment definition string
    enrichment_definition_str = f"t_{experiment_id}.frac = ["
    enrichment_definition_str += ",".join(enrichment_definition_lst)
    enrichment_definition_str += " ];\n"

    # Collect script
    tmp_script = (
        f"% define tracers used in {experiment_id}\n"
        + tracer_definition_str
        + enrichment_definition_str
        + mdv_definition_str
    )
    return tmp_script


@pa.check_input(FluxMeasurementsSchema)
def define_flux_measurements(
    flux_measurements: pd.DataFrame, experiment_id: str
) -> str:
    """Define the flux measurements used in one experiment. Multiple experiments
    is handled in the define_experiments function."""

    def create_flux(rxn_id: str, flux: float, flux_std_error: float) -> str:
        """Parse a flux measurement into a string format readable by INCA."""
        return f"data('{rxn_id}', 'val', {flux}, 'std', {flux_std_error})"

    fluxes_subset = flux_measurements[
        flux_measurements["experiment_id"] == experiment_id
    ]

    if fluxes_subset.empty:
        warnings.warn(f"No flux measurements found for experiment {experiment_id}")
        return "" 

    tmp_script = (
        f"\n% define flux measurements for experiment {experiment_id}\n"
        + f"f_{experiment_id}"
        + " = [...\n"
    )

    for _, flux in fluxes_subset.iterrows():
        tmp_script += create_flux(flux["rxn_id"], flux["flux"], flux["flux_std_error"])
        tmp_script += ",...\n"
    tmp_script += "];\n"
    return tmp_script

pa.check_input(PoolSizeMeasurementsSchema)
def define_pool_measurements(
        pool_measurements: pd.DataFrame, experiment_id: str
)-> str:
    """Define the pool measurements used in one experiment. Multiple experiments
    is handled in the define_experiments function."""

    pools_subset = pool_measurements[
        pool_measurements["experiment_id"] == experiment_id
    ]

    if pools_subset.empty:
        warnings.warn(f"No pool measurements found for experiment {experiment_id}")
        return ""
    
    tmp_script = (
        f"\n% define pool measurements for experiment {experiment_id}\n"
        + f"p_{experiment_id}"
        + " = [...\n"
    )

    for _, pool in pools_subset.iterrows():
        tmp_script += instantiate_inca_class_call(
            inca_class='data', 
            S="'" + pool["met_id"] + "'", 
            val=pool["pool_size"], 
            std=pool["pool_size_std_error"]
        )
        tmp_script += ",...\n"
    tmp_script += "];\n"
    return tmp_script


def modify_class_instance(
    class_name: Literal['rates', 'states'],
    sub_class_name: Literal[None, 'flx'],
    instance_id: str,
    properties: Dict,
):
    """Modify properties of a class instance in the model. This is useful for
    example to set the flux of a reaction to zero or specify a bounds 
    for a reaction.

    e.g. 
    modify_class('rates', 'flx', 'R_EX_glc__D_e', {'lb': -10, 'ub': 0})
    modify_class('rates', 'flx', 'R_EX_glc__D_e', {'val': 0, 'fix': TRUE})
    modify_class('states', None, 'glc__D_e', {'val': 0, 'fix': TRUE})
    
    Look in the INCA documentation for a list of all possible properties for the class
    (<path-to-inca-folder>/doc/inca/class/)."""


    tmp_script = f"index_{instance_id} = find(strcmp(m.{class_name}.id, '{instance_id}'));\n"
    for k, v in properties.items():
        if isinstance(v, bool):
            v = f"{str(v).lower()}"
        
        if sub_class_name is not None:
            tmp_script += f"m.{class_name}(index_{instance_id}).{sub_class_name}.{k} = {v};\n"
        else:
            tmp_script += f"m.{class_name}(index_{instance_id}).{k} = {v};\n"

    return tmp_script

def get_unlabelled_atom_ids(molecular_formula: str, labelled_atom_ids: str) -> str:
    """
    Get the unlabelled atoms in a molecule by substrating the labelled atoms.

    Parameters
    ----------
        molecular_formula: str
            The molecular formula of the molecule.
        labelled_atom_ids: str
            The labelled atoms in the molecule.

    Returns
    -------
        unlabelled_atom_ids: str
            A molecular formula string of the unlabelled atoms.
    """
    formula_dict = chemical_formula._create_compound_dict(molecular_formula)
    labelled_atom_ids_formula = chemical_formula.create_formula_from_dict(
        collections.Counter(labelled_atom_ids)
    )
    unlabelled_atom_ids_formula = chemical_formula.subtract_formula(
        molecular_formula,
        labelled_atom_ids_formula,
    )

    return unlabelled_atom_ids_formula


def _fill_mass_isotope_gaps_in_group(ms_measurements):
    """Fill gaps in mass_isotope column and add nan for intensity and intensity_std_error. 
    Here a gap is defined as gaps in the mass_isotope column that are not consecutive 
    intergers starting from 0. This does not consider the labelled_atom_ids. Missing 
    values above the largest measured mass_isotope are handled by INCA.
    
    This function is meant to be used with pandas.DataFrame.groupby().apply().
    
    Parameters
    ----------
    ms_measurements : pandas.DataFrame
        A sub-dataframe of ms_measurement data where all columns only have one unique
        value except for intensity, intensity_std_error, and mass_isotope.
    
    Returns
    -------
    pandas.DataFrame
        A dataframe with the same columns as the input dataframe but with the mass_isotope
        column filled with consecutive integers starting from 0. The intensity and
        intensity_std_error columns are filled with pd.NA for the missing values."""

    largest_mass_isotope = ms_measurements['mass_isotope'].max()
    fill_columns = [name for name in ms_measurements.columns if name not in ['intensity', 'intensity_std_error', 'mass_isotope']]
    ms_measurements = ms_measurements.set_index("mass_isotope").reindex(range(0, largest_mass_isotope + 1), fill_value=pd.NA)
    ms_measurements[fill_columns] = ms_measurements[fill_columns].ffill().bfill()
    return ms_measurements

@pa.check_input(MSMeasurementsSchema)
def fill_all_mass_isotope_gaps(ms_measurements: pd.DataFrame) -> pd.DataFrame:
    groupby_cols = ["experiment_id", "ms_id", "measurement_replicate", 'time']
    out = (ms_measurements
        .groupby(groupby_cols)
        .apply(_fill_mass_isotope_gaps_in_group)
        .drop(columns=groupby_cols)
        .reset_index()
    )
    return out


def instantiate_inca_class_call(inca_class: str, S, **kwargs) -> str:
    """Create a string to instantiate an INCA class. An INCA class is instantiated
    by calling the class with the arguments S and kwargs. The type of S depends on the
    class, but in most cases it is a string. The kwargs defines the properties of the
    class. The propeties are defined in INCA as two successive arguments, the first
    argument is the name of the property and the second argument is the value of the 
    property. The properties of a specific class' can be found in the INCA documentation
    (<inca folder>/doc/inca/class)."""

    kwargs_str = ", ".join([f"'{k}', {v}" for k, v in kwargs.items()])
    if not kwargs:
        return f"{inca_class}({S})"
    elif not S:
        return f"{inca_class}({kwargs_str})"

    return f"{inca_class}({S}, {kwargs_str})"


@pa.check_input(MSMeasurementsSchema)
def _define_measured_ms_fragments(
    ms_measurements: pd.DataFrame, experiment_id: str
) -> str:
    """INCA's data model distinguishes between the ms fragments and the measurements of
    the fragments. This function defines the possible ms fragments that was measured,
    in one experiment. Multiple experiments is handled in the define_experiments function.
    """

    def create_ms(
        ms_id: str,
        met_id: str,
        labelled_atom_ids: List,
        unlabelled_atoms: Optional[str] = None,
    ) -> str:
        labelled_atom_ids_string = " ".join(str(x) for x in labelled_atom_ids)
        ms_fragment_string = f"'{ms_id}: {met_id} @ {labelled_atom_ids_string}'"

        if unlabelled_atoms is not None and unlabelled_atoms != "" and not pd.isna(unlabelled_atoms):
            return instantiate_inca_class_call(
                "msdata", ms_fragment_string, more=f"'{unlabelled_atoms}'"
            )
        return instantiate_inca_class_call("msdata", ms_fragment_string)

    ms_measurements_subset = ms_measurements[
        ms_measurements["experiment_id"] == experiment_id
    ]

    if ms_measurements_subset.empty:
        warnings.warn(f"No ms measurements found for experiment {experiment_id}. Skipping possible ms fragments.")
        return "" 

    tmp_script = (
        f"\n% define mass spectrometry measurements for experiment {experiment_id}\n"
        + f"ms_{experiment_id}"
        + " = [...\n"
    )

    for ms_id, ms_df in ms_measurements_subset.groupby("ms_id"):
        ms_df = ms_df.iloc[0]
        if not "unlabelled_atoms" in ms_df.index:
            tmp_script += create_ms(
                ms_id,
                ms_df["met_id"],
                ms_df["labelled_atom_ids"],
            )
        else:
            tmp_script += create_ms(
                ms_id,
                ms_df["met_id"],
                ms_df["labelled_atom_ids"],
                ms_df["unlabelled_atoms"],
            )

        tmp_script += ",...\n"
    tmp_script += "];\n"
    return tmp_script


def matlab_column_vector(lst: List[float]) -> str:
    """Convert a list to a matlab column vector string. These are of the fortmat
    [1;2;3;4;5]"""
    return "[" + ";".join([str(i) for i in lst]) + "]"

@pa.check_input(MSMeasurementsSchema)
def _define_ms_measurements(ms_measurements: pd.DataFrame, experiment_id: str) -> str:
    """Defines measurements of ms fragments. This is done by updating the msdata objects
    of the individuals ms fragements."""
    
    def add_idvs_to_msdata(
		experiment_id: str,
        ms_id: str,
        df: pat.DataFrame,
    ) -> str:
        """Write a line of matlab code to add measurements of one ms fragment to the
        msdata object. ALL measurements related that fragment has to be written in one
        line. Theses multiple measurements can either originate from replicated 
        measurements or from multiple time points. The idv() INCA class interprets 
        one idv of a timepoint or replicate as a column vector. Therefore the python 
        lists are converted into matlab column vectors.

        Each measurement is given a unique id. This is done by concatenating the
        experiment_id, ms_id, time and replicate number.
        """

        # convert to matlab NaN
        df_new = df.copy()
        df_new[['intensity', 'intensity_std_error']] = df[['intensity', 'intensity_std_error']].fillna('NaN')

        measurement_id_lst = []
        idv_str = "["
        idv_std_error_str = "["
        # Create a column vector for each timepoint/replicate
        for (replicate, time), grp_df in df_new.groupby(['measurement_replicate', 'time']):
            grp_df = grp_df.sort_values('mass_isotope', ascending=True)
            idv_str += matlab_column_vector(grp_df['intensity']) + ","
            idv_std_error_str += matlab_column_vector(grp_df['intensity_std_error']) + ","

            # create unique id for each measurement
            measurement_id_lst.append(
                "'" +
                str(experiment_id) + "_" +
                str(ms_id) + "_" + 
                str(time).replace(".", "_") + "_" +
                str(replicate) +
                "'"
            )

        # remove last comma
        idv_str = idv_str.rstrip(",") + "]"
        idv_std_error_str = idv_std_error_str.rstrip(",") + "]"

        idv_id = "{" + ",".join(measurement_id_lst) + "}"

        time_str = "[" + ",".join(df_new['time'].unique().astype(str)) + "]"
        return (
            f"ms_{experiment_id}{{'{ms_id}'}}.idvs = " + 
            instantiate_inca_class_call(
                "idv", idv_str, id=idv_id, std=idv_std_error_str, time=time_str
            )
        )

    ms_measurements_subset = ms_measurements[
        ms_measurements["experiment_id"] == experiment_id
    ]

    if ms_measurements_subset.empty:
        warnings.warn(f"No ms measurements found for experiment {experiment_id}")
        return "" 

    tmp_script = (
        f"\n% define mass spectrometry measurements for experiment {experiment_id}\n"
    )
    for ms_id, ms_df in ms_measurements_subset.groupby("ms_id"):
        tmp_script += add_idvs_to_msdata(
            experiment_id,
            ms_id,
            ms_df,
        )
        tmp_script += "\n"
    return tmp_script

def define_ms_data(ms_measurements: pd.DataFrame, experiment_id: str) -> str:
    """Wrapper function to define both the msdata objects and the ms measurements."""
    ms_measurements = fill_all_mass_isotope_gaps(ms_measurements)
    tmp_script = _define_measured_ms_fragments(ms_measurements, experiment_id)
    tmp_script += _define_ms_measurements(ms_measurements, experiment_id)
    return tmp_script

def _inverse_dict(d):
    """Return a dictionary with the keys as the elements of the lists and the values 
    as the keys of the original dictionary. Examples:
    >>> inverse_dict({'flux': ['exp1', 'exp2'], 'ms': ["exp2", "exp3"]})
    {'exp1': ['flux'], 'exp2': ['flux', 'ms'], 'exp3': ['ms']}
    """
    result = {}
    for k, v in d.items():
        for item in v:
            result.setdefault(item, []).append(k)
    return result


def make_experiment_data_config(    
    flux_measurements: Union[pd.DataFrame, None] = None,
    ms_measurements: Union[pd.DataFrame, None] = None,
    pool_measurements: Union[pd.DataFrame, None] = None,
    nmr_measurements: Union[pd.DataFrame, None] = None,
) -> Dict:

    experiments_with_measurement_type = dict() # type: Dict[str, List[str]]
    if flux_measurements is not None:
        experiments_with_measurement_type['data_flx'] = flux_measurements["experiment_id"].unique().tolist()
    if ms_measurements is not None:
        experiments_with_measurement_type['data_ms'] = ms_measurements["experiment_id"].unique().tolist()
    if pool_measurements is not None:
        experiments_with_measurement_type['data_cxn'] = pool_measurements["experiment_id"].unique().tolist()
    if nmr_measurements is not None:
        experiments_with_measurement_type['data_nmr'] = nmr_measurements["experiment_id"].unique().tolist()

    experimental_data_config = _inverse_dict(experiments_with_measurement_type)

    return experimental_data_config

#@pa.check_input() # make a pandera schema experimental_data_config dictionary
def define_experiment(
    experiment_id: str, measurement_types: List
) -> str:
    """Write a line of matlab code to define an experiment. The experiment requires
    a tracer object to be instantiated earlier in the matlab script."""

    data_list = list()
    for measurement_type in measurement_types:
        if measurement_type == "data_flx":
            data_list.extend(["'data_flx'", f"f_{experiment_id}"])
        if measurement_type == "data_ms":
            data_list.extend(["'data_ms'", f"ms_{experiment_id}"])
        if measurement_type == "data_cxn":
            data_list.extend(["'data_cxn'", f"p_{experiment_id}"])
        if measurement_type == "data_nmr":
            data_list.extend(["'data_nmr'", f"nmr_{experiment_id}"])
    data_list_str = ", ".join(data_list)

    return f"e_{experiment_id} = experiment(t_{experiment_id}, 'id', '{experiment_id}', {data_list_str});\n"

def define_model(
    experiment_ids: List[str]
) -> str:
    """Write a line of matlab code to define a model. The model requires
    a tracer object to be instantiated earlier in the matlab script."""

    experiment_list = list()
    for experiment_id in experiment_ids:
        experiment_list.extend([f"e_{experiment_id}"])
    experiment_list_str = "[" + ",".join(experiment_list) + "]"

    return f"m = model(r, 'expts', {experiment_list_str});\n"


def define_options(**kwargs):
    """Write a line of matlab code to define options for the model.
    The available options can be found in the INCA documentation.
    <inca-folder>/doc/inca/class/@option/option.html"""
    for k, v in kwargs.items():
        # matlab does not like True/False, it wants true/false
        if isinstance(v, bool):
            kwargs[k] = f"{str(v).lower()}"
        # some options (e.g. oed_crit) require strings in the matlab script
        if isinstance(v, str):
            kwargs[k] = f"'{v}'"
    return "m.options = " + instantiate_inca_class_call("option", S=None, **kwargs)

def define_runner(        
        output_filename: pathlib.Path,
        run_estimate: bool = True,
        run_simulation: bool = True,
        run_continuation: bool = False,
        run_montecarlo: bool = False,
    ) -> str:
        """
        Generate a MATLAB script that specifies operations to be performed with the model defined in the INCA script.

        Parameters
        ----------
        output_filename : pathlib.Path
            Path to the output file. The output file will be a .mat file.
        run_continuation : bool, optional
            Whether to run parameter continuation with the settings defined in the INCA script, default True.
        run_simulation : bool, optional
            Whether to run a simulation with the settings defined in the INCA script, default True.
            This is necessary for a fluxmap to be loaded into INCA.

        Returns
        -------
        String
        """

        if run_montecarlo and not run_estimate:
            raise ValueError("Monte Carlo analysis requires an estimate to be run.")

        estimation = "f = estimate(m);\n" if run_estimate else ""
        continuation = "f=continuate(f,m);\n" if run_continuation else ""
        simulation = (
            "s=simulate(m);\n" if run_simulation else ""
        )  # For a fluxmap to be loaded into INCA, the .mat file must have a simulation


        # using pathlib.Path.resolve() to get the absolute path of the output file
        # otherwise the output file will be save in the temporary directory created 
        # during run_inca()
        if type(output_filename) is not pathlib.Path:
            output_filename = pathlib.Path(output_filename)
        output = f"filename = '{output_filename.resolve()}';\n"

        saving = "save(filename, "
        if run_estimate:
            saving += "'f', "
        if run_simulation:
            saving += "'s', "

        saving += "'m');\n"

        montecarlo = ""
        if run_montecarlo:
            mc_filename = output_filename.with_name(output_filename.stem + "_mc.mat")
            montecarlo += f"mc_filename = '{mc_filename.resolve()}';\n"
            montecarlo += "m = fit2mod(m,f);\n" # the fit has to be added to the model for montecarlo to work properly
            montecarlo += f"[K,CI] = montecarlo(f,m);\n"
            montecarlo += "save(mc_filename, 'K','CI');\n"

        return estimation + continuation + simulation + output + saving + montecarlo


def create_inca_script_from_data(
   reactions_data: ReactionsSchema, 
   tracer_data: TracerSchema, 
   flux_measurements: FluxMeasurementsSchema = None, 
   ms_measurements: MSMeasurementsSchema = None, 
   pool_measurements = None,
   experiment_ids: Optional[Union[str,List]] = 'All',
)->INCAScript:
    """Create an INCAScript object from dataframes with the data. The experiment configuration 
    is inferred from the data. The user can specify which experiments to include in the INCA script
    by specifying the experiment_ids.
    
    Parameters
    ----------
    reactions_data : dataschemas.ReactionsSchema
        Dataframe with the reactions data
    tracer_data : dataschemas.TracerSchema
        Dataframe with the tracer data
    flux_measurements : dataschemas.FluxMeasurementsSchema, optional
        Dataframe with the flux measurements, by default None
    ms_measurements : dataschemas.MSMeasurementsSchema, optional
        Dataframe with the MS measurements, by default None
    pool_measurements : [type], optional
        Not yet implemented, by default None
    experiment_ids : Optional(Union[str,List[str]]), optional
        List of experiment ids to include in the INCA script, by default 'All'.
    
    Returns
    -------
    INCAScript
        INCAScript object populated with reactions, tracers, experiments, model and measurements.
    """
    exp_config = make_experiment_data_config(flux_measurements, ms_measurements, pool_measurements)
    if experiment_ids != 'All':
        if isinstance(experiment_ids, list):
            exp_config = {k:v for k,v in exp_config.items() if k in experiment_ids}
        if isinstance(experiment_ids, str):
            exp_config = exp_config[experiment_ids]

    inca_script = INCAScript()
    inca_script.add_to_block('reactions', define_reactions(reactions_data))

    # Specify data
    for exp_id, measurement_types in exp_config.items():
        inca_script.add_to_block("tracers", define_tracers(tracer_data, exp_id))
        if "data_flx" in measurement_types:
            inca_script.add_to_block("fluxes", define_flux_measurements(flux_measurements, exp_id))
        if "data_ms" in measurement_types:
            inca_script.add_to_block("ms_fragments", define_ms_data(ms_measurements, exp_id))
        if "data_cxn" in measurement_types:
            inca_script.add_to_block("pool_sizes", define_pool_measurements(pool_measurements, exp_id))
        inca_script.add_to_block("experiments", define_experiment(exp_id, measurement_types))
        
    inca_script.add_to_block('model', define_model(exp_config.keys()))

    return inca_script

__all__ = [
    "define_reactions",
    "define_tracers",
    "define_experiment",
    "define_model",
    "define_flux_measurements",
    "define_ms_data",
    "define_pool_measurements",
    "define_options",
    "define_runner",
    "create_inca_script_from_data",
    "modify_class_instance",
]