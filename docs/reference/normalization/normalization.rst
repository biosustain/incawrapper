Normalization
=============

.. currentmodule:: BFAIR.normalization

Normalization is crucial in order to make your data comparable between different
experiments, or even just different samples. To make this process easier, we provide
a catalogue of different normalization techniques along with descriptions about their
intended use in the corresponding example notebook. These functions can be imported
like this:

.. code-block::

   >>> import BFAIR.normalization as normalization

These normalization tools are designed for the shape of the intermediate- and
output dataframes produced by the BFAIR metabolomics tools (e.g. FIA-MS), like
the following example:

.. code-block::

    >>> intensities_Ecoli.head()
    sample_group_name            Metabolite    Formula      Intensity
    ---------------------------  ------------  ---------  -----------
    Linearity_P1Ecoli_100xDil_1  12dgr120_c    C27H52O5       9583.65
    Linearity_P1Ecoli_100xDil_1  12dgr140_c    C31H60O5       1276.41
    Linearity_P1Ecoli_100xDil_1  12dgr141_c    C31H56O5       1282.27
    Linearity_P1Ecoli_100xDil_1  12dgr160_c    C35H68O5      29685.5
    Linearity_P1Ecoli_100xDil_1  12dgr161_c    C35H64O5      21447.5

Functions
---------

The functions included in this toolbox can be separated into the following categories

Feature scaling
^^^^^^^^^^^^^^^

These methods scale your data into a predefined range, e.g. from 0 to 1.

.. autosummary::
   :toctree: generated/

   min_max_norm

Total Sum Intentensity normalization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All of these methods are variations of a :abbr:`TSI (Total Sum Intentensity)` type
normalization, where each value is divided by the sum of all values in the same sample

.. autosummary::
   :toctree: generated/

   tsi_norm
   lim_tsi_norm
   pqn_norm
