Installation
===============

incawrapper requires Python 3.6. The recommended installation method is `pip <https://pip.pypa.io/en/stable/>`_.

.. code-block:: bash

    pip install incawrapper[matlab]

Alternatively, you can download the source code from `GitHub <github.com/biosustain/incawrapper>`_ and install it manually.

.. code-block:: bash

    git clone github.com/biosustain/incawrapper
    cd incawrapper
    pip install incawrapper[matlab]


To run INCA you furthermore need to install matlab (>2022b this allows installation of the matlabengine 
package through pip) and the INCA software (https://mfa.vueinnovations.com/).

Use without matlab
-------------------
The incawrapper can be used analyse INCA output files (.mat) without matlab. In that case install the package without the matlab extras:
using the following command:

.. code-block:: bash

    pip install incawrapper

The incawrapper can then be used to read INCA output files and to create a INCA scripts, but will not be able 
to run INCA.