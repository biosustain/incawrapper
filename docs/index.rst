Welcome to incawrapper's documentation!
=======================================

incawrapper is a Python package which wraps for the matlab application INCA. INCA is a tool for
13C metabolic flux analysis [1,2]. The incawrapper package allows to import data,
setup the model and run INCA all from within Python. The results can be exported
back to Python for further analysis and simply saved as .csv files. Furthermore, it is possible to 
export results from INCA runs entirely done through the GUI to Python.

.. toctree::
   :numbered: 3
   :maxdepth: 1

   install
   examples/Quick_start
   examples/Data input
   examples/multiple_experiments
   incawrapper_and_the_incagui
   examples/index
   developer/index


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


References
----------
[1] Young, Jamey D. “INCA: A Computational Platform for Isotopically Non-Stationary Metabolic Flux Analysis.” Bioinformatics 30, no. 9 (May 1, 2014): 1333–35. https://doi.org/10.1093/bioinformatics/btu015.

[2] Rahim, Mohsin, Mukundan Ragavan, Stanislaw Deja, Matthew E. Merritt, Shawn C. Burgess, and Jamey D. Young. “INCA 2.0: A Tool for Integrated, Dynamic Modeling of NMR- and MS-Based Isotopomer Measurements and Rigorous Metabolic Flux Analysis.” Metabolic Engineering 69 (January 2022): 275–85. https://doi.org/10.1016/j.ymben.2021.12.009.

