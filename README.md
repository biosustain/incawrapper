# incawrapper
incawrapper is a Python package which wraps for the matlab application INCA. INCA is a tool for
13C metabolic flux analysis. The incawrapper package allows to import data,
setup the model and run INCA all from within Python. The results can be exported
back to Python for further analysis and simply saved as .csv files. Furthermore, it is possible to 
export results from INCA runs entirely done through the GUI to Python. 

## What can the incawrapper do for me?
- Provide a Python interface to use INCA 100% independent of the INCA GUI
- Provide a data structure that can be imported to INCA
- Provide methods for exporting results from INCA to Python
- Provide methods for plotting results from INCA in Python
- Provide methods for creating INCA models with data, which can then be used in the INCA GUI
- Run both Isotopically Non-Stationary (INS) and Isotopically Stationary (IS) 13C-MFA
- Estimate fluxes and confidence intervals through the following INCA algorithms: estimate, parameter continuation, and Monte Carlo sampling

## What can the incawrapper NOT do for me?
- Integration of NMR data
- Simulation of experiments 
- Optimization of experimental design

## How to use it?
This is an extremely quick show case of the incawrapper for more extensive examples please see our documentation page. 

First, load your data typically atom mapped reactions, tracers information, flux measurements and MS measurements into pandas dataframes.
```python
import pandas as pd
tracers_data = pd.read_csv("tracers.csv", 
    converters={'atom_mdv':ast.literal_eval, 'atom_ids':ast.literal_eval} # a trick to read lists from csv
)
reactions_data = pd.read_csv("reactions.csv")
flux_data = pd.read_csv("flux_measurements.csv")
ms_data = pd.read_csv("ms_measurements.csv", 
   converters={'labelled_atom_ids': ast.literal_eval} # a trick to read lists from csv
)
```
Then create the inca script and specify the options and which INCA algorithms to execute.
```python
import incawrapper
output_file = "name/of/results/file.mat"
script = incawrapper.create_inca_script_from_data(reactions_data, tracers_data, flux_data, ms_data, experiment_ids=["exp1"])
script.add_to_block("options", incawrapper.define_options(fit_starts=5,sim_na=False))
script.add_to_block("runner", incawrapper.define_runner(output_file, run_estimate=True, run_simulation=True, run_continuation=True))
```
Now you are ready to run the inca script.
```python
from incawrapper import run_inca
inca_directory = "path/to/inca/installation"
run_inca(script, INCA_base_directory=inca_directory)
```
INCA will now run in the background and execute the specified algorithms and store the results in the `output_file`. This file can be open in the INCA GUI (using Open Flux Map) or imported into Python:
```python
res = incawrapper.INCAResults(output_file)
res.fitdata.fitted_parameters.head()
```
|    | type      | id      | eqn                |      val |       std |      lb |       ub |   free |...|
|---:|:----------|:--------|:-------------------|---------:|----------:|--------:|---------:|-------:|--:|
|  0 | Net flux  | R1      | A -> B             | 10       | 1e-05     | 9.99998 | 10       |      0 |...|
|  1 | Net flux  | R2 net  | B <-> D            |  6.08415 | 0.0680021 | 5.9477  |  6.2182  |      1 |...|
|  2 | Exch flux | R2 exch | B <-> D            |  6.62023 | 0.330634  | 6.00107 |  7.35286 |      1 |...|
|  3 | Net flux  | R3      | B -> C + E         |  1.95792 | 0.0340011 | 1.8909  |  2.02615 |      1 |...|
|  4 | Net flux  | R4      | B + C -> D + E + E |  1.95792 | 0.0340011 | 1.8909  |  2.02615 |      0 |...|


## Installation
For now, in order to install the incawrapper package, [clone this repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository) onto your machine. Once ready, find the path to the base folder of your incawrapper clone and pip install the package like this
`>>> cd /path/to/incawrapper/base/folder`
`>>> pip install ".[matlab]"`
Once released, incawrapper will be pip-installable. In a terminal, write
`>>> pip install incawrapper[matlab]`


## Supported Matlab and INCA versions
Both Matlab and INCA requires licenses which makes it difficult to automate testing of verison compatibility. For that reason will we only ensure compatibility with one INCA and one Matlab version. **Currently supporting:** **Matlab 2023a**, and **INCA v2.2**.


## Documentation and examples
Example use cases and a description of the API can be found in [our documentation](https://incawrapper.readthedocs.io/en/latest/index.html) (not uploaded yet).

## Contributing
We welcome all contributions.  Please follow the guidelines below when contributing code.

### Quick start
1. Fork the repository
2. Clone the repository
3. Make a new branch from `develop` (see git model below) with your feature or fix
4. Submit a pull request

### Git model
Please use the [GitFlow model](https://datasift.github.io/gitflow/IntroducingGitFlow.html#:~:text=GitFlow%20is%20a%20branching%20model,and%20scaling%20the%20development%20team)

### Documentation
Please use the [Numpy docstrings](https://numpydoc.readthedocs.io/en/latest/format.html) format

### Commit messages
Please use the following standard for commit messages
- `fix: ...` for all commits that deal with fixing an issue
- `feat: ...` for all commits that deal with adding a new feature
- `tests:...` for all commits that deal with unit testing
- `build:...` for all commits that deal with the CI infrastructure and deployment

### Pull requests
Please use the following PR title and description standards:
- The PR title should be short and descriptive.  Work in progress reviews should be titled as `WIP:...` and all other should follow the above for commit messages.
- The PR description should describe 1) new features, 2) fixes, and 3) other changes

### PR acceptance rules
In order to accept a PR, the following must be satisfied:
1. All new functions and classes have corresponding unit tests
2. All new functions and classes are documented using the correct style
3. All unit tests, linting tests, and integration tests pass
4. All new code is reviewed and approved by a repository maintainer
