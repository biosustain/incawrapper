MFA input data processing
=========================

.. currentmodule:: BFAIR.mfa.INCA

Metabolic flux analysis prerequisites
-------------------------------------

In order to run a metabolic flux analysis (MFA), we need the information that is listed below.
Except for atom mapping, all the other inputs can be prepared automatically using BFAIR.

* Metabolic model info - ``INCA.parse_cobra_model``
* Atom mapping info - not automatically available yet
* Experimental data - Obtained from SmartPeak, parser will be provided
* Tracer info - parser will be provided
* Flux info - Output of the exometabolomics module, link will be provided

Here we aim to describe how you should prepare your data.

Metabolic model
---------------

The information about the underlying metabolic model can be extracted from a COBRA model.
This will be the basis of you MFA. The metabolic model can be provided as a ``.json`` or
a ``.sbml`` file.

.. autosummary::
   :toctree: generated/

   parse_cobra_model

Standard input parsers
----------------------

Parsers for standard input formats are provided.

.. currentmodule:: BFAIR.parsers

.. autosummary::
   :toctree: generated/

   data_import_parsers
