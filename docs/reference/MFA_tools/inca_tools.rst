INCA
====

.. currentmodule:: BFAIR.INCA

Prerequisites
-------------

The BFAIR :abbr:`MFA (metabolic flux analysis)` tools use the software
:abbr:`INCA (Isotopomer Network Compartmental Analysis)` in MATLAB and
subsequently re-import its output before processing the data. To make
full use of these tools you will have to have both INCA and MATLAB
installed on your system.

INCA
^^^^

"INCA (Isotopomer Network Compartmental Analysis) is a MATLAB-based
software package for isotopomer network modeling and metabolic flux
analysis." You can read more about it in
`Young, 2014 <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3998137/pdf/btu015.pdf>`_
You have to get a free academic licence for INCA from
`the Vanderbilt University website <http://mfa.vueinnovations.com/licensing>`_
(the second option is the relevant one) and install it. Note the path to the base
directory of your INCA installation, you will need it later.

MATLAB
^^^^^^

Get a free academic licence and install MATLAB from the
`mathworks website <https://www.mathworks.com>`_. Then, install the engine API following
the guide provided
`under this link <https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html>`_.
In short, you will have to go to your MATLAB root folder (find your
installation and open that folder) and, in the command line, go to

.. code-block::

    >>> cd /extern/engines/python

and run

.. code-block::

    >>> python setup.py install

That should do the trick.

Modules
-------

.. currentmodule:: BFAIR.INCA.INCA_script_generator

.. autodata:: script_generator_descr
   :annotation:

.. currentmodule:: BFAIR.INCA.INCA_reimport

.. autodata:: reimport_descr
   :annotation:

.. currentmodule:: BFAIR.INCA

INCA script generation
----------------------

The MATLAB scripts for INCA can be automatically generated with the right input.
To do that, we need to limit the input to only the information that will actually
be used for the analysis.

Data pre-processing
^^^^^^^^^^^^^^^^^^^

If you have large dataframes that include multiple experiments
that should be used in separate analyses or information about multiple models, you
reduce them using these functions.

.. autosummary::
   :toctree: generated/

    INCA_script.limit_to_one_model
    INCA_script.limit_to_one_experiment

Step-wise generation
^^^^^^^^^^^^^^^^^^^^

Once the input is ready, INCA script can be generated. This can be done either
step-wise or all at once. Here are the functions for the sequential construction.
See below for the short-cut.

.. autosummary::
   :toctree: generated/

    INCA_script.initiate_MATLAB_script
    INCA_script.add_reactions_to_script
    INCA_script.initialize_model
    INCA_script.symmetrical_metabolites
    INCA_script.unbalanced_reactions
    INCA_script.add_reaction_parameters
    INCA_script.verify_and_estimate
    INCA_script.add_experimental_parameters
    INCA_script.mapping

Summary function
^^^^^^^^^^^^^^^^

Both the ``INCA_script`` and the ``INCA_reimport`` module have summarizing functions
that run large parts of the workflows if the correct input is provided. The input
script can be generated using the ``INCA_script.script_generator`` summary function.

.. autosummary::
   :toctree: generated/

    INCA_script.script_generator

Runner script generation
^^^^^^^^^^^^^^^^^^^^^^^^

The analysis functions are kept saparate from the metabolic model and the experimental
data used in INCA. The runner script, containing these analysis functions, is created
using the following functions.

.. autosummary::
   :toctree: generated/

    INCA_script.runner_script_generator

Save the scripts
^^^^^^^^^^^^^^^^

Until now, our scripts are just large strings. These functions save them as ``.m``
MATLAB scripts.

.. autosummary::
   :toctree: generated/

    INCA_script.save_INCA_script
    INCA_script.save_runner_script

INCA execution
--------------

If the MATLAB engine is activated (see top), then the INCA script can be run in MATLAB from python,
i.e. directly from e.g. a Jupyter Notebook.

MATLAB engine execution function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated/

    INCA_script.run_INCA_in_MATLAB

INCA output re-import
---------------------

After INCA was successfully run, the results will be saved in a ``.mat`` file. The results
will have to be parsed in order to use them in python again. This is done with the ``INCA_reimport``
module.

Step-wise re-import
^^^^^^^^^^^^^^^^^^^

You can execute everything all at once (check the summary function below) or one by one,
as described here.

.. autosummary::
   :toctree: generated/

    INCA_reimport.INCA_reimport.extract_file_info
    INCA_reimport.INCA_reimport.det_simulation_type
    INCA_reimport.INCA_reimport.data_extraction
    INCA_reimport.INCA_reimport.extract_model_info
    INCA_reimport.INCA_reimport.extract_sim_params
    INCA_reimport.INCA_reimport.extract_base_stats
    INCA_reimport.INCA_reimport.get_fit_info
    INCA_reimport.INCA_reimport.sort_fit_info
    INCA_reimport.INCA_reimport.get_residuals_info
    INCA_reimport.INCA_reimport.sort_residual_info
    INCA_reimport.INCA_reimport.get_fitted_parameters
    INCA_reimport.INCA_reimport.sort_parameter_info

Summary function
^^^^^^^^^^^^^^^^

The output can also be re-imported using the ``INCA_reimport.reimport`` summary function.

.. autosummary::
   :toctree: generated/

    INCA_reimport.INCA_reimport.reimport
