# BFAIR
Big and F.A.I.R. Omics Data. This package provides tools for high throughput metabolomics analysis, both targeted and untargeted, making use of (and facilitating) different types of metabolic models. For a detailed documentation, please check [our ReadtheDocs](https://bfair.readthedocs.io/en/latest/index.html).

## Installation
For now, in order to install the BFAIR package, [clone this repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository) onto your machine. Once ready, find the path to the base folder of your BFAIR clone and pip install the package like this
`>>> pip install /path/to/BFAIR/base/folder`
Once released, BFAIR will be pip-installable. In a terminal, write
`>>> pip install BFAIR`

## Features
BFAIR provides a metabolomics analysis toolbox including, but not limited to:
- Tools for analyzing untargeted FIA-MS metabolomics data
- Tools for a general analysis of targeted metabolomics
- A full metabolic flux analysis (MFA) workflow combined with our sister-software [SmartPeak](https://github.com/AutoFlowResearch/SmartPeak)
- Input preparation for the MFA workflow, including exometabolomics analysis, COBRA model parsing, MDV parsing and automated atom mapping

## Examples
Extensive examples can be found in the "example notebooks" section of [our documentation](https://bfair.readthedocs.io/en/latest/index.html). These are Jupyter Notebooks presenting a typical use case for each of the described modules. The notebooks can be found in [this location](https://github.com/AutoFlowResearch/BFAIR/tree/develop/docs/examples) in the repository.

## Contributing
We welcome all contributions.  Please follow the guidelines below when contributing code.

### Quick start
1. Fork the repository
2. Clone the repository
3. Make a new branch from `develop` (see git model below) with your feature or fix
4. Submita pull request

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
