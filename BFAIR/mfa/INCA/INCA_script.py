#%%
import pandas as pd
import pandera as pa
import pandera.typing as pat
from typing import Iterable, Literal, Union, List
import pathlib
import time
import tempfile
import matlab.engine
import ast
import BFAIR.mfa.utils.chemical_formula as chemical_formula
import collections


class INCA_script:
    def __init__(self):
        self.reaction = "% REACTION BLOCK\n"
        self.tracers = "% TRACERS BLOCK\n"
        self.ms_fragments = "% MS_FRAGMENTS BLOCK\n"
        self.experimental_data = "% EXPERIMENTAL_DATA BLOCK\n"
        self.options = "% OPTIONS BLOCK\n"

        # The user is not intented to change these blocks
        self._define_model = "m = model(r, 'expts', experiments)"
        self._verify_model = (
            "m.rates.flx.val = mod2stoich(m); % make sure the fluxes are feasible"
        )

    def add_to_block(
        self,
        matlab_script_block: str,
        block_name: Literal["reaction", "ms_fragments", "experiments", "options"],
    ):
        """Add a matlab script block to a specific block of the INCA script.
        This block workflow ensures that the structure of the INCA script is
        correct. The blocks are: reaction, tracers, ms_fragments, experimental_data, options."""
        if block_name == "reaction":
            self.reaction += matlab_script_block
        elif block_name == "ms_fragments":
            self.ms_fragments += matlab_script_block
        elif block_name == "experiments":
            self.experimental_data += matlab_script_block
        elif block_name == "options":
            self.options += matlab_script_block
        else:
            print(
                f"Block name {block_name} not recognized. Has to be one of the following: reaction, tracers, ms_fragments, experiments, options."
            )

    def generate_script(self):
        """Generate the INCA script."""
        self.matlab_script = "\n\n".join(
            [
                "clear functions",
                self.reaction,
                self.tracers,
                self.ms_fragments,
                self.experimental_data,
                self.options,
                self._define_model,
                self._verify_model,
            ]
        )

    def _generate_runner_script(
        self,
        output_filename: pathlib.Path,
        run_continuation: bool = True,
        run_simulation: bool = True,
        run_montecarlo: bool = False,
    ) -> None:
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
        None
        """
        if run_montecarlo:
            raise NotImplementedError("Monte Carlo sampling is not implemented yet.")

        estimation = f"f = estimate(m);\n"
        continuation = "f=continuate(f,m);\n" if run_continuation else ""
        simulation = (
            "s=simulate(m);\n" if run_simulation else ""
        )  # For a fluxmap to be loaded into INCA, the .mat file must have a simulation
        output = f"filename = '{output_filename}';\n"

        if run_simulation:
            saving = "save(filename,'f','m','s');"
        else:
            saving = "save(filename,'f','m');"

        self.runner_script = estimation + continuation + simulation + output + saving

    def save_script(self, filename: pathlib.Path):
        """Save the INCA script to a file."""
        with open(filename, "w") as f:
            f.write(self.matlab_script)

    def save_runner_script(self, filename: pathlib.Path):
        """Save the INCA runner script to a file."""
        with open(filename, "w") as f:
            f.write(self.runner_script)


def run_inca(
    inca_script: INCA_script,
    INCA_base_directory: pathlib.Path,
    output_filename: pathlib.Path = None,
    run_simulation: bool = True,
    run_continuation: bool = False,
    run_montecarlo: bool = False,
) -> None:
    """Run INCA with a given INCA script."""

    # Create a temporary folder to store the INCA script and the runner script
    # The temporary folder will be deleted after the script is run
    if type(output_filename) is not pathlib.Path:
        output_filename = pathlib.Path(output_filename)
    if type(INCA_base_directory) is not pathlib.Path:
        INCA_base_directory = pathlib.Path(INCA_base_directory)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = pathlib.Path(temp_dir)

        # Write the INCA script to a file
        script_filename = "inca_script.m"
        inca_script.save_script(temp_dir / script_filename)
        print(f"INCA script saved to {temp_dir / script_filename}.")
        # Write the runner script to a file
        runner_filename = "inca_runner.m"
        inca_script._generate_runner_script(
            output_filename, run_continuation, run_simulation, run_montecarlo
        )
        inca_script.save_runner_script(temp_dir / runner_filename)

        # Run the INCA script
        start_time = time.time()
        print("Starting MATLAB engine...")
        eng = matlab.engine.start_matlab()
        eng.cd(str(INCA_base_directory.resolve()), nargout=0)
        eng.startup(nargout=0)
        eng.setpath(nargout=0)
        eng.cd(str(temp_dir.resolve()), nargout=0)
        _f = getattr(eng, str(script_filename.replace(".m", "")))
        _f(nargout=0)
        _f2 = getattr(eng, str(runner_filename.replace(".m", "")))
        _f2(nargout=0)
        eng.quit()
        print("--- %s seconds -" % (time.time() - start_time))


# Define the schema for the model reactions
model_reactions_schema = pa.DataFrameSchema(
    # TODO: Add validation for reaction arrow
    # TODO: Add validation for id uniqueness
    columns={
        "reaction": pa.Column(pa.String, required=True),
        "id": pa.Column(pa.String, required=True),
    }
)


@pa.check_input(model_reactions_schema)
def define_reactions(model_reactions: pd.DataFrame) -> str:
    def create_reaction(reaction_string: str, reaction_id: str) -> str:
        """Parse a reaction string into a function call of the INCA reaction."""
        return f"reaction('{reaction_string}', ['id'], ['{reaction_id}'])"

    reaction_func_calls = model_reactions.apply(
        lambda row: create_reaction(row["reaction"], row["id"]), axis=1
    )

    script = "% Create reactions\nr = [...\n"
    for reaction in reaction_func_calls:
        script += f"{reaction},...\n"
    script += "];"

    return script


def prepare_input(string, type_of_replacement=["Curly", "Double_square"]):
    """
    Process data that is stored in strings of lists etc in the files

    Parameters
    ----------
    string : string, in this set up a single cell in a pandas.DataFrame
        Processes the data in cells in the dataframes.
        The info is either bordered by curly or double square
        brackets.
    type_of_replacement : string
        Define the type of surrounding brackets

    Returns
    -------
    string : list
        returns data in lists without bordering brackets
    """
    if type_of_replacement == "Curly":
        string = string.strip("}{").split(",")
    elif type_of_replacement == "Double_square":
        string = string[1:-1]
        string = ast.literal_eval(string)
    return string


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


@pa.check_input(tracer_schema)
def define_tracers(tracers: pd.DataFrame, experiment_id: str) -> str:
    """Define the tracers used in one experiment. Multiple experiments
    are handled in the define_experiments function."""
    tmp_script = (
        "\n% define tracers used in the experiments\n"
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
    tmp_script += " ];\n"
    return tmp_script


# INCA_script.run_inca()

# inca_script.matlab_script
# inca_script.runner()

# def add(self, matlab_script_block: str, block_name: str)
#     self.block_name += matlab_script_string

# inca_script.add(define_reactions(model_reactions), 'reactions')
# inca_script = INCA_script()
# inca_script.add(define_reactions(model_reactions), 'reactions')

# inca_script.add(define_experiments(tracers, fluxes, ms), ['exp1', 'exp2'])

################ HERE
# def define_experiments(tracers: pd.DataFrame, fluxes: pd.DataFrame, ms: pd.DataFrame, experiment_ids: list = None):
# for experiment_id in experiment_ids:
#    f"Defining experiment {experiment_id}"
#    define_tracers(tracers, experiment_id)
#    define_fluxes(fluxes, experiment_id)
#    define_ms(ms, experiment_id)
#    ex_{experiment_id} = experiment(t_{experiment_id}, ['id', 'data_flx', 'data_ms'], [{experiment_id}, f_{experiment_id}, ms_{experiment_id}])

# inca_script.add(define_options(model_options), 'options')

# inca_script.generate_script()
# inca_script.generate_runner_script(output_filename)

# run_inca(inca_script: str, inca_base_directry: pathlib.Path, output_filename: pathlib.Path=None, run_simulation: bool=True, run_continuation: bool=False, run_montecarlo: bool = False)





#%%
tracer_df = pd.read_csv(
    "../../../tests/test_data/MFA_modelInputsData/simple_model/tracers.csv"
)
tracer_df_test = pd.DataFrame(
    {
        "experiment_id": ["exp1", "exp1"],
        "met_name": ["[1-13C]A", "[1,2-13C]B"],
        "met_id": ["A", "B"],
        "labelled_atoms": ["[1]", "[1,2]"],
        "ratio": [0.5, 0.5],
    }
)
print(define_tracers(tracer_df_test, "exp1"))
### Experiment structure
# add_experiment(experiment_id: str, tracer_df: pd.DataFrame, flux_df: pd.DataFrame, ms_df: pd.DataFrame)
# tracer data
# t_{experiment_id} = tracer({
# flux data
# ms data
# {experiment_id} = experiment(t, ['id', 'data_flx', 'data_ms'], [{experiment_id}, f, ms])

# m.expts = [{*experiment_ids}];


# %%
flux_measurements_schema = pa.DataFrameSchema(
    columns={
        "experiment_id": pa.Column(pa.String, required=True),
        "rxn_id": pa.Column(pa.String, required=True),
        "flux": pa.Column(pa.Float, required=True),
        "flux_std_error": pa.Column(pa.Float, required=True),
    }
)


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


# make a test dataframe for flux measurements
flux_measurements_test = pd.DataFrame(
    {
        "experiment_id": ["exp1", "exp1", "exp1"],
        "rxn_id": ["r1", "r2", "r3"],
        "flux": [1.0, 2.0, 3.0],
        "flux_std_error": [0.1, 0.2, 0.3],
    }
)
print(define_flux_measurements(flux_measurements_test, "exp1"))

# %%


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


ms_measurements_schema = pa.DataFrameSchema(
    columns={
        "experiment_id": pa.Column(pa.String, required=True),
        "met_id": pa.Column(pa.String, required=True),
        "ms_id": pa.Column(pa.String, required=True),
        "molecular_formula": pa.Column(
            pa.String, required=True, nullable=True
        ),  # nullable=True allows null values as nan or None
        "labelled_atoms": pa.Column(pa.String, required=True),
        #"idv": pa.Column(pa.Float, required=True),
        #"idv_std_error": pa.Column(pa.Float, required=True),
    }
)

def instantiate_inca_class_call(inca_class: str, S, **kwargs) -> str:
    """Create a string to instantiate an INCA class."""
    kwargs_str = ", ".join([f"'{k}', {v}" for k, v in kwargs.items()])
    if not kwargs:
        return f"{inca_class}({S})"
    return f"{inca_class}({S}, {kwargs_str})"

@pa.check_input(ms_measurements_schema)
def define_posible_ms_fragments(ms_measurements: pd.DataFrame, experiment_id: str) -> str:
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
            return instantiate_inca_class_call("msdata", ms_fragment_string, more=f"'{unlabelled_atoms}'")
        return instantiate_inca_class_call("msdata", ms_fragment_string)

        

    ms_measurements_subset = ms_measurements[
        ms_measurements["experiment_id"] == experiment_id
    ]
    tmp_script = (
        f"\n% define mass spectrometry measurements for experiment {experiment_id}\n"
        + f"ms_{experiment_id}"
        + " = [...\n"
    )

    for _, ms in ms_measurements_subset.iterrows():
        if ms["molecular_formula"] in [None, ""] or pd.isna(ms["molecular_formula"]):
            unlabelled_atoms = None
        else:
            unlabelled_atoms = get_unlabelled_atoms(
                ms["molecular_formula"], ms["labelled_atoms"]
            )

        tmp_script += create_ms(
            ms["ms_id"],
            ms["met_id"],
            ms["labelled_atoms"],
            unlabelled_atoms,
        )
        tmp_script += ",...\n"
    tmp_script += "];\n"
    return tmp_script


# make a test dataframe for ms measurements
ms_measuremets_test = pd.DataFrame(
    {
        "experiment_id": ["exp1", "exp1", "exp1"],
        "ms_id": ["ms1", "ms2", "ms3"],
        "met_id": ["A", "B", "C"],
        "labelled_atoms": ["[1,2]", "[C3,C4]", "[3]"],
        "molecular_formula": ["C7H19O", "C2H4Si", None],
        "idv": [[1.0,0.4], [2.0], [3.0]],
        "idv_std_error": [[0.1,0.2], [0.2], [0.3]],
        "time":[0,0,0]
    }
)

print(define_posible_ms_fragments(ms_measuremets_test, "exp1"))
#%%
def define_ms_measurements(ms_measurements: pd.DataFrame, experiment_id: str) -> str:
    """Defines measurements of ms fragments. This is done by updating the msdata objects 
    of the individuals ms fragements."""

    def add_idvs_to_msdata(
        experiment_id: str, 
        ms_id: str, 
        idv, #: Union[List[float], pd.Series[List[float]]], 
        idv_std_error, #: Union[List[float], pd.Series[List[float]]]
        time,
    ) -> str:
        """"""
        if isinstance(idv, pd.Series):
            # HERE
            pass
        else:
            idv_str = "[" + ";".join([str(i) for i in idv]) + "]"
            idv_std_error_str = "[" + ";".join([str(i) for i in idv_std_error]) + "]"
            idv_id = "'" + experiment_id + "_" + ms_id + "'"

        return f"ms_{experiment_id}{{'{ms_id}'}}.idvs = " + instantiate_inca_class_call("idv", idv_str, id=idv_id, std=idv_std_error_str, time=time)

    ms_measurements_subset = ms_measurements[ms_measurements["experiment_id"] == experiment_id]
    tmp_script = f"\n% define mass spectrometry measurements for experiment {experiment_id}\n"
    for _, ms in ms_measurements_subset.iterrows():
        tmp_script += add_idvs_to_msdata(experiment_id, ms["ms_id"], ms["idv"], ms["idv_std_error"], ms["time"])
        tmp_script += "\n"
    return tmp_script

print(define_ms_measurements(ms_measuremets_test, "exp1"))

# %%


def define_experiment(
    experiment_id: Union[str, List[str]],
    tracers: Union[pd.DataFrame, None] = None,
    flux_measurements: Union[pd.DataFrame, None] = None,
    ms_measurements: Union[pd.DataFrame, None] = None,
    pool_measurements: Union[pd.DataFrame, None] = None,
    nmr_measurements: Union[pd.DataFrame, None] = None,
) -> str:
    def experiment_is_in_measurement_type(experiment_id: Union[str, List[str]], s: pd.Series)-> bool:
        return experiment_id in s.unique()
    
    def create_experiment(experiment_id: str, measurement_types: List) -> str:
        data_list = list()
        for measurement_type in measurement_types:
            if measurement_type == 'data_flx':
                data_list.extend(["'data_flx'", f"f_{experiment_id}"])
            if measurement_type == 'data_ms':
                data_list.extend(["'data_ms'", f"ms_{experiment_id}"])
            if measurement_type == 'data_cxn':
                data_list.extend(["'data_cxn'", f"cxn_{experiment_id}"])
            if measurement_type == 'data_nmr':
                data_list.extend(["'data_nmr'", f"nmr_{experiment_id}"])
        data_list_str = ", ".join(data_list)
        return f"experiment('{experiment_id}', {data_list_str})"
    tmp_script = "\n% define experimental data\n"
    # The following chunk adds the experimental data to the script
    measurement_types_dict = dict() # dict collecting the measurement types for each experiment
    for experiment in experiment_id:
        measurement_types_dict[experiment] = list()
        if tracers is not None:
            tmp_script += define_tracers(tracers, experiment)

        if flux_measurements is not None:
           if experiment_is_in_measurement_type(experiment, flux_measurements["experiment_id"]):
                measurement_types_dict[experiment].append("data_flx")
                tmp_script += define_flux_measurements(flux_measurements, experiment)

        if ms_measurements is not None:
           if experiment_is_in_measurement_type(experiment, ms_measurements["experiment_id"]):
                measurement_types_dict[experiment].append("data_ms")
                tmp_script += define_ms_measurements(ms_measurements, experiment)

        if pool_measurements is not None:
            raise NotImplementedError("Pool measurements not implemented yet.")
            # if experiment_is_in_measurement_type(experiment, pool_measurements["experiment_id"]):
            #   measurement_types_dict[experiment].append("data_cxn")
            #   tmp_script += define_pool_measurements(pool_measurements, experiment)
        
        if nmr_measurements is not None:
            raise NotImplementedError("NMR measurements not implemented yet.")
            # if experiment_is_in_measurement_type(experiment, nmr_measurements["experiment_id"]):
            #   measurement_types_dict[experiment].append("data_nmr")
            #   tmp_script += define_nmr_measurements(nmr_measurements, experiment)

    # The following chunk defines which data is associated for which experiment
    tmp_script += "\n% define experiments\n"
    tmp_script += "experiments = [...\n" 
    for experiment in experiment_id:
        tmp_script += create_experiment(experiment, measurement_types_dict[experiment])
        tmp_script += ",...\n"
    tmp_script += "];\n"

    return tmp_script

print(define_experiment(["exp1"], tracer_df_test , flux_measurements_test, ms_measuremets_test))
# %%

reaction_test = pd.DataFrame(
    {"reaction": ["A (C1:a C2:b) -> B (C1:b C2:a)", "B -> C", "C -> D"], "id": ["r1", "r2", "r3"]}
)
inca_script = INCA_script()
inca_script.add_to_block(define_reactions(reaction_test), "reaction")
inca_script.add_to_block(define_experiment(["exp1"], tracer_df_test , flux_measurements_test, ms_measuremets_test), "experiments")
inca_script.generate_script()
inca_script.save_script("test_script.m")
run_inca(inca_script, '/Users/s143838/inca2.1', "test_script.mat",)


# %%
