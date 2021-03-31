Utils
=====

.. currentmodule:: BFAIR.pathways.utils

The utils module offers a toolbox to handle chemical compounds and calculate structural similarity scores between them.
It must be manually imported:

.. code-block::

   >>> from BFAIR.pathways import utils

Functions
---------

Handling chemical compounds
^^^^^^^^^^^^^^^^^^^^^^^^^^^

With these functions, one can convert a string depection of a molecule (such as InChI or SMILES) into a RDKit molecule
object. These molecules are standardized for the sake of cohesiveness.

.. autosummary::
   :toctree: generated/

   get_compound
   standardize

Calculating chemical similarity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A molecular fingerprint is a list of indices that represent substructural features of a chemical compound. They are
useful tools to compare the similarities between two molecules. For instance, the algorithm used in the
`calculate_similarity` routine uses the Tanimoto coefficient, which is the intersection of structural properties
(indices) divided by their union.

.. autosummary::
   :toctree: generated/

   calculate_similarity
   get_molecular_fingerprint
