MFA sampling
============

.. currentmodule:: incawrapper.mfa.sampling

Tools were set up to facilitate the analysis of the fluxes calculated in a metabolic flux analysis. Some tools that can help adapting naming conventions if different models were used and identifying exchange fluxes, i.e. fluxes with non-overlapping forward- and reverse reactions, are presented first, followed by methods to add the MFA-calculated fluxes as constraints to a COBRA model and how to deal with infeasible solutions.

Compatibility
-------------

If a different model was used for the MFA than for the subsequent analysis (e.g. a reduced model rather than a genome scale model), issues with the naming conventions might arise. Here, some functions that help with consolidating these models are provided.

Functions
^^^^^^^^^

.. autosummary::
   :toctree: generated/

    model_rxn_overlap
    rxn_coverage
    split_lumped_rxns
    split_lumped_reverse_rxns
    find_reverse_rxns
    combine_split_rxns
    cobra_add_split_rxns
    find_biomass_reaction
    get_min_solution_val
    replace_biomass_rxn_name


Sampling
--------

Methods are provided to apply the MFA-calculated fluxes as constraints to the model that is used for further analyses and to deal with infeasible solutions.

Functions
^^^^^^^^^

.. autosummary::
   :toctree: generated/
   
    add_constraints
    add_feasible_constraints
    bound_relaxation
