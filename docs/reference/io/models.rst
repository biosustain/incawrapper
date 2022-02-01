Metabolic models
================

.. currentmodule:: BFAIR.io.model_factory

Factory classes
---------------

BFAIR contains pre-curated genome-scale metabolic models that can be accessed
through the ``models`` or ``thermo_models`` classes.

.. autodata:: models
   :annotation:

.. autodata:: thermo_models
   :annotation:

Functions
---------

Alternatively (and equivalently), one can manually load genome-scale models
using the following functions:

.. autosummary::
   :toctree: generated/

   load_cbm
   load_data
   create_model