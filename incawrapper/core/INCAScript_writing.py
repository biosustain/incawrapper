"""This module contains functions that write the matlab script blocks for the INCA script.

**matlab variable naming convention:**

Many of the functions in this module relies on a naming convention for the matlab variables. The
naming convention is as follows:

* `r`: is the matlab variable that contains the reactions in the model.
* `e_<experiment_id>`: is the matlab variable that contains the experiment with the id give by
    `<experiment_id>`.
* `f_<experiment_id>`: is the matlab variable that contains the flux measurements for the
    experiment with the id give by `<experiment_id>`.
* `ms_<experiment_id>`: is the matlab variable that contains the mass spectrometry measurements for
    the experiment with the id give by `<experiment_id>`.
* `p_<experiment_id>`: is the matlab variable that contains the pool size measurements for the
    experiment with the id give by `<experiment_id>`.
* `m`: is the matlab variable that contains the model.

"""
import pandas as pd
import pandera as pa
import pandera.typing as pat
from typing import Dict, Union, List, Optional
import pathlib
import incawrapper.utils.chemical_formula as chemical_formula
from incawrapper.core.INCAScript import INCAScript
from incawrapper.core.dataschemas import ReactionsSchema, TracerSchema, FluxMeasurementsSchema, MSMeasurementsSchema, PoolSizeMeasurementsSchema
import warnings

@pa.check_input(ReactionsSchema)
def define_reactions(model_reactions: pd.DataFrame) -> str:
    """Write the matlab script block that to define the reactions in the model. The all reactions
    has to defined at once, so it is not possible to add reactions to the script block later on.
    
    Parameters
    ----------
    model_reactions: pd.DataFrame
        A dataframe with the reactions in the model. The dataframe is validated using the
        ReactionsSchema upon input.
    
    Returns
    -------
    str
        The matlab script block that defines the reactions in the model.
    """

    reaction_func_calls = model_reactions.apply(
        lambda row: instantiate_inca_class_call(
            inca_class='reaction', 
            S="'"+row["rxn_eqn"]+"'", 
            id="'" + row["rxn_id"] + "'",
        ), 
        axis=1
    )

    script = "% Create reactions\nr = [...\n"
    for reaction in reaction_func_calls:
        script += f"{reaction},...\n"
    script += "];"

    return script


@pa.check_input(TracerSchema)
def define_tracers(tracers: pd.DataFrame, experiment_id: str) -> str:
    """Writes a matlab script which defines the tracers used in one experiment. To define multiple 
    experiments this function has to be called multiple times. Most users will use this function 
    implicitly through the `create_inca_script_from_data()` function.
    
    Parameters
    ----------
    tracers: pd.DataFrame
        A dataframe with the tracers used in the model. The dataframe is validated using the 
        TracerSchema
    experiment_id: str
        The experiment id used to subset the tracers dataframe.
    
    Returns
    -------
    str
        The matlab script block that defines the tracers used in one experiment.
    """

    def create_tracer(tracer_id: str, met_id: str, atom_ids: List) -> str:
        """Parse a tracer into a string format readable by INCA.
        
        Parameters
        ----------
        tracer_id: str
            The unique id of the tracer, e.g. [1,2]Glc
        met_id: str
            The id of the metabolite which tracer is mass isotopomer of.
        atom_ids: List
            A list of the atom ids (numbers) that are labelled in the tracer.

        Returns
        -------
        str
            A string of matlab code that one tracer molecule.
        """
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
    """Define the flux measurements used in one experiment. Most users will use this function 
    implicitly through the `create_inca_script_from_data()` function.
    
    Parameters
    ----------
    flux_measurements: pd.DataFrame
        A dataframe with the flux measurements used in the model. The dataframe is validated using the
        FluxMeasurementsSchema
    experiment_id: str
        The experiment id used to subset the flux measurements dataframe.
    
    Returns
    -------
    str
        The matlab script block that defines the flux measurements used in one experiment.
    """

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
    """Define the pool measurements used in one experiment. Most users will use this function 
    implicitly through the `create_inca_script_from_data()` function.
    
    Parameters
    ----------
    pool_measurements: pd.DataFrame
        A dataframe with the pool measurements used in the model. The dataframe is validated using the
        PoolSizeMeasurementsSchema
    experiment_id: str
        The experiment id used to subset the pool measurements dataframe.
    
    Returns
    -------
    str
        The matlab script block that defines the pool measurements used in one experiment.
    """

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
    class_name: str,
    sub_class_name: Union[str, None],
    instance_id: str,
    properties: Dict,
) -> str:
    """Modify properties of a class instance in the model. This is useful for
    example to set the flux of a reaction to zero, specify a bounds 
    for a reaction, or to set metabolite as unbalanced.

    Parameters
    ----------
    class_name : str
        The name of the class to modify.
    sub_class_name : str or None
        The name of the sub class to modify. In some cases the class is split into
        sub classes. For example the class `rates` has a sub class `flx` for fluxes.
        If the class does not have sub classes, set this to None.
    instance_id : str
        The id of the instance to modify. For example the id of a reaction or a 
        metabolite id.
    properties : dict
        A dictionary with the properties to modify. The keys are the property names
        and the values are the new values for the property.

    Returns
    -------
    str
        A string with the INCA script that modifies the class instance.

    Notes
    -----
    Look in the INCA documentation for a list of all possible properties for the class
    (`<path-to-inca-folder>/doc/inca/class/`).

    Examples
    -------- 
    >>> modify_class('rates', 'flx', 'R_EX_glc__D_e', {'lb': -10, 'ub': 0})
    '''index_R_EX_glc__D_e = find(strcmp(m.rates.id, 'R_EX_glc__D_e'));
    m.rates.flx.lb(index_R_EX_glc__D_e) = -10;
    m.rates.flx.ub(index_R_EX_glc__D_e) = 0;'''
    >>> modify_class('rates', 'flx', 'R_EX_glc__D_e', {'val': 0, 'fix': True})
    '''index_R_EX_glc__D_e = find(strcmp(m.rates.id, 'R_EX_glc__D_e'));
    m.rates.flx.val(index_R_EX_glc__D_e) = 0;
    m.rates.flx.fix(index_R_EX_glc__D_e) = true;'''
    >>> modify_class('states', None, 'glc__D_e', {'bal': True})
    '''index_glc__D_e = find(strcmp(m.states.id, 'glc__D_e'));
    m.states.bal(index_glc__D_e) = true;'''

    """
    tmp_script = f"index_{instance_id} = find(strcmp(m.{class_name}.id, '{instance_id}'));\n"
    for k, v in properties.items():
        if isinstance(v, bool):
            v = f"{str(v).lower()}"
        
        if sub_class_name is not None:
            tmp_script += f"m.{class_name}.{sub_class_name}.{k}(index_{instance_id}) = {v};\n"
        else:
            tmp_script += f"m.{class_name}.{k}(index_{instance_id}) = {v};\n"

    return tmp_script


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
    """Loops over the ms_measurements dataframe and insert nan values for missing mass isotope measurements.
    
    Parameters
    ----------
    ms_measurements : pandas.DataFrame
        A dataframe with the ms_measurement data. The dataframe will be validated using
        the MSMeasurementsSchema.

    Returns
    -------
    pandas.DataFrame
        A dataframe with the same columns as the input dataframe but with gaps in the 
        mass_isotope column filled with consecutive integers starting from 0 and nan
        in the intensity and intensity_std_error columns for the missing values.
    """
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
    (<inca folder>/doc/inca/class).
    
    Parameters
    ----------
    inca_class : str
        The name of the INCA class.
    S : str
        The string that defines the class. The type of S depends on the class, but in
        most cases it is a string.
    **kwargs
        Define any properties of the class using keyword arguments.
        
    Returns
    -------
    str
        A string creates an instance of the INCA class.
    """

    kwargs_str = ", ".join([f"'{k}', {v}" for k, v in kwargs.items()])
    if not kwargs:
        return f"{inca_class}({S})"
    elif not S:
        return f"{inca_class}({kwargs_str})"

    return f"{inca_class}({S}, {kwargs_str})"


@pa.check_input(MSMeasurementsSchema)
def _define_ms_fragments(
    ms_measurements: pd.DataFrame, experiment_id: str
) -> str:
    """INCA's data model distinguishes between the ms fragments and the measurements of
    the fragments. This function defines the ms fragments for one experiment. The actual
    measurements are defined in the _define_ms_measurements function.

    Parameters
    ----------
    ms_measurements : pandas.DataFrame
        A dataframe with the ms_measurement data. The dataframe will be validated using
        the MSMeasurementsSchema.
    experiment_id : str
        The id of the experiment for which to define ms fragments.
    
    Returns
    -------
    str
        A string that defines the ms fragments that was measured in one experiment.
    """

    def _create_ms(
        ms_id: str,
        met_id: str,
        labelled_atom_ids: List,
        unlabelled_atoms: Optional[str] = None,
    ) -> str:
        """Create a string that defines one ms fragment."""

        labelled_atom_ids_string = " ".join(str(x) for x in labelled_atom_ids)
        ms_fragment_string = f"'{ms_id}: {met_id} @ {labelled_atom_ids_string}'"

        if unlabelled_atoms is not None and unlabelled_atoms != "" and not pd.isna(unlabelled_atoms):
            return instantiate_inca_class_call(
                "msdata", ms_fragment_string, more=f"'{unlabelled_atoms}'"
            )
        return instantiate_inca_class_call("msdata", ms_fragment_string)

    # subset the ms measurements to contain only one experiment
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
        # The ms_measurements dataframe contains multiple rows for each ms_id. The
        # information about the ms fragment is the same for all rows, so we only need
        # to use the first row.
        fragment_info = ms_df.iloc[0]
        if not "unlabelled_atoms" in fragment_info.index:
            tmp_script += _create_ms(
                ms_id,
                fragment_info["met_id"],
                fragment_info["labelled_atom_ids"],
            )
        else:
            tmp_script += _create_ms(
                ms_id,
                fragment_info["met_id"],
                fragment_info["labelled_atom_ids"],
                fragment_info["unlabelled_atoms"],
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
    of the individuals ms fragements.
    
    Parameters
    ----------
    ms_measurements : pandas.DataFrame
        A dataframe with the ms_measurement data. The dataframe will be validated using
        the MSMeasurementsSchema.
    experiment_id : str
        The id of the experiment for which to define ms measurements.
    
    Returns
    -------
    str
        A string that defines all the ms measurements for one experiment.
    """
    
    def add_idvs_to_msdata(
		experiment_id: str,
        ms_id: str,
        df: pat.DataFrame,
    ) -> str:
        """Write a line of matlab code to add measurements of one ms fragment to the
        msdata object. ALL measurements related that fragment has to be written in one
        line. Multiple measurements of a fragments can either originate from replicated 
        measurements or from multiple time points. 
        
        The idv() INCA class interprets one idv of a timepoint or replicate as a column 
        vector. Therefore the python lists are converted into matlab column vectors.

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
    """Wrapper function that first fills the mass isopomer measurement gaps, then the msdata objects (fragments) 
    and finally defines the ms measurements. Most users will use this function implicitly when using the
    define_ms_data_from_csv function.
    
    Parameters
    ----------
    ms_measurements : pandas.DataFrame
        A dataframe with the ms_measurement data. The dataframe will be validated using
        the MSMeasurementsSchema.
    experiment_id : str
        The id of the experiment for which to define ms measurements.
    
    Returns
    -------
    str
        A string that defines all the ms fragments and measurements for one experiment.
    """
    ms_measurements = fill_all_mass_isotope_gaps(ms_measurements)
    tmp_script = _define_ms_fragments(ms_measurements, experiment_id)
    tmp_script += _define_ms_measurements(ms_measurements, experiment_id)
    return tmp_script

def _inverse_dict(d):
    """Return a dictionary with the keys as the elements of the lists and the values 
    as the keys of the original dictionary. 
    
    Examples
    --------
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
    """Create a dictionary that defines which measurements are available for each experiment. Most users 
    will use this function implicitly through the `create_inca_script_from_data()` function.

    Examples
    --------
    >>> make_experimental_data_config(flux_measurements, ms_measurements)
    {'exp1': ['flux'], 'exp2': ['flux', 'ms'], 'exp3': ['ms']} 
    """

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
    a tracer object to be instantiated earlier in the matlab script this done through
    the `define_tracers()` function. This funciton relies on a variable naming convention
    in the matlab script discussed in the module docstring. Most users will use this function 
    implicitly through the `create_inca_script_from_data()` function. 
    
    Parameters
    ----------
    experiment_id : str
        The id of the experiment to define.
    measurement_types : List[str]
        A list of measurement types that are available for this experiment. The measurement
        types has to be one of the following: 'data_flx', 'data_ms', 'data_cxn', 'data_nmr'.

    Returns
    -------
    str
        A string of matlab code that defines an experiment. 

    Raises
    ------
    ValueError
        If the measurement type is not one of the valid types.
    NotImplementedError
        If the measurement type is 'data_nmr' as this is not yet supported.
    """

    data_list = list()
    for measurement_type in measurement_types:
        if measurement_type == "data_flx":
            data_list.extend(["'data_flx'", f"f_{experiment_id}"])
        elif measurement_type == "data_ms":
            data_list.extend(["'data_ms'", f"ms_{experiment_id}"])
        elif measurement_type == "data_cxn":
            data_list.extend(["'data_cxn'", f"p_{experiment_id}"])
        elif measurement_type == "data_nmr":
            raise NotImplementedError("NMR data is not yet supported")
            # data_list.extend(["'data_nmr'", f"nmr_{experiment_id}"])
        else:
            raise ValueError(
                f"Unknown measurement type {measurement_type}. Valid types are: 'data_flx', "
                "'data_ms', 'data_cxn'."
            )
    data_list_str = ", ".join(data_list)

    return f"e_{experiment_id} = experiment(t_{experiment_id}, 'id', '{experiment_id}', {data_list_str});\n"

def define_model(
    experiment_ids: List[str]
) -> str:
    """Write a line of matlab code to define a model. The functions relies on a variable naming
    convention in the matlab script discussed in the module docstring. Most users will use this function 
    implicitly through the `create_inca_script_from_data()` function.
    
    Parameters
    ----------
    experiment_ids : List[str]
        A list of experiment ids that should be included in the model.
        
    Returns
    -------
    str
        A string of matlab code that defines a model.
    """

    experiment_list = list()
    for experiment_id in experiment_ids:
        experiment_list.extend([f"e_{experiment_id}"])
    experiment_list_str = "[" + ",".join(experiment_list) + "]"

    return f"m = model(r, 'expts', {experiment_list_str});\n"


def define_options(**kwargs):
    """Write a line of matlab code to define options for the model.
    The available options can be found in the INCA documentation.
    `<inca-folder>/doc/inca/class/@option/option.html`. NB this function
    contains NO validation that the options are valid.
    
    Parameters
    ----------
    **kwargs
        Keyword arguments that are passed to the matlab option class. If you want to set the 
        fit_starts options to 10 simply pass `fit_starts=10` to this function.
        
    Returns
    -------
    str
        A string of matlab code that updates the options in the model.
    """
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
        Generate a MATLAB script that specifies which algorithms to be performed with the model.

        Parameters
        ----------
        output_filename : pathlib.Path
            Path to the output file. The output file will be a .mat file.
        run_estimate : bool, optional
            Whether to run flux estimation. Default True.
        run_simulation : bool, optional
            Whether to run a simulation. Default True. This is necessary for a fluxmap to be loaded 
            into INCA.
        run_continuation : bool, optional
            Whether to run parameter continuation. Default False.
        run_montecarlo : bool, optional
            Whether to run Monte Carlo algorithm. Default False.
        
        Returns
        -------
        str
            A string of matlab code that specifies which algorithms to be performed with the model and 
            where to save the results.
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