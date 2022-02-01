FIA-MS tools
============

.. currentmodule:: BFAIR.FIA_MS

The following tools can be used to extract metabolite data from ``.featureXML``
files (the outout of SmartPeak) into pandas DataFrames that can subsequently
be analyzed and visualized. Import these tools like this:

.. code-block::

    >>> import BFAIR.FIA_MS as fia_ms

Import
------

SmartPeak stores the processed analytical data in folders containing ``.featureXML``
files. In order to use this information in python, it has extracted from the
individual files and combined in a DataFrame. The extracted information can e.g.
be :doc:`normalized <../normalization/normalization>` after this step.

Functions
^^^^^^^^^

.. autosummary::
   :toctree: generated/

    extractNamesAndIntensities

Statistics
----------

Once reimported, the data can be summarized by combining replicates and descibed
by calculating basic statistics.

Functions
^^^^^^^^^
.. autosummary::
   :toctree: generated/

    calculateMeanVarRSD


