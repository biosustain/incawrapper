Rule library
============

Overview
--------

.. currentmodule:: BFAIR.pathways
.. autoclass:: RuleLibrary
   :exclude-members:

Methods
-------

Opening and closing the rule database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``RuleLibrary`` object is an interface to a SQL database of reaction rules. Used as a context manager, the
connection to the database is automatically established. However, if one desires so, it is also possible to manually
open and close the database.

.. autosummary::
   :toctree: generated/

   RuleLibrary.open
   RuleLibrary.close

Adding and removing filters
^^^^^^^^^^^^^^^^^^^^^^^^^^^

To obtain a subset of reaction rules to work with, there are several filters that can be applied to a ``RuleLibrary``.
For instance, one can select the reactions that are only available in yeast or rules that have certain specificity.
Multiple filters can be combined.

.. autosummary::
   :toctree: generated/

   RuleLibrary.filter_by_compound
   RuleLibrary.filter_by_diameter
   RuleLibrary.filter_by_organism
   RuleLibrary.filter_by_uncertainty
   RuleLibrary.pop_filter
   RuleLibrary.reset

Applying reaction rules
^^^^^^^^^^^^^^^^^^^^^^^

Finally, once a subset of rules has been selected, the reaction rules can be applied to a compound (typically a known
intermediate from a heterologous pathway). This will produce a list of products that can stem from the input source.
Further pruning over this list can produce a list of off-products that arise from unexpected promiscuous enzymatic
activity.

.. autosummary::
   :toctree: generated/

   RuleLibrary.apply_to
   RuleLibrary.list_products
