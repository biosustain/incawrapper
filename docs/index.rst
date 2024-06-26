Welcome to INCAWrapper's documentation!
=======================================

INCAWrapper is a Python package which wraps around the matlab application INCA. INCA is a tool for
13C metabolic flux analysis [1,2]. The INCAWrapper package allows to import data,
setup the model and run INCA all from within Python. The results can be exported
back to Python for further analysis and simply saved as .csv files. Furthermore, it is possible to 
export results from INCA runs entirely done through the GUI to Python.

The INCAWrapper code is freely available under an MIT License. However, to run INCA, you need a MATLAB and INCA licenses. Additionally, methods using COBRA tools need a GUROBI license. An INCA license is free for non-commercial use at `mfa.vueinnovations.com <mfa.vueinnovations.com>`_ and GUROBI offers free academic licenses at `gurobi.com <gurobi.com>`_. For more installation, please check our pre-requisites and installation guide.

What can the INCAWrapper do for me?
-----------------------------------
* Provide a Python interface to use INCA 100% independent of the INCA GUI
* Provide a data structure that can be imported to INCA
* Provide methods for exporting results from INCA to Python
* Provide methods for plotting results from INCA in Python
* Provide methods for creating INCA models with data, which can then be used in the INCA GUI
* Run both Isotopically Non-Stationary (INST) and Isotopically Stationary (IS) 13C-MFA
* Estimate fluxes and confidence intervals through the following INCA algorithms: estimate, parameter continuation, and Monte Carlo sampling

What can the INCAWrapper NOT do for me?
---------------------------------------
* Integration of NMR data
* Simulation of experiments 
* Optimization of experimental design


Overview of the documentation
-----------------------------
.. toctree::
   :numbered: 3
   :maxdepth: 1

   install
   quick_start
   input_data
   multiple_experiments
   monte_carlo_sampling
   incawrapper_and_the_incagui
   options
   Low_level_api
   examples/index
   developer/index
   API </autoapi/incawrapper/index.rst> 


References
----------
[1] Young, Jamey D. “INCA: A Computational Platform for Isotopically Non-Stationary Metabolic Flux Analysis.” Bioinformatics 30, no. 9 (May 1, 2014): 1333–35. https://doi.org/10.1093/bioinformatics/btu015.

[2] Rahim, Mohsin, Mukundan Ragavan, Stanislaw Deja, Matthew E. Merritt, Shawn C. Burgess, and Jamey D. Young. “INCA 2.0: A Tool for Integrated, Dynamic Modeling of NMR- and MS-Based Isotopomer Measurements and Rigorous Metabolic Flux Analysis.” Metabolic Engineering 69 (January 2022): 275–85. https://doi.org/10.1016/j.ymben.2021.12.009.



Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

