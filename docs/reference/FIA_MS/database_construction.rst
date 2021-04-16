Database construction
=====================

.. currentmodule:: BFAIR.FIA_MS

The databases that are being used in the annotation process by SmartPeak
can be constructed using these tools. The output are struct and mapping files.
These databases can be expanded using the :doc:`BFAIR.io.database <../io/database>` tools.

Import these tools separate from the other FIA-MS tools like this:

.. code-block::

    >>> from BFAIR.FIA_MS import create_database

or together with the others like this:

.. code-block::

    >>> import BFAIR.FIA_MS as fia_ms


Functions
---------

Database construction
^^^^^^^^^^^^^^^^^^^^^

The databases are being created based on metabolic models. Please consult the example notebook
for an in depth walkthrough for various versions of metabolic models.

.. autosummary::
   :toctree: generated/

    create_database
