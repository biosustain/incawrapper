Pre-requisites and installation
===============================

Pre-requisites
----------------
To fully use the incawrapper you need to install the following software:

* Python
* matlab (>2022b this allows installation of the matlabengine package through pip)
* matlab Statistics and Machine Learning Toolbox and Optimization Toolbox (installed through the matlab Add-on manager)
* INCA software (https://mfa.vueinnovations.com/)

Both matlab and INCA are commercial software and the each user needs to acquire a license. The incawrapper can be used without a matlab or INCA license, but will not be able to run INCA (See below).

* matlab: Get a free academic licence and install MATLAB from https://www.mathworks.com. Then, install the engine API following the guide provided `under this link <https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html>`_. In brief, you will have to go to your MATLAB root folder (find your installation and open that folder) and go to "/extern/engines/python" and run "python setup.py install" from the command line.
* INCA: INCA (Isotopomer Network Compartmental Analysis) is a MATLAB-based software package for isotopomer network modeling and metabolic flux analysis." You can read more about it in `Young, 2014 <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3998137/pdf/btu015.pdf>`_. If you are in academia, you can get a free academic licence for INCA from the `Vanderbilt University website <https://mfa.vueinnovations.com/>`_ (the second option is the relevant one) and install it. Find the path to the base directory of your INCA installation, you will need it later.

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