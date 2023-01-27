#%%
import pandas as pd
import pandera as pa
import pandera.typing as pat
from typing import Literal
import pathlib
import time
import tempfile
import matlab
import ast


class INCA_script:
    def __init__(self):
        self.reaction = "% REACTION BLOCK\n" 
        self.tracers = "% TRACERS BLOCK\n"
        self.ms_fragments = "% MS_FRAGMENTS BLOCK\n"
        self.experimental_data = "% EXPERIMENTAL_DATA BLOCK\n"
        self.options = "% OPTIONS BLOCK\n"

        # The user is not intented to change these blocks
        self._define_model = "m = model(r)"
        self._verify_model = "m.rates.flx.val = mod2stoich(m); % make sure the fluxes are feasible"


    def add_to_block(self, matlab_script_block: str, block_name: Literal['reaction', 'ms_fragments', 'experimentals', 'options']):
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
            print(f"Block name {block_name} not recognized. Has to be one of the following: reaction, tracers, ms_fragments, experimental_data, options.")


    def generate_script(self):
        """Generate the INCA script."""
        self.matlab_script = "\n\n".join(
            [
                "clear functions",
                self.reaction,
                self._define_model,
                self._verify_model,
                self.tracers,
                self.ms_fragments,
                self.experimental_data,
                self.options,
            ]
        )

   
    def _generate_runner_script(self, output_filename: pathlib.Path, run_continuation: bool=True, run_simulation: bool=True, run_montecarlo: bool=False)->None:
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
            simulation = "s=simulate(m);\n" if run_simulation else "" # For a fluxmap to be loaded into INCA, the .mat file must have a simulation
            output = f"filename = '{output_filename}';\n"

            if run_simulation:
                saving = "save(filename,'f','m','s');"
            else:
                saving = "save(filename,'f','m');"

            self.runner_script = (
                estimation + 
                continuation + 
                simulation + 
                output + 
                saving
            )
    def save_script(self, filename: pathlib.Path):
        """Save the INCA script to a file."""
        with open(filename, "w") as f:
            f.write(self.matlab_script)
    
    def save_runner_script(self, filename: pathlib.Path):
        """Save the INCA runner script to a file."""
        with open(filename, "w") as f:
            f.write(self.runner_script)


def run_inca(inca_script: INCA_script, INCA_base_directory: pathlib.Path, output_filename: pathlib.Path=None, run_simulation: bool=True, run_continuation: bool=False, run_montecarlo: bool = False)->None:
    """Run INCA with a given INCA script."""

    # Create a temporary folder to store the INCA script and the runner script
    # The temporary folder will be deleted after the script is run
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = pathlib.Path(temp_dir)

        # Write the INCA script to a file
        script_filename = "inca_script.m"
        inca_script.save_script(temp_dir / script_filename)

        # Write the runner script to a file
        runner_filename = "inca_runner.m"
        inca_script._generate_runner_script(output_filename, run_continuation, run_simulation, run_montecarlo)
        inca_script.save_runner_script(temp_dir / runner_filename)

        # Run the INCA script
        start_time = time.time()
        eng = matlab.engine.start_matlab()
        eng.cd(r"" + INCA_base_directory, nargout=0)
        eng.startup(nargout=0)
        eng.setpath(nargout=0)
        eng.cd(r"" + temp_dir, nargout=0)
        _f = getattr(eng, script_filename)
        _f(nargout=0)
        _f2 = getattr(eng, runner_filename)
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
        return f"reaction('{reaction_string}', [id], ['{reaction_id}'])"
    reaction_func_calls = model_reactions.apply(lambda row: create_reaction(row["reaction"], row["id"]), axis=1)

    script = "% Create reactions\nr = [...\n"
    for reaction in reaction_func_calls:
        script += f"{reaction},...\n"
    script += "];"

    return script 

def prepare_input(
        string, type_of_replacement=["Curly", "Double_square"]
    ):
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
        "labelled_atoms": pa.Column(pa.String, required=True), #  "List of labelled atoms in the metabolite. E.g. [1,2] or [C1,C2]"
        "ratio": pa.Column(pa.Float, required=True), 
    }
)

pa.check_input(model_reactions_schema)
def define_tracers(tracers: pd.DataFrame, experiment_id: str) -> str:
    """Define the tracers used in one experiment. Multiple experiments 
    are handled in the define_experiments function."""
    tmp_script = (
        "\n% define tracers used in the experiments\n"
        +f"t_{experiment_id}"
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
    tmp_script += "\n% define fractions of tracers_subset used\nt.frac = [" 

    tmp_script += ",".join(tracers_subset['ratio'].astype(str).tolist())
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


test_df = pd.DataFrame({"reaction": ["A (C1:a, C2:b) -> B (C1:b, C2:a)", "B -> C"], "id": ["r1", "r2"]})

inca_script = INCA_script()

inca_script.generate_script()
print(inca_script.matlab_script)

#%%
tracer_df = pd.read_csv("../../../tests/test_data/MFA_modelInputsData/simple_model/tracers.csv")
tracer_df_test = pd.DataFrame(
    {
        "experiment_id": ["exp1", "exp1"],
        "met_name": ["[1-13C]A", "[1,2-13C]B"],
        "met_id": ["A", "B"],
        "labelled_atoms": ["[1]", "[1,2]"],
        "ratio": [0.5, 0.5],
    }
)
define_tracers(tracer_df_test, "exp1")
### Experiment structure
# add_experiment(experiment_id: str, tracer_df: pd.DataFrame, flux_df: pd.DataFrame, ms_df: pd.DataFrame)
# tracer data
# t_{experiment_id} = tracer({
# flux data
# ms data
# {experiment_id} = experiment(t, ['id', 'data_flx', 'data_ms'], [{experiment_id}, f, ms])

# m.expts = [{*experiment_ids}];


# %%
