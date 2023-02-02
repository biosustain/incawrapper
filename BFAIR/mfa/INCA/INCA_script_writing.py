import pandas as pd
import pandera as pa
import pandera.typing as pat
from typing import Dict, Iterable, Literal, Union, List
import pathlib
import time
import tempfile
import matlab.engine
import ast
import BFAIR.mfa.utils.chemical_formula as chemical_formula
import collections
from BFAIR.mfa.INCA.dataschemas import model_reactions_schema, tracer_schema, flux_measurements_schema, ms_measurements_schema
import warnings

@pa.check_input(model_reactions_schema)
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


@pa.check_input(tracer_schema)
def define_tracers(tracers: pd.DataFrame, experiment_id: str) -> str:
    """Define the tracers used in one experiment. Multiple experiments
    are handled in the define_experiments function."""
    tmp_script = (
        "% define tracers used in the experiments\n"
        + f"t_{experiment_id}"
        + " = tracer({...\n"  # noqa E501
    )

    def create_tracer(met_name: str, met_id: str, labelled_atoms: str) -> str:
        """Parse a tracer into a string format readable by INCA."""
        labelled_atoms_parsed = labelled_atoms.strip("}{").strip("][").split(",")
        labelled_atoms_string = " ".join(labelled_atoms_parsed)
        return f"'{met_name}: {met_id} @ {labelled_atoms_string}'"

    tracers_subset = tracers[tracers["experiment_id"] == experiment_id]

    for _, tracer in tracers_subset.iterrows():
        tracer_string = create_tracer(
            tracer["met_name"],
            tracer["met_id"],
            tracer["labelled_atoms"],
        )
        tmp_script += f"{tracer_string},...\n"

    tmp_script += "});\n"
    tmp_script += (
        f"\n% define fractions of tracers_subset used\nt_{experiment_id}.frac = ["
    )

    tmp_script += ",".join(tracers_subset["ratio"].astype(str).tolist())
    tmp_script += " ];"
    return tmp_script


@pa.check_input(flux_measurements_schema)
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


def get_unlabelled_atoms(molecular_formula: str, labelled_atoms: str) -> str:
    """
    Get the unlabelled atoms in a molecule by substrating the labelled atoms.

    Parameters
    ----------
        molecular_formula: str
            The molecular formula of the molecule.
        labelled_atoms: str
            The labelled atoms in the molecule.

    Returns
    -------
        unlabelled_atoms: str
            A molecular formula string of the unlabelled atoms.
    """
    formula_dict = chemical_formula._create_compound_dict(molecular_formula)
    labelled_atoms_formula = chemical_formula.create_formula_from_dict(
        collections.Counter(labelled_atoms)
    )
    unlabelled_atoms_formula = chemical_formula.subtract_formula(
        molecular_formula,
        labelled_atoms_formula,
    )

    return unlabelled_atoms_formula





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


@pa.check_input(ms_measurements_schema)
def define_possible_ms_fragments(
    ms_measurements: pd.DataFrame, experiment_id: str
) -> str:
    """INCA's data model distinguishes between the ms fragments and the measurements of
    the fragments. This function defines the possible ms fragments that was measured,
    in one experiment. Multiple experiments is handled in the define_experiments function.
    """

    def create_ms(
        ms_id: str,
        met_id,
        labelled_atoms,
        unlabelled_atoms,
    ) -> str:
        labelled_atoms_parsed = labelled_atoms.strip("}{").strip("][").split(",")
        labelled_atoms_string = " ".join(labelled_atoms_parsed)
        ms_fragment_string = f"'{ms_id}: {met_id} @ {labelled_atoms_string}'"

        if unlabelled_atoms is not None:
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
        if ms_df["molecular_formula"] in [None, ""] or pd.isna(
            ms_df["molecular_formula"]
        ):
            unlabelled_atoms = None
        else:
            unlabelled_atoms = get_unlabelled_atoms(
                ms_df["molecular_formula"], ms_df["labelled_atoms"]
            )

        tmp_script += create_ms(
            ms_id,
            ms_df["met_id"],
            ms_df["labelled_atoms"],
            unlabelled_atoms,
        )
        tmp_script += ",...\n"
    tmp_script += "];\n"
    return tmp_script


def matlab_column_vector(lst: List[float]) -> str:
    """Convert a list to a matlab column vector string. These are of the fortmat
    [1;2;3;4;5]"""
    return "[" + ";".join([str(i) for i in lst]) + "]"

@pa.check_input(ms_measurements_schema)
def define_ms_measurements(ms_measurements: pd.DataFrame, experiment_id: str) -> str:
    """Defines measurements of ms fragments. This is done by updating the msdata objects
    of the individuals ms fragements."""
    
    def add_idvs_to_msdata(
        experiment_id: pat.Series[str],
        ms_id: pat.Series[str],
        idv: pat.Series[List],
        idv_std_error: pat.Series[List],
        time: pat.Series[float],
    ) -> str:
        """Write a line of matlab code to add measurements of one ms fragment to the
        msdata object. It is allowed to have multiple measurements of the same ms
        fragment. The idv() INCA class interprets one idv as a column vector. Therefore
        convert the python lists to matlab column vectors.

        Each measurement is given a unique id. This is done by concatenating the
        experiment_id, ms_id, time and replicate number.
        """

        replicate_counter = 0
        idv_id_lst = []
        idv_str = "["
        idv_std_error_str = "["
        for idx, _ in idv.items():
            idv_str += matlab_column_vector(idv[idx]) + ","
            idv_std_error_str += matlab_column_vector(idv_std_error[idx]) + ","
            replicate_counter += 1
            idv_id_lst.append(
                "'"
                + experiment_id
                + "_"
                + ms_id
                + "_"
                + str(time)
                + "_"
                + str(replicate_counter)
                + "'"
            )

        # remove last comma
        idv_str = idv_str.rstrip(",")
        idv_std_error_str = idv_std_error_str.rstrip(",")
        idv_str += "]"
        idv_std_error_str += "]"

        idv_id = "{" + ",".join(idv_id_lst) + "}"

        return (
            f"ms_{experiment_id}{{'{ms_id}'}}.idvs = " + 
            instantiate_inca_class_call(
                "idv", idv_str, id=idv_id, std=idv_std_error_str, time=time
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
            ms_df["idv"],
            ms_df["idv_std_error"],
            ms_df["time"].iloc[0],
        )
        tmp_script += "\n"
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
            data_list.extend(["'data_cxn'", f"cxn_{experiment_id}"])
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
        if run_montecarlo:
            raise NotImplementedError("Monte Carlo sampling is not implemented yet.")

        estimation = "f = estimate(m);\n" if run_estimate else ""
        continuation = "f=continuate(f,m);\n" if run_continuation else ""
        simulation = (
            "s=simulate(m);\n" if run_simulation else ""
        )  # For a fluxmap to be loaded into INCA, the .mat file must have a simulation

        output = f"filename = '{output_filename}';\n"

        saving = "save(filename, "
        if run_estimate:
            saving += "'f', "
        if run_simulation:
            saving += "'s', "

        saving += "'m');\n"

        return estimation + continuation + simulation + output + saving
    

