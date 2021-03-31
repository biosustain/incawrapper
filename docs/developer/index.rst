Contributor Guide
=================

We welcome all contributions.  Please follow the guidelines below when contributing code.

Quickstart
----------

1. Fork the repository
2. Clone the repository
3. Make a new branch from `develop` (see git model below) with your feature or fix
4. Submit a pull request

Guidelines
----------

- Please use the `GitFlow model <https://datasift.github.io/gitflow/IntroducingGitFlow.html>`_.
- Please use `Numpy docstrings <https://numpydoc.readthedocs.io/en/latest/format.html>`_.
- Please use the following `standard prefixes for commit messages <https://www.conventionalcommits.org/en/v1.0.0/>`_:

  - ``fix``: for all commits that deal with fixing an issue,
  - ``feat``: for all commits that deal with adding a new feature,
  - ``test``: for all commits that deal with unit testing,
  - ``build``: for all commits that deal with the CI infrastructure and deployment,
  - ``docs``: to identify documentation changes,
  - ``perf``: to identify changes related to performance improvements,
  - ``style``: to identify changes related to styling (e.g., indentations, semi-colons, quotes, etc.), and
  - ``refactor``: for all commits that deal with changes in code that neither add or fix a feature (e.g., renaming
    variables, simplifying codes, removing redundant code, etc.).

- Please use the following PR title and description standards:

  - The PR title should be short and descriptive.  Work in progress reviews should be titled as ``WIP:...`` and all
    other should follow the above for commit messages.
  - The PR description should describe 1) new features, 2) fixes, and 3) other changes.

PR Acceptance Rules
^^^^^^^^^^^^^^^^^^^

In order to accept a PR, the following must be satisfied:

1. All new functions and classes have corresponding unit tests.
2. All new functions and classes are documented using the correct style.
3. All unit tests, linting tests, and integration tests pass.
4. All new code is reviewed and approved by a repository maintainer.