# -*- coding: utf-8 -*-
"""Main module."""

# Libraries

import pandas as pd
import numpy as np
import time
import ast
import sys

try:
    import matlab.engine
except ModuleNotFoundError:
    print(
        "Please check the README for a guide on how to install the MATLAB \
            engine"
    )

__version__ = "0.0.1"


class INCA_script:
    def __init__(self):
        """
        Class of functions to set up a MATLAB script for MFA using
        INCA and for interaction with MATLAB itself. Will later on
        also re-import data from .mat file.
        """

    def limit_to_one_model(self, data_input, model_name_column, model_name):
        """
        Limits the data to values that are assigned to one metabolic model

        Parameters:
            data_input: Input data file that needs to be processed
            model_name_column: Column name where model names are defined
            model_name: Name of the model the data will be limited to

        Returns:
            data_input: Limited data

        """
        data_output = pd.DataFrame()
        for i, row in data_input.iterrows():
            if row[model_name_column] == model_name:
                if len(data_output) == 0:
                    data_output = pd.DataFrame.transpose(row.to_frame())
                else:
                    data_output = data_output.append(
                        pd.DataFrame.transpose(row.to_frame())
                    )
        data_input = data_output
        return data_input

    def limit_to_one_experiment(
        self, data_input, experiment_name_column, experiment_name
    ):
        """
        Limits the data to values that were acquired in one experiment

        Parameters:
            data_input: Input data file that needs to be processed
            experiment_name_column: Column name where experiment names
                are defined
            model_name: Name of the model the data will be limited to

        Returns:
            data_input: Limited data

        """
        data_output = pd.DataFrame()
        for i, row in data_input.iterrows():
            if row[experiment_name_column] == experiment_name:
                if len(data_output) == 0:
                    data_output = pd.DataFrame.transpose(row.to_frame())
                else:
                    data_output = data_output.append(
                        pd.DataFrame.transpose(row.to_frame())
                    )
        data_input = data_output
        return data_input

    def prepare_input(
        self, string, type_of_replacement=["Curly", "Double_square"]
    ):
        """
        Process data that is stored in strings of lists etc in the files

        Parameters:
            string: Processes the data in cells in the dataframes.
                The info is either bordered by curly or double square
                brackets.
            type_of_replacement: Define the type of surrounding brackets

        Returns:
            string: returns data in lists without bordering brackets

        """
        if type_of_replacement == "Curly":
            string = string.strip("}{").split(",")
        elif type_of_replacement == "Double_square":
            string = string[1:-1]
            string = ast.literal_eval(string)
        return string

    def initiate_MATLAB_script(self):
        """
        Starts writing the MATLAB script

        Returns:
            mat_script: Initialized MATLAB script

        """
        mat_script = "clear functions\n\n"

        return mat_script

    def reaction_mapping(
        self,
        atomMapping_molecules_ids,
        model_molecules_ids,
        atomMapping_molecules_stoichiometry,
        atomMapping_molecules_elements,
        atomMapping_molecules_mapping,
        model_molecules_stoichiometry,
        reaction_type="reactant",
    ):
        """
        Provides the carbon mapping for metabolites in a model.
        Called within "add_reactions_to_script()"

        Parameters:
            atomMapping_molecules_ids: processed atomMappingReactions_data_I
                reactants_ids_tracked or products_ids_tracked
            model_molecules_ids: processed modelReaction_data_I
                reactants_ids or products_ids
            atomMapping_molecules_stoichiometry: processed
                atomMappingReactions_data_I
                reactants_stoichiometry_tracked or
                productss_stoichiometry_tracked
            atomMapping_molecules_elements: processed
                atomMappingReactions_data_I
                reactants_elements_tracked or products_elements_tracked
            atomMapping_molecules_mapping: processed
                atomMappingReactions_data_I
                reactants_mapping or products_mapping
            model_molecules_stoichiometry: processed modelReaction_data_I
                reactants_stoichiometry or products_stoichiometry
            reaction_type: reactant or product

        Returns:
            rxn_equation: Reaction equation for the defined reaction

        """
        rxn_equation = ""
        if reaction_type == "product":
            rxn_equation += " -> "
        # This had to be added because some metabolites appear more than once
        # in one reaction with different mappings
        seen_molecule = {}
        dupes_molecule = []
        if not len(atomMapping_molecules_ids) == len(
            set(atomMapping_molecules_ids)
        ):
            for x in atomMapping_molecules_ids:
                if x not in seen_molecule:
                    seen_molecule[x] = 1
                else:
                    if seen_molecule[x] == 1:
                        dupes_molecule.append(x)
                    seen_molecule[x] += 1

        # Iterate through the metabolites involved in the reactions
        for molecule_cnt, molecule in enumerate(model_molecules_ids):
            # Indices for metabolites with multiple different mappings
            # are being sought
            # initiate boolean for "while" loop
            duplicates_not_done = True
            duplicates_counter = 0
            while duplicates_not_done:
                # this little bit adds +s if it's not the first molecule
                if molecule_cnt > 0:
                    rxn_equation += " + "
                if molecule in atomMapping_molecules_ids:
                    if molecule in dupes_molecule:
                        positions = [
                            i
                            for i, x in enumerate(atomMapping_molecules_ids)
                            if x == molecule
                        ]
                        molecule_index = positions[duplicates_counter]
                        if duplicates_counter == len(positions) - 1:
                            duplicates_not_done = False
                        duplicates_counter += 1
                    else:
                        molecule_index = atomMapping_molecules_ids.index(
                            molecule
                        )
                        duplicates_not_done = False

                    # here we check if it is a tuple, i.e. there is more than
                    # one metabolite, or a list, i.e. only one metabolite
                    rxn_equation += (
                        str(
                            atomMapping_molecules_stoichiometry[molecule_index]
                        )
                        + "*"
                        + molecule
                        + " ("
                    )
                    if type(atomMapping_molecules_elements) is tuple:
                        # here we go through the mapping, enumerate the atoms
                        # and add the corresponding mapping
                        for mapping_cnt, mapping in enumerate(
                            atomMapping_molecules_elements[molecule_index]
                        ):
                            # to remove the final whitespace
                            if (mapping_cnt + 1) == len(
                                atomMapping_molecules_mapping[molecule_index]
                            ):
                                rxn_equation += (
                                    mapping
                                    + str(mapping_cnt + 1)
                                    + ":"
                                    + atomMapping_molecules_mapping[
                                        molecule_index
                                    ][mapping_cnt]
                                )
                            else:
                                rxn_equation += (
                                    mapping
                                    + str(mapping_cnt + 1)
                                    + ":"
                                    + atomMapping_molecules_mapping[
                                        molecule_index
                                    ][mapping_cnt]
                                    + " "
                                )
                    elif type(atomMapping_molecules_elements) is list:
                        for mapping_cnt, mapping in enumerate(
                            atomMapping_molecules_elements
                        ):
                            # to remove the final whitespace
                            if (mapping_cnt + 1) == len(
                                atomMapping_molecules_mapping[0]
                            ):
                                rxn_equation += (
                                    mapping
                                    + str(mapping_cnt + 1)
                                    + ":"
                                    + atomMapping_molecules_mapping[0][
                                        mapping_cnt
                                    ]
                                )
                            else:
                                rxn_equation += (
                                    mapping
                                    + str(mapping_cnt + 1)
                                    + ":"
                                    + atomMapping_molecules_mapping[0][
                                        mapping_cnt
                                    ]
                                    + " "
                                )
                    # close the brackets for mapping
                    rxn_equation += ")"

                # Exceptions that are in the model but not
                # tracked are added here
                else:
                    rxn_equation += (
                        str(model_molecules_stoichiometry[molecule_cnt])
                        + "*"
                        + molecule
                    )
                    duplicates_not_done = False

        return rxn_equation

    def add_reactions_to_script(
        self, modelReaction_data_I, atomMappingReactions_data_I
    ):
        """
        Translates the model and adds mapping using reaction_mapping()

        Parameters:
            modelReaction_data_I: pre-processed modelReaction_data_I input data
            atomMappingReactions_data_I: pre-processed
                atomMappingReactions_data_I input data

        Returns:
            mat_script: Extention to the MATLAB script under construction
            model_rxn_ids_exp: List of reaction IDs used for the model

        """
        if len(atomMappingReactions_data_I["rxn_id"]) != len(
            atomMappingReactions_data_I["rxn_id"].unique()
        ):
            sys.exit(
                "There is a duplicate reaction in atomMappingReactions_data_I"
            )
        mat_script = "r = reaction({... % define reactions\n"

        model_rxn_ids = []
        model_rxn_ids_exp = []
        # First we go through the reactions in the model to make sure that
        # we only include the ones that are actually there
        for cnt, modelReaction_data in modelReaction_data_I.iterrows():
            if modelReaction_data["used_"]:
                model_rxn_id = modelReaction_data["rxn_id"]
                model_rxn_ids.append(model_rxn_id)
        model_rxn_ids = sorted(model_rxn_ids, key=str.lower)
        for id_cnt, model_rxn_id in enumerate(model_rxn_ids):
            for cnt, modelReaction_data in modelReaction_data_I.iterrows():

                # Model
                index_in_model = list(modelReaction_data_I["rxn_id"]).index(
                    modelReaction_data["rxn_id"]
                )
                model_reactants_stoichiometry = self.prepare_input(
                    modelReaction_data_I.iloc[index_in_model].loc[
                        "reactants_stoichiometry"
                    ],
                    "Curly",
                )
                model_products_stoichiometry = self.prepare_input(
                    modelReaction_data_I.iloc[index_in_model].loc[
                        "products_stoichiometry"
                    ],
                    "Curly",
                )

                if modelReaction_data["rxn_id"] == model_rxn_id:

                    rxn_equation = "'"

                    # we save the location of the row corresponding to
                    # this reaction in the other file
                    # "prepare_input" is a helper function to make the
                    # entries useable, this will have to be checked with
                    # other input

                    # Atom Mapping
                    index_in_atomMapping = list(
                        atomMappingReactions_data_I["rxn_id"]
                    ).index(modelReaction_data["rxn_id"])
                    atomMapping_reactants_stoichiometry = self.prepare_input(
                        atomMappingReactions_data_I.iloc[
                            index_in_atomMapping
                        ].loc["reactants_stoichiometry_tracked"],
                        "Curly",
                    )
                    atomMapping_products_stoichiometry = self.prepare_input(
                        atomMappingReactions_data_I.iloc[
                            index_in_atomMapping
                        ].loc["products_stoichiometry_tracked"],
                        "Curly",
                    )

                    # this step makes sure that we exclude reactions that
                    # do not have any stoichiometry annotated
                    if (
                        atomMapping_reactants_stoichiometry[0] == ""
                        and atomMapping_products_stoichiometry[0] == ""
                    ):
                        print(
                            "There is no stoichimetriy given for:",
                            model_rxn_id,
                        )
                        # Model
                        model_reactants_ids = self.prepare_input(
                            modelReaction_data_I.iloc[index_in_model].loc[
                                "reactants_ids"
                            ],
                            "Curly",
                        )
                        model_products_ids = self.prepare_input(
                            modelReaction_data_I.iloc[index_in_model].loc[
                                "products_ids"
                            ],
                            "Curly",
                        )
                        model_reactants_stoichiometry = [
                            float(i) * -1
                            for i in model_reactants_stoichiometry
                        ]
                        model_products_stoichiometry = [
                            float(i) for i in model_products_stoichiometry
                        ]

                        for reactant_cnt, reactant in enumerate(
                            model_reactants_ids
                        ):
                            # this little bit adds +s if it's not
                            # the first reactant
                            if reactant_cnt > 0:
                                rxn_equation += " + "
                            rxn_equation += (
                                str(
                                    model_reactants_stoichiometry[reactant_cnt]
                                )
                                + "*"
                                + reactant
                            )
                        rxn_equation += " -> "
                        for product_cnt, product in enumerate(
                            model_products_ids
                        ):
                            # this little bit adds +s if it's not
                            # the first product
                            if product_cnt > 0:
                                rxn_equation += " + "
                            rxn_equation += (
                                str(model_products_stoichiometry[product_cnt])
                                + "*"
                                + product
                            )
                    else:
                        # process the remaining info about the metabolites.
                        # Done here because it can throw an error if
                        # anything is empty

                        # Atom Mapping
                        atomMapping_reactants_ids = self.prepare_input(
                            atomMappingReactions_data_I.iloc[
                                index_in_atomMapping
                            ].loc["reactants_ids_tracked"],
                            "Curly",
                        )
                        atomMapping_products_ids = self.prepare_input(
                            atomMappingReactions_data_I.iloc[
                                index_in_atomMapping
                            ].loc["products_ids_tracked"],
                            "Curly",
                        )
                        atomMapping_reactants_elements = self.prepare_input(
                            atomMappingReactions_data_I.iloc[
                                index_in_atomMapping
                            ].loc["reactants_elements_tracked"],
                            "Double_square",
                        )
                        atomMapping_products_elements = self.prepare_input(
                            atomMappingReactions_data_I.iloc[
                                index_in_atomMapping
                            ].loc["products_elements_tracked"],
                            "Double_square",
                        )
                        atomMapping_reactants_mapping = self.prepare_input(
                            atomMappingReactions_data_I.iloc[
                                index_in_atomMapping
                            ].loc["reactants_mapping"],
                            "Curly",
                        )
                        atomMapping_products_mapping = self.prepare_input(
                            atomMappingReactions_data_I.iloc[
                                index_in_atomMapping
                            ].loc["products_mapping"],
                            "Curly",
                        )
                        atomMapping_reactants_stoichiometry = [
                            float(i) * -1
                            for i in atomMapping_reactants_stoichiometry
                        ]
                        atomMapping_products_stoichiometry = [
                            float(i)
                            for i in atomMapping_products_stoichiometry
                        ]

                        # Model
                        model_reactants_ids = self.prepare_input(
                            modelReaction_data_I.iloc[index_in_model].loc[
                                "reactants_ids"
                            ],
                            "Curly",
                        )
                        model_products_ids = self.prepare_input(
                            modelReaction_data_I.iloc[index_in_model].loc[
                                "products_ids"
                            ],
                            "Curly",
                        )
                        model_reactants_stoichiometry = [
                            float(i) * -1
                            for i in model_reactants_stoichiometry
                        ]
                        model_products_stoichiometry = [
                            float(i) for i in model_products_stoichiometry
                        ]

                        rxn_equation = "'"
                        # We go through the IDs to treat each
                        # metabolite separately
                        reactant_equation = self.reaction_mapping(
                            atomMapping_reactants_ids,
                            model_reactants_ids,
                            atomMapping_reactants_stoichiometry,
                            atomMapping_reactants_elements,
                            atomMapping_reactants_mapping,
                            model_reactants_stoichiometry,
                            reaction_type="reactant",
                        )
                        product_equation = self.reaction_mapping(
                            atomMapping_products_ids,
                            model_products_ids,
                            atomMapping_products_stoichiometry,
                            atomMapping_products_elements,
                            atomMapping_products_mapping,
                            model_products_stoichiometry,
                            reaction_type="product",
                        )
                        rxn_equation = (
                            rxn_equation + reactant_equation + product_equation
                        )
            # the ids of the equations are being added to the list that
            # will be exported
            model_rxn_ids_exp.append(model_rxn_id)
            mat_script += rxn_equation + " ';...\n"
        mat_script += "});\n\n"

        return mat_script, model_rxn_ids_exp

    def initialize_model(self):
        """
        Previously described reactions are assigned to a model object

        Returns:
            mat_script: addition to MATLAB script under construction

        """
        mat_script = "m = model(r); % set up model\n\n"

        return mat_script

    def symmetrical_metabolites(self, atomMappingMetabolite_data_I):
        """
        Takes care of symmetrical metabolites if not done so in the
        reaction equations

        Parameters:
            atomMappingMetabolite_data_I: pre-processed
                atomMappingMetabolite_data_I input data

        Returns:
            mat_script: addition to MATLAB script under construction

        """
        tmp_script = "% take care of symmetrical metabolites\n"
        for cnt_met, met in atomMappingMetabolite_data_I.iterrows():
            if not pd.isna(met["met_symmetry_atompositions"]):
                tmp_script = (
                    tmp_script
                    + "m.mets{'"
                    + met["met_id"]
                    + "'}.sym = list('rotate180', atommap('"
                )
                met_positions = [
                    int(x)
                    for x in self.prepare_input(met["met_atompositions"],
                                                "Curly")
                ]
                met_elements = self.prepare_input(met["met_elements"], "Curly")
                met["met_symmetry_elements"] = met[
                    "met_symmetry_elements"
                ].replace("{}", str(np.nan))
                met_symmetry_elements = self.prepare_input(
                    met["met_symmetry_elements"], "Curly"
                )
                met["met_symmetry_atompositions"] = met[
                    "met_symmetry_atompositions"
                ].replace("{}", str(np.nan))
                met_symmetry_atompositions = [
                    int(x)
                    for x in self.prepare_input(
                        met["met_symmetry_atompositions"], "Curly"
                    )
                ]

                for cnt, atompositions in enumerate(met_positions):
                    tmp_script = (
                        tmp_script
                        + met_elements[cnt]
                        + str(atompositions + 1)
                        + ":"
                        + met_symmetry_elements[cnt]
                        + str(met_symmetry_atompositions[cnt] + 1)
                        + " "
                    )
                tmp_script = tmp_script[:-1]
                tmp_script = tmp_script + "'));\n"
            else:
                continue
        tmp_script = tmp_script + "\n"
        mat_script = tmp_script

        return mat_script

    # NOTE: hard-coded for now until a better workaround can be done
    def unbalanced_reactions(
        self,
        atomMappingMetabolite_data_I,
        unbalanced_metabolites=["co2_e", "h2o_e", "h_e", "na1_e"],
    ):
        """
        Adds in the metabolite state (balanced or unbalanced)

        Parameters:
            atomMappingMetabolite_data_I: pre-processed
                atomMappingMetabolite_data_I input data
            unbalanced_metabolites: list of unbalanced
                metabolites - hardcoded

        Returns:
            mat_script: addition to MATLAB script under construction

        """
        tmp_script = "% define unbalanced reactions\n"
        # specify reactions that should be forcible unbalanced
        metabolites_all = [
            x["met_id"] for cnt, x in atomMappingMetabolite_data_I.iterrows()
        ]
        # unbalanced reactions:
        for met in unbalanced_metabolites:
            if met in metabolites_all:
                tmp_script = (
                    tmp_script
                    + "m.states{'"
                    + met
                    + ".EX"
                    + "'}.bal = false;\n"
                )
        mat_script = tmp_script

        return mat_script

    # Stedv stuff should be checked once more before merging to main
    def add_reaction_parameters(
        self,
        modelReaction_data_I,
        measuredFluxes_data_I,
        model_rxn_ids,
        fluxes_present=True,
    ):
        """
        Flux parameters are added. They correspond to the previously
        described reactions

        Parameters:
            modelReaction_data_I: pre-processed
                modelReaction_data_I input data
            measuredFluxes_data_I: pre-processed
                measuredFluxes_data_I input data
            model_rxn_ids: pre-processed
                model_rxn_ids input data
            fluxes_present: confirm if fluxes are present. If not then the
                flux measuredFluxes_data_I file will be ignored

        Returns:
            mat_script: addition to MATLAB script under construction

        """
        # Add in initial fluxes (lb/ub, values, on/off) and define the
        # reaction ids
        # NOTE: lb, ub, val = 0 for steady-state
        # lower bounds
        tmp_script_lb = "\n% define lower bounds\nm.rates.flx.lb = [...\n"
        # upper bounds
        tmp_script_ub = "\n%define upper bounds\nm.rates.flx.ub = [...\n"
        # intial flux values
        tmp_script_val = "\n% define flux vals\nm.rates.flx.val = [...\n"
        # include/exclude a reaction from the simulation
        tmp_script_on = "\n% include/exclude reactions\nm.rates.on = [...\n"
        # rxn_ids
        tmp_script_id = "\n% define reaction ids\nm.rates.id = {...\n"
        for model_rxn_id in model_rxn_ids:
            for rxn_cnt, rxn in modelReaction_data_I.iterrows():
                if rxn["rxn_id"] == model_rxn_id and rxn["used_"]:
                    if fluxes_present:
                        if rxn["rxn_id"] in list(
                            measuredFluxes_data_I["rxn_id"]
                        ):
                            for (
                                flux_cnt,
                                flux,
                            ) in measuredFluxes_data_I.iterrows():
                                if rxn["rxn_id"] == flux["rxn_id"]:
                                    tmp_script_lb = (
                                        tmp_script_lb
                                        + str(flux["flux_lb"])
                                        + ",...\n"
                                    )
                                    tmp_script_ub = (
                                        tmp_script_ub
                                        + str(flux["flux_ub"])
                                        + ",...\n"
                                    )
                                    tmp_script_val = (
                                        tmp_script_val
                                        + str(flux["flux_average"])
                                        + ",...\n"
                                    )
                        else:
                            tmp_script_lb = (
                                tmp_script_lb
                                + str(rxn["lower_bound"])
                                + ",...\n"
                            )
                            tmp_script_ub = (
                                tmp_script_ub
                                + str(rxn["upper_bound"])
                                + ",...\n"
                            )
                            tmp_script_val = tmp_script_val + str(0) + ",...\n"
                    else:
                        tmp_script_lb = (
                            tmp_script_lb + str(rxn["lower_bound"]) + ",...\n"
                        )
                        tmp_script_ub = (
                            tmp_script_ub + str(rxn["upper_bound"]) + ",...\n"
                        )
                    if rxn["upper_bound"] == 0.0 and rxn["lower_bound"] == 0.0:
                        tmp_script_on = tmp_script_on + "false" + ",...\n"
                    else:
                        tmp_script_on = tmp_script_on + "true" + ",...\n"
                    tmp_script_id = (
                        tmp_script_id + "'" + rxn["rxn_id"] + "',...\n"
                    )
        tmp_script_lb = tmp_script_lb + "];\n"
        tmp_script_ub = tmp_script_ub + "];\n"
        tmp_script_val = tmp_script_val + "];\n"
        tmp_script_on = tmp_script_on + "];\n"
        tmp_script_id = tmp_script_id + "};\n"

        mat_script = (
            tmp_script_lb
            + tmp_script_ub
            + tmp_script_val
            + tmp_script_on
            + tmp_script_id
        )
        return mat_script

    def verify_and_estimate(self):
        """
        Adds a QC step and defines the restarts for later processing

        Returns:
            mat_script: addition to MATLAB script under construction

        """
        mat_script = "\nm.rates.flx.val = mod2stoich(m); % make sure the fluxes are feasible\n"  # noqa E501
        mat_script = (
            mat_script
            + "m.options.fit_starts = 10; % 10 restarts during the estimation procedure\n"  # noqa E501
        )

        return mat_script

    def add_experimental_parameters(
        self,
        experimentalMS_data_I,
        tracer_I,
        measuredFluxes_data_I,
        atomMappingMetabolite_data_I,
    ):
        """
        Defines the measured fragments and adds tracer information

        Parameters:
            experimentalMS_data_I: pre-processed
                experimentalMS_data_I input data
            tracer_I: pre-processed
                tracer_I input data
            measuredFluxes_data_I: pre-processed
                measuredFluxes_data_I input data
            atomMappingMetabolite_data_I: pre-processed
                atomMappingMetabolite_data_I input data

        Returns:
            mat_script: addition to MATLAB script under construction
            fragments_used: List of the fragments in the data that fit into
                the defined parameters

        """
        mat_script = ""

        fragments_used = []

        experiments_all = [
            x["experiment_id"] for cnt, x in experimentalMS_data_I.iterrows()
        ]
        experiments = list(set(experiments_all))
        experiments.sort()

        fragments_all = [
            x["fragment_id"] for cnt, x in experimentalMS_data_I.iterrows()
        ]
        fragments = list(set(fragments_all))
        fragments.sort()

        for experiment_cnt, experiment in enumerate(experiments):
            tmp_script = "\n% define which fragments of molecules were measured in which experiment\nd = msdata({...\n"  # noqa E501
            for frg_cnt, fragment in enumerate(fragments):
                for ms_cnt, ms_data in experimentalMS_data_I.iterrows():
                    if (
                        ms_data["fragment_id"] == fragment
                        and ms_data["experiment_id"] == experiment
                    ):
                        met_positions = [
                            int(x)
                            for x in self.prepare_input(
                                ms_data["met_atompositions"], "Curly"
                            )
                        ]
                        atomMapping_atompositions_row = (
                            atomMappingMetabolite_data_I[
                                atomMappingMetabolite_data_I["met_id"]
                                == ms_data["met_id"]
                            ]
                        )
                        if (
                            len(
                                list(
                                    atomMapping_atompositions_row[
                                        "met_atompositions"
                                    ]
                                )
                            )
                            > 0
                        ):
                            atomMapping_atompositions = [
                                int(x)
                                for x in self.prepare_input(
                                    list(
                                        atomMapping_atompositions_row[
                                            "met_atompositions"
                                        ]
                                    )[0],
                                    "Curly",
                                )
                            ]
                            if max(met_positions) <= max(
                                atomMapping_atompositions
                            ):
                                fragments_used.append(ms_data["fragment_id"])
                                tmp_script = (
                                    tmp_script
                                    + "'"
                                    + ms_data["fragment_id"]
                                    + ": "
                                    + ms_data["met_id"]
                                    + " @ "
                                )
                                met_elements = self.prepare_input(
                                    ms_data["met_elements"], "Curly"
                                )
                                for pos_cnt, pos in enumerate(met_positions):
                                    tmp_script = (
                                        tmp_script
                                        + met_elements[pos_cnt]
                                        + str(pos + 1)
                                        + " "
                                    )
                                tmp_script = tmp_script[:-1]
                                tmp_script = tmp_script + "';\n"
                                break
                        else:
                            break
            tmp_script = tmp_script + "});\n"
            tmp_script = (
                tmp_script
                + "\n% initialize mass distribution vector\nd.mdvs = mdv;\n"
            )
            mat_script = mat_script + tmp_script

            # write substrate labeling (i.e. tracer) information
            tmp_script = ""
            tmp_script = (
                tmp_script
                + "\n% define tracers used in the experiments\nt = tracer({...\n"  # noqa E501
            )
            for tracer_cnt, tracer in tracer_I.iterrows():
                if tracer["experiment_id"] == experiment:
                    tmp_script = (
                        tmp_script
                        + "'"
                        + tracer["met_name"]
                        + ": "
                        + tracer["met_id"]
                        + ".EX"
                        + " @ "
                    )
                    tracer_met_atompositions = self.prepare_input(
                        tracer["met_atompositions"], "Curly"
                    )
                    tracer_met_elements = self.prepare_input(
                        tracer["met_elements"], "Curly"
                    )
                    for cnt, met_atompositions in enumerate(
                        tracer_met_atompositions
                    ):
                        tmp_script = (
                            tmp_script
                            + tracer_met_elements[cnt]
                            + str(met_atompositions)
                            + " "
                        )
                    # remove extra whitespace
                    tmp_script = tmp_script[:-1]
                    tmp_script = tmp_script + "';...\n"
            tmp_script = tmp_script + "});\n"
            tmp_script = (
                tmp_script
                + "\n% define fractions of tracers used\nt.frac = [ "
            )
            for tracer_cnt, tracer in tracer_I.iterrows():
                if tracer["experiment_id"] == experiment:
                    tmp_script = tmp_script + str(tracer["ratio"]) + ","
            # remove extra comma
            tmp_script = tmp_script[:-1]
            tmp_script = tmp_script + " ];\n"
            mat_script = mat_script + tmp_script

            # write flux measurements
            tmp_script = ""
            tmp_script = (
                tmp_script + "\n% define experiments for fit data\nf = data(' "
            )
            for flux_cnt, flux in measuredFluxes_data_I.iterrows():
                if flux["experiment_id"] == experiment:
                    tmp_script = tmp_script + flux["rxn_id"] + " "
            tmp_script = tmp_script[:-1]
            tmp_script = tmp_script + " ');\n"
            tmp_script = tmp_script + "\n% add fit values\nf.val = [...\n"
            for flux_cnt, flux in measuredFluxes_data_I.iterrows():
                if flux["experiment_id"] == experiment:
                    tmp_script = (
                        tmp_script + str(flux["flux_average"]) + ",...\n"
                    )
            tmp_script = tmp_script + "];\n"
            tmp_script = tmp_script + "% add fit stds\nf.std = [...\n"
            for flux_cnt, flux in measuredFluxes_data_I.iterrows():
                if flux["experiment_id"] == experiment:
                    tmp_script = (
                        tmp_script + str(flux["flux_stdev"]) + ",...\n"
                    )
            tmp_script = tmp_script + "];\n"
            tmp_script = (
                tmp_script
                + "\n% initialize experiment with t and add f and d\nx = experiment(t);\n"  # noqa E501
            )
            tmp_script = tmp_script + "x.data_flx = f;\n"
            tmp_script = tmp_script + "x.data_ms = d;\n"
            tmp_script = (
                tmp_script
                + "\n% assing all the previous values to a specific experiment"
            )
            tmp_script = tmp_script + "\nm.expts(%d) = x;\n" % (
                experiment_cnt + 1
            )

            mat_script = mat_script + tmp_script
        return mat_script, fragments_used

    # check the stedv stuff before merging to main
    def mapping(self, experimentalMS_data_I, fragments_used):
        """
        Adds MS data to measured fragments

        Parameters:
            experimentalMS_data_I: pre-processed
                experimentalMS_data_I input data
            fragments_used: List of the fragments in the data that fit into
                the defined parameters from "add_experimental_parameters()"

        Returns:
            mat_script: addition to MATLAB script under construction

        """
        experiments_all = [
            x["experiment_id"] for cnt, x in experimentalMS_data_I.iterrows()
        ]
        experiments = list(set(experiments_all))
        experiments.sort()

        fragments = fragments_used

        times_all = [
            x["time_point"] for cnt, x in experimentalMS_data_I.iterrows()
        ]
        times = list(set(times_all))
        times.sort()

        mat_script = ""
        # Add in ms data or Write ms data to separate file
        for experiment_cnt, experiment in enumerate(experiments):
            tmp_script = "\n% add experimental data for annotated fragments\n"
            for i, fragment in enumerate(fragments):
                for j, time_j in enumerate(times):
                    for cnt_x, ms_data in experimentalMS_data_I.iterrows():
                        if (
                            ms_data["fragment_id"] == fragments[i]
                            and ms_data["time_point"] == times[j]
                            and ms_data["experiment_id"] == experiment
                        ):
                            if not pd.isna(
                                ms_data["intensity_normalized_average"]
                            ):
                                ms_data_norm_ave_int = [
                                    float(x)
                                    for x in ms_data[
                                        "intensity_normalized_average"
                                    ]
                                    .strip("}{")
                                    .split(",")
                                ]
                                ms_data_norm_stdev_int = [
                                    float(x)
                                    for x in ms_data[
                                        "intensity_normalized_stdev"
                                    ]
                                    .strip("}{")
                                    .split(",")
                                ]
                                for cnt, intensity in enumerate(
                                    ms_data_norm_ave_int
                                ):
                                    # each column is a seperate time point
                                    # each row is a seperate mdv
                                    if cnt == 0:
                                        # Assign names and times
                                        name = (
                                            fragment
                                            + "_"
                                            + str(cnt)
                                            + "_"
                                            + str(j)
                                            + "_"
                                            + str(experiment)
                                        )
                                        tmp_script = tmp_script + (
                                            "m.expts(%d).data_ms(%d).mdvs.id(%d,%d) = {'%s'};\n"  # noqa E501
                                            % (
                                                experiment_cnt + 1,
                                                i + 1,
                                                cnt + 1,
                                                j + 1,
                                                name,
                                            )
                                        )
                                        tmp_script = tmp_script + (
                                            "m.expts(%d).data_ms(%d).mdvs.time(%d,%d) = %s;\n"  # noqa E501
                                            % (
                                                experiment_cnt + 1,
                                                i + 1,
                                                cnt + 1,
                                                j + 1,
                                                time_j,
                                            )
                                        )

                                    # Assign values
                                    ave = intensity
                                    stdev = ms_data_norm_stdev_int[cnt]
                                    # remove 0.0000 values and replace with NaN
                                    if ave <= 1e-6:
                                        ave = "NaN"
                                        tmp_script = tmp_script + (
                                            "m.expts(%d).data_ms(%d).mdvs.val(%d,%d) = %s;\n"  # noqa E501
                                            % (
                                                experiment_cnt + 1,
                                                i + 1,
                                                cnt + 1,
                                                j + 1,
                                                ave,
                                            )
                                        )
                                    else:
                                        tmp_script = tmp_script + (
                                            "m.expts(%d).data_ms(%d).mdvs.val(%d,%d) = %f;\n"  # noqa E501
                                            % (
                                                experiment_cnt + 1,
                                                i + 1,
                                                cnt + 1,
                                                j + 1,
                                                ave,
                                            )
                                        )
                                    if stdev <= 1e-3:
                                        if stdev == 0.0:
                                            stdev = 0.05
                                        else:
                                            stdev = 0.001
                                        tmp_script = tmp_script + (
                                            "m.expts(%d).data_ms(%d).mdvs.std(%d,%d) = %s;\n"  # noqa E501
                                            % (
                                                experiment_cnt + 1,
                                                i + 1,
                                                cnt + 1,
                                                j + 1,
                                                stdev,
                                            )
                                        )
                                    else:
                                        tmp_script = tmp_script + (
                                            "m.expts(%d).data_ms(%d).mdvs.std(%d,%d) = %f;\n"  # noqa E501
                                            % (
                                                experiment_cnt + 1,
                                                i + 1,
                                                cnt + 1,
                                                j + 1,
                                                stdev,
                                            )
                                        )
                            else:
                                ave == "NaN"
                                stdev = "NaN"
                                tmp_script = tmp_script + (
                                    "m.expts(%d).data_ms(%d).mdvs.std(%d,%d) = %s;\n"  # noqa E501
                                    % (
                                        experiment_cnt + 1,
                                        i + 1,
                                        cnt + 1,
                                        j + 1,
                                        stdev,
                                    )
                                )
            mat_script = mat_script + tmp_script

        return mat_script

    def script_generator(
        self,
        modelReaction_data_I,
        atomMappingReactions_data_I,
        atomMappingMetabolite_data_I,
        measuredFluxes_data_I,
        experimentalMS_data_I,
        tracer_I,
    ):
        """
        Combines the functions that construct the model

        Parameters:
            modelReaction_data_I: pre-processed
                modelReaction_data_I input data
            atomMappingReactions_data_I: pre-processed
                atomMappingReactions_data_I input data
            atomMappingMetabolite_data_I: pre-processed
                atomMappingMetabolite_data_I input data
            measuredFluxes_data_I: pre-processed
                measuredFluxes_data_I input data
            experimentalMS_data_I: pre-processed
                experimentalMS_data_I input data
            tracer_I: pre-processed
                tracer_I input data

        Returns:
            script: combined parts of the MATLAB script constrcted
                by the previously defined functions

        """
        script = ""
        script = self.initiate_MATLAB_script()
        script_temp, model_rxn_ids = self.add_reactions_to_script(
            modelReaction_data_I, atomMappingReactions_data_I
        )
        script += script_temp
        script += self.initialize_model()
        script += self.symmetrical_metabolites(atomMappingMetabolite_data_I)
        script += self.unbalanced_reactions(atomMappingMetabolite_data_I)
        script += self.add_reaction_parameters(
            modelReaction_data_I, measuredFluxes_data_I, model_rxn_ids
        )
        script += self.verify_and_estimate()
        script_temp, fragments_used = self.add_experimental_parameters(
            experimentalMS_data_I,
            tracer_I,
            measuredFluxes_data_I,
            atomMappingMetabolite_data_I,
        )
        script += script_temp
        script += self.mapping(experimentalMS_data_I, fragments_used)
        return script

    def save_INCA_script(self, script, scriptname):
        """
        Writes the output file

        Parameters:
            script: output from "script_generator()"
            scriptname: user defined name of the .m output file

        Outputs:
            .m INCA script

        """
        file1 = open(scriptname + ".m", "w")
        file1.write(script)
        file1.close()

    def runner_script_generator(self, output_filename, n_estimates=10):
        """
        Adds the functions needed to run the script and export the .mat file

        Parameters:
            output_filename: user defined name of the .mat output file, the
                INCA output file
            n_estimates: number of times the fluxes will be estimated

        Returns:
            runner: MATLAB script that will run the previously created
                INCA script

        """
        runner = (
            "f=estimate(m,"
            + str(n_estimates)
            + ");\n\nf=continuate(f,m);\n\nfilename = '"
            + output_filename
            + ".mat';\nsave(filename,'f','m')"
        )
        return runner

    def save_runner_script(self, runner, scriptname):
        """
        Writes the runner output file

        Parameters:
            runner: previously created runner script
            scriptname: name of the runner file, can be the same as
                the scriptname of the INCA script

        Outputs:
            .m runner script

        """
        file2 = open(scriptname + "_runner.m", "w")
        file2.write(runner)
        file2.close()

    def run_INCA_in_MATLAB(
        self, INCA_base_directory, script_folder, matlab_script, runner_script
    ):
        """
        Executes the script in MATLAB using INCA
        Prints time and produces .mat file

        Parameters:
            INCA_base_directory:
            script_folder:
            matlab_script:
            runner_script:

        Outputs:
            .mat output of INCA

        """
        start_time = time.time()
        eng = matlab.engine.start_matlab()
        eng.cd(r"" + INCA_base_directory, nargout=0)
        eng.startup(nargout=0)
        eng.setpath(nargout=0)
        eng.cd(r"" + script_folder, nargout=0)
        _f = getattr(eng, matlab_script)
        _f(nargout=0)
        _f2 = getattr(eng, runner_script)
        _f2(nargout=0)
        eng.quit()
        print("--- %s seconds -" % (time.time() - start_time))
