Pre-requisites and installation
===============================

Pre-requisites
----------------
To fully use the incawrapper you need to install the following software:

* Python
* matlab (>2022b this allows installation of the matlabengine package through pip)
* INCA software (https://mfa.vueinnovations.com/)

Both matlab and INCA are commercial software and the each user needs to acquire a license. The incawrapper can be used without a matlab or INCA license, but will not be able to run INCA (See below).

How to install
----------------
incawrapper requires Python. The recommended installation method is `pip <https://pip.pypa.io/en/stable/>`_.

.. code-block:: bash

    pip install incawrapper[matlab]

Alternatively, you can download the source code from `GitHub <github.com/biosustain/incawrapper>`_ and install it manually.

.. code-block:: bash

    git clone github.com/biosustain/incawrapper
    cd incawrapper
    pip install incawrapper[matlab]


Use without matlab
-------------------
The incawrapper can be used analyse INCA output files (.mat) without matlab. In that case install the package without the matlab using the following command:

.. code-block:: bash

    pip install incawrapper

With this installation the incawrapper can read INCA output files and to create a INCA scripts, but will not be able 
to run INCA.