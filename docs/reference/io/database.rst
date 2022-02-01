Database
========

.. currentmodule:: BFAIR.io.database

A metabolite database is represented by two types of files: a struct and
a mapping. These databases are used in the annotation process ran by
SmartPeak.

Both files are in :abbr:`TSV (tab-separated values)` format. Functions
to handle these files have to be imported from the ``io`` module.

.. code-block::

    >>> from BFAIR.io import struct, mapping

Struct
------

Struct files contain 4 columns of metabolite ID, formula, SMILES, and
InChI. Only the first two columns are used by SmartPeak, so the rest can be
filled with placeholders. As in the example:

.. code-block::

    >>> struct_test = struct.read("struct_test.tsv")
    >>> struct_test.head()
    id      formula    unused_smiles    unused_inchi
    ------  ---------  ---------------  --------------
    glc__D  C6H12O6    smiles           inchi
    gln__L  C5H10N2O3  smiles           inchi
    glu__L  C5H9NO4    smiles           inchi
    glx     C2H2O3     smiles           inchi
    h2o     H2O        smiles           inchi


Functions
^^^^^^^^^

The ``struct`` module contains functions to read, create, merge, and read
struct files.

.. autosummary::
   :toctree: generated/

   struct.from_inchis
   struct.from_products_dict
   struct.merge
   struct.read
   struct.rename_metabolites
   struct.write

Mapping
-------

A mapping file summarizes a struct file by grouping metabolites by their
formula. These data structures contain 3 columns of mass, formula, and
metabolite IDs. The mass column is unused, so it typically contains 0 as a
placeholder.

.. code-block::

    >>> mapping_test = mapping.from_struct(struct_test)
    >>> mapping_test.head()
      unused_mass  formula        ids
    -------------  -------------  --------
                0  C10H14N5O7P    ['amp']
                0  C10H15N5O10P2  ['adp']
                0  C10H16N5O13P3  ['atp']
                0  C21H28N7O14P2  ['nad']
                0  C21H29N7O14P2  ['nadh']



Functions
^^^^^^^^^

The ``mapping`` module contains functions to read, create, merge, and read
mapping files.

.. autosummary::
   :toctree: generated/

   mapping.from_struct
   mapping.merge
   mapping.read
   mapping.write
