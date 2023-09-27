"""Atom Mapping.
Module that automatically performs atom-atom mapping of reactions,
when provided a metabolic model with suitable annotations.
Relies heavily on:
Reaction Decoder Tool (RDT) (https://github.com/asad/ReactionDecoder)
to map the reactions;
CADD Group Chemoinformatics Tools and User Services
(https://cactus.nci.nih.gov/chemical/structure)
to resolve InChI strings from given InChI keys;
Java, to run RDT"""

import requests
import os
import glob
import platform
import subprocess
import pandas as pd
import shutil
from pymatgen.symmetry import analyzer
from pymatgen.core import structure

try:
    from rdkit import Chem, RDLogger
except ModuleNotFoundError:
    print(
        "RDKit is not installed. Please install "
        "RDKit to use the atom mapping module."
    )

__version__ = "0.0.1"


class MolfileDownloader:
    def __init__(self, metabolite_data, base_path, db_preference=(0, 1, 2, 3)):
        """ Class to find and download metabolite structures in
        Molfile format.

        Parameters
        ----------
        metabolite_data : pandas.DataFrame
            Dataframe that contains information about metabolites
            the model. Obtain from INCA_input_parser module.
        db_preference : tuple of int, optional
            Four integers specify the order of preference of
            databases to obtain the metabolite structures from:
            0: Using InChI key > InChI string conversion
            1: KEGG Compound database
            2: HMDB database
            3: CHEBI database
        """
        self.database_dict = {
            0: "get_from_inchi_key",
            1: "get_from_kegg",
            2: "get_from_hmdb",
            3: "get_from_chebi",
        }

        self.metabolite_data = metabolite_data
        self.db_preference = db_preference
        self.base_path = base_path

    def generate_molfile_database(self):
        """ Main method that calls other methods and performs
        most sanity checks on obtained files.

        Parameters
        ----------
        base_path : str
            Path to the base directory.

        Outputs
        -------
        Molfiles : .mol files
        """
        
        print("Fetching metabolite structures...")

        # move to base path
        if self.base_path is not None:
            os.chdir(self.base_path)
        else:
            raise RuntimeError("Base path not specified")

        if not os.path.isdir("metabolites"):
            os.mkdir("metabolites")
        # Disable RDKit warnings
        RDLogger.DisableLog("rdApp.*")

        for i, met in self.metabolite_data.iterrows():
            self.filename = met.met_id + ".mol"

            get_from_inchi_keyBool = False
            get_from_keggBool = False
            get_from_hmdbBool = False
            get_from_chebiBool = False

            # Check for annotations and set bool values for those
            # present.
            if "inchi_key" in met.annotations:
                self.inchi_key = met.annotations["inchi_key"][0]
                get_from_inchi_keyBool = True  # noqa: F841
            if "kegg.compound" in met.annotations:
                self.keggIDs = [
                    keggID for keggID in met.annotations["kegg.compound"]
                ]
                get_from_keggBool = True  # noqa: F841
            if "hmdb" in met.annotations:
                self.hmdbIDnums = [
                    "0" * (7 - len(hmdbID[4:])) + hmdbID[4:]
                    for hmdbID in met.annotations["hmdb"]
                ]
                get_from_hmdbBool = True  # noqa: F841
            if "chebi" in met.annotations:
                self.chebiIDs = [
                    chebiID for chebiID in met.annotations["chebi"]
                ]
                get_from_chebiBool = True  # noqa: F841

            # Call helper functions according to order of preference
            # and available references (specified by previous bool values).
            for opt in self.db_preference:
                if eval(self.database_dict.get(opt) + "Bool"):
                    getattr(self, self.database_dict.get(opt))()
                else:
                    continue

                try:
                    # Rewrites the .mol file. This removes hydrogens from
                    # structure, lowkey standardizes molecules, and works
                    # as a failswitch to see if file is of correct format.
                    m = Chem.MolFromMolFile(f"metabolites/{self.filename}")
                    with open(f"metabolites/{self.filename}", "w+") as f:
                        print(Chem.MolToMolBlock(m), file=f)

                    # Add metabolite ID to the first line of Molfile
                    with open(f"metabolites/{self.filename}", "r") as f:
                        lines = f.readlines()
                        lines.insert(0, self.filename[:-4])
                        with open(f"metabolites/{self.filename}", "w") as wf:
                            wf.writelines(lines)
                    break
                except BaseException:
                    os.remove(f"metabolites/{self.filename}")
                    continue

        print(
            f"Successfully fetched {len(os.listdir('metabolites'))}/"
            f"{self.metabolite_data.shape[0]} metabolites"
        )

    def get_from_inchi_key(self):
        """ Helper method to obtain InChI string from InChI key,
        and generate the Molfile from the string.
        """
        url = (
            f"https://cactus.nci.nih.gov/chemical/"
            f"structure/{self.inchi_key}/stdinchi"
        )
        r = requests.get(url, allow_redirects=False)
        inchi_string = r.text

        try:
            molfile = Chem.inchi.MolFromInchi(inchi_string)
            with open(f"metabolites/{self.filename}", "w+") as f:
                print(Chem.MolToMolBlock(molfile), file=f)
        except BaseException:
            return

    def get_from_kegg(self):
        """ Helper method to obtain Molfile from KEGG Compound database
        """
        for keggID in self.keggIDs:
            url = (
                f"https://www.genome.jp/dbget-bin/"
                f"www_bget?-f+m+compound+{keggID}"
            )
            r = requests.get(url, allow_redirects=False)
            open(f"metabolites/{self.filename}", "wb").write(r.content)
            if os.path.getsize(f"metabolites/{self.filename}") != 0:
                break

    def get_from_hmdb(self):
        """ Helper method to obtain Molfile from HMDB database
        """
        for hmdbID in self.hmdbIDnums:
            url = f"https://hmdb.ca/structures/metabolites/HMDB{hmdbID}.mol"
            r = requests.get(url, allow_redirects=False)
            open(f"metabolites/{self.filename}", "wb").write(r.content)
            if os.path.getsize(f"metabolites/{self.filename}") != 0:
                break

    def get_from_chebi(self):
        """ Helper method to obtain Molfile from CHEBI database
        """
        for chebiID in self.chebiIDs:
            url = (
                f"https://www.ebi.ac.uk/chebi/saveStructure.do"
                f"?defaultImage=true&chebiId={chebiID}&imageId=0"
            )
            r = requests.get(url, allow_redirects=False)
            open(f"metabolites/{self.filename}", "wb").write(r.content)
            if os.path.getsize(f"metabolites/{self.filename}") != 0:
                break


def write_rxn_files(rxn_data, base_path):
    """ Generates RXN files in RDT suitable format.
    Requires Molfiles of all metabolites to be present
    in the working directory/metabolites folder.

    Parameters
    ----------
    rxn_data : pandas.DataFrame
        Dataframe that contains information about reactions
        in the model. Obtained from INCA_input_parser module.
    base_path : str
        Path to the base directory.

    Outputs
    -------
    RXN files : .rxn files
    """
    met_filter = ["h_e", "h_c", "h_p", "h2_e", "h2_c", "h2_p"]
    biomass_filter = ["Biomass", "biomass", "BIOMASS"]

    # move to base path
    if base_path is not None:
        os.chdir(base_path)
    else:
        raise RuntimeError("Base path not specified")


    if not os.path.isdir("unmappedRxns"):
        os.mkdir("unmappedRxns")

    path = os.path.join(os.getcwd(), "unmappedRxns")

    for i, rxn in rxn_data.iterrows():
        # Filter out biomass reaction
        if any(biomass_id in rxn.rxn_id for biomass_id in biomass_filter):
            print(f"Excluded {rxn.rxn_id} reaction from mapping")
            continue

        rxn_filename = rxn.rxn_id + ".rxn"
        # Use copies to avoid messing up the original dataframe
        reactants = rxn.reactants_ids.copy()
        reactants_st = [
            int(abs(s)) for s in rxn.reactants_stoichiometry.copy()
        ]
        products = rxn.products_ids.copy()
        products_st = [int(abs(s)) for s in rxn.products_stoichiometry.copy()]

        # Filter out unwanted molecules
        react_indexes = []
        prod_indexes = []
        for i, met in enumerate(reactants):
            if met in met_filter:
                react_indexes.append(i)
        if len(react_indexes) != 0:
            for i in sorted(react_indexes, reverse=True):
                del reactants[i]
                del reactants_st[i]

        for i, met in enumerate(products):
            if met in met_filter:
                prod_indexes.append(i)
        if len(prod_indexes) != 0:
            for i in sorted(prod_indexes, reverse=True):
                del products[i]
                del products_st[i]

        metabolites = reactants + products
        metabolites_st = reactants_st + products_st

        # Check if all metabolite structures are present
        if not all(
            [os.path.isfile(f"metabolites/{met}.mol") for met in metabolites]
        ):
            print(f"Metabolite structures missing for reaction {rxn.rxn_id}")
            continue
        else:
            with open(os.path.join(path, rxn_filename), "w") as f:
                # Write first three lines, including reaction equation
                f.write(f"$RXN\n{rxn.rxn_id}\n\n{rxn.equation}\n")

                # Write export reactions (1 reactant)
                if not products_st and abs(int(sum(reactants_st))) == 1:
                    f.write(
                        f"{abs(int(sum(reactants_st)))} "
                        f"{int(sum(reactants_st))}\n"
                    )
                    met = metabolites[0]
                    with open(f"metabolites/{met}.mol", "r") as wf:
                        structure = wf.read()
                        f.write(f"$MOL\n{structure}")
                        f.write(f"$MOL\n{structure}")

                # Write all the other reactions with at least 1 metabolite on
                # each side
                else:
                    f.write(
                        f"{abs(int(sum(reactants_st)))} "
                        f"{int(sum(products_st))}\n"
                    )
                    for s, met in zip(metabolites_st, metabolites):
                        with open(f"metabolites/{met}.mol", "r") as wf:
                            structure = wf.read()
                            # Repeat structure based on stoichiometry
                            for i in range(s):
                                f.write(f"$MOL\n{structure}")
    print(f"Generated {len(os.listdir('unmappedRxns'))}/{rxn_data.shape[0]}")


def obtain_atom_mappings(base_path, max_time=120):
    """ Performs atom mapping by using RDT.
    Only maps reactions that are available in .rxn format,
    in the working_directory/unmappedRxns folder.

    Parameters
    ----------
    max_time : int, optional
        Specifies time limit for single reaction mapping
        in seconds. Default: 120s.
    base_path : str
        Path to the base directory.

    Outputs
    -------
    mapped RXN files : .rxn files
    mapped TXT files : .txt files
        Mappings in SMILES format
    pictures of mappings : .png files
    """
    # move to base path
    if base_path is not None:
        os.chdir(base_path)
    else:
        raise RuntimeError("Base path not specified")

    # Check if Java is installed
    if os.system("java -version") != 0:
        raise RuntimeError("Java installation not found")

    print("Mapping reactions...")
    # Set the original working dir
    owd = os.getcwd()

    # Check if RDT is present in working dir, download if not
    if not os.path.isfile("RDT.jar"):
        url = (
            "https://github.com/asad/ReactionDecoder/"
            "releases/download/v2.4.1/rdt-2.4.1-jar-with-dependencies.jar"
        )
        r = requests.get(url)
        open(os.getcwd() + "/RDT.jar", "wb").write(r.content)

    # Check if required directories are present
    if not os.path.isdir("mappedRxns"):
        os.makedirs("mappedRxns/rxnFiles")
        os.makedirs("mappedRxns/txtFiles")
        os.makedirs("mappedRxns/pngFiles")

    rxn_list = os.listdir("unmappedRxns")
    print(rxn_list)

    # Change working dir to keep the output organized
    os.chdir("mappedRxns")
    try:
        for rxnFile in rxn_list:
            # Check if reaction is mapped, and run RDT with specified time
            # limit if not
            try:
                if not os.path.isfile(f"rxnFiles/{rxnFile}"):
                    subprocess.run(
                        [
                            "java",
                            "-jar",
                            "../RDT.jar",
                            "-Q",
                            "RXN",
                            "-q",
                            f"../unmappedRxns/{rxnFile}",
                            "-g",
                            "-j",
                            "AAM",
                            "-f",
                            "TEXT",
                        ],
                        timeout=max_time,
                    )
            except BaseException:
                continue
        # Obtain filenames of generated files and simplify them to respective
        # reaction IDs
        for name in glob.glob("ECBLAST*"):
            os.rename(name, name[8:-8] + name[-4:])

        # Move all generated files to different directories, in respect to
        # their filetype
        if platform.system() == "Windows":
            os.system("move *.png pngFiles")
            os.system("move *.rxn rxnFiles")
            os.system("move *.txt txtFiles")
        else:
            os.system("mv *.png ./pngFiles")
            os.system("mv *.rxn ./rxnFiles")
            os.system("mv *.txt ./txtFiles")

    except BaseException:
        # Make sure that wd is back to normal no matter what
        os.chdir(owd)

    print(
        f"Reactions mapped in total: "
        f"{len(os.listdir('rxnFiles'))}/{len(rxn_list)}"
    )
    # Change working dir back to original
    os.chdir(owd)

    # Remove RDT.jar from working dir
    os.remove("RDT.jar")


def parse_single_reaction_mappings(rxn_file_path, rxn_equation_unmapped):
    """
    Parses single reaction mapping from mapped RXN file
    to a dataframe in suitable format for INCA. Requires
    mapped RXN file to be present in the working_dir/
    mappedRxns/rxnFiles folder. For unmapped reactions,
    data is picked from working_dir/unmappedRxns folder
    and all mapping data is represented as blanks.

    Parameters
    ----------
    rxn_file_path : str

    Returns
    -------
    mapping_data : pandas.DataFrame
        Reaction mapping data.
    """

    keys = [
        "rxn_id",
        "reactants_stoichiometry_tracked",
        "products_stoichiometry_tracked",
        "reactants_ids_tracked",
        "products_ids_tracked",
        "reactants_mapping",
        "products_mapping",
        "rxn_equation",
        "reactants_elements_tracked",
        "products_elements_tracked",
        "reactants_positions_tracked",
        "products_positions_tracked",
    ]
    mapping_dict_tmp = {}
    mapping_dict = {k: [] for k in keys}
    met_mapping = []
    react_cnt = 0
    prod_cnt = 0
    productBool = False
    rxn = ''

    with open(f"{rxn_file_path}", "r") as f:
        lines = f.readlines()
        for j, line in enumerate(lines):
            if line.rstrip() == "$RXN":
                # Extract number of reactants
                react_lim = int(lines[j + 4].split()[0])
                # Extract number of products
                prod_lim = int(lines[j + 4].split()[1])
            if line.rstrip() == "$MOL":
                met_id = lines[j + 1].rstrip()

            # Hard-coded, since 16 columns is standard for Molfile
            # atom rows,
            # and 15 can occur if we have >100 atoms on one side (cols
            # merge)
            if len(line.split()) in (15, 16):
                atom_row = line.split()
                if atom_row[3] == "C":
                    # Split columns if they get merged
                    if atom_row[-3][0] == "0":
                        atom_row[-3] = atom_row[-3][1:]
                    met_mapping.append(atom_row[-3])

                # Check if reached the last atom row
                if len(lines[j + 1].split()) not in (15, 16):
                    # Check if current metabolite is reactant or
                    # product
                    if not productBool:
                        # Check if any carbons are present
                        if met_mapping:
                            c_tracked = ["C" for atom in met_mapping]
                            pos_tracked = list(range(len(met_mapping)))
                            mapping_dict[
                                "reactants_ids_tracked"
                            ].append(met_id)
                            mapping_dict["reactants_mapping"].append(
                                met_mapping
                            )
                            mapping_dict[
                                "reactants_elements_tracked"
                            ].append(c_tracked)
                            mapping_dict[
                                "reactants_positions_tracked"
                            ].append(pos_tracked)
                        react_cnt += 1
                        if react_cnt == react_lim:
                            productBool = True

                    # Assign metabolite to products if reached reactant
                    # limit
                    else:
                        if met_mapping:
                            c_tracked = ["C" for atom in met_mapping]
                            pos_tracked = list(range(len(met_mapping)))
                            mapping_dict[
                                "products_ids_tracked"
                            ].append(met_id)
                            mapping_dict["products_mapping"].append(
                                met_mapping
                            )
                            mapping_dict[
                                "products_elements_tracked"
                            ].append(c_tracked)
                            mapping_dict[
                                "products_positions_tracked"
                            ].append(pos_tracked)
                        prod_cnt += 1

                        if prod_cnt == prod_lim:
                            react_stoich = [
                                "-1"
                                for met in range(
                                    len(
                                        mapping_dict[
                                            "reactants_mapping"
                                        ]
                                    )
                                )
                            ]
                            prod_stoich = [
                                "1"
                                for met in range(
                                    len(
                                        mapping_dict[
                                            "products_mapping"
                                        ]
                                    )
                                )
                            ]
                            mapping_dict[
                                "reactants_stoichiometry_tracked"
                            ] = react_stoich
                            mapping_dict[
                                "products_stoichiometry_tracked"
                            ] = prod_stoich

                    met_mapping = []

    mapping_dict["rxn_id"] = rxn[:-4]
    mapping_dict_tmp[0] = mapping_dict
    mapping_data = pd.DataFrame.from_dict(mapping_dict_tmp, "index")

    # alphabet for number-letter matching. Max capacity is 63 characters,
    # which is a limit set in INCA for this format.
    alphabet = (
        list(map(chr, range(97, 123)))
        + list(map(chr, range(65, 91)))
        + list(map(chr, range(48, 58)))
        + ["_"]
    )

    # Loop through all reactions
    for i, rxn in mapping_data.iterrows():
        try:
            # Convert number mappings to letters
            carbons_list = [
                atom for met in rxn["reactants_mapping"] for atom in met
            ]
            carbon_map_dict = dict(zip(carbons_list, alphabet))

            # Generate a reaction equation
            reaction_str = ""
            if len(rxn["reactants_mapping"]) < 1 and len(
                rxn["products_mapping"]
            ) < 1:
                return None
            for j, met in enumerate(rxn["reactants_mapping"]):
                reactant_str = " ("
                if j != 0:
                    reaction_str += " + "
                reaction_str += str(
                    abs(
                        float(
                            rxn["reactants_stoichiometry_tracked"][j]))) + '*'
                reaction_str += rxn["reactants_ids_tracked"][j]
                for k, atom in enumerate(met):
                    if k != 0:
                        reactant_str += " "
                    reactant_str += f"C{str(k+1)}:"
                    reactant_str += carbon_map_dict[atom]
                reactant_str += ")"
                reaction_str += reactant_str
            
            if '<' in rxn_equation_unmapped:
                reaction_str += ' <-> '
            else:
                reaction_str += ' -> '

            for j, met in enumerate(rxn["products_mapping"]):
                product_str = " ("
                if j != 0:
                    reaction_str += " + "
                reaction_str += str(
                    abs(
                        float(
                            rxn["products_stoichiometry_tracked"][j]))) + '*'
                reaction_str += rxn["products_ids_tracked"][j]
                for k, atom in enumerate(met):
                    if k != 0:
                        product_str += " "
                    product_str += f"C{str(k+1)}:"
                    product_str += carbon_map_dict[atom]
                product_str += ")"
                reaction_str += product_str
            
            mapping_data.at[i, "rxn_equation"] = reaction_str

        except KeyError:
            if len(carbons_list) > 63:
                print(
                    f'Reaction {rxn["rxn_id"]} contains '
                    f"more than 63 carbon atoms"
                )
            else:
                # Mostly happens when one of the metabolites has (R)
                # group in the Molfile, and other has a C in that spot
                print(f'{rxn["rxn_id"]} has unmapped carbon(-s)')
            reaction_str = None

    return reaction_str


def parse_reaction_mappings_old():
    """ Parses reaction mappings from mapped RXN files
    to a dataframe in suitable format for INCA. Requires
    all mapped RXN files to be present in the working_dir/
    mappedRxns/rxnFiles folder. For unmapped reactions,
    data is picked from working_dir/unmappedRxns folder
    and all mapping data is represented as blanks.

    Returns
    -------
    mapping_data : pandas.DataFrame
        Reaction mapping data.
    """
    if not os.path.isdir("mappedRxns"):
        raise RuntimeError(
            "'mappedRxns' directory not present in current working directory"
        )

    rxn_list = sorted(os.listdir("unmappedRxns"))
    # Compile list of reactions that do not have any mapping
    unmapped_list = list(
        set(os.listdir("unmappedRxns"))
        - set(os.listdir("mappedRxns/rxnFiles"))
    )

    keys = [
        "Unnamed: 0",
        "Unnamed: 0.1",
        "id",
        "mapping_id",
        "rxn_id",
        "rxn_description",
        "reactants_stoichiometry_tracked",
        "products_stoichiometry_tracked",
        "reactants_ids_tracked",
        "products_ids_tracked",
        "reactants_mapping",
        "products_mapping",
        "rxn_equation",
        "used_",
        "comment_",
        "reactants_elements_tracked",
        "products_elements_tracked",
        "reactants_positions_tracked",
        "products_positions_tracked",
    ]
    mapping_dict_tmp = {}

    for i, rxn in enumerate(rxn_list):
        mapping_dict = {k: [] for k in keys}
        met_mapping = []
        react_cnt = 0
        prod_cnt = 0
        productBool = False

        if rxn not in unmapped_list:
            # Extract info from mapped .rxn files
            with open(f"mappedRxns/rxnFiles/{rxn}", "r") as f:
                lines = f.readlines()
                for j, line in enumerate(lines):
                    if line.rstrip() == "$RXN":
                        # Extract number of reactants
                        react_lim = int(lines[j + 4].split()[0])
                        # Extract number of products
                        prod_lim = int(lines[j + 4].split()[1])
                    if line.rstrip() == "$MOL":
                        met_id = lines[j + 1].rstrip()

                    # Hard-coded, since 16 columns is standard for Molfile
                    # atom rows,
                    # and 15 can occur if we have >100 atoms on one side (cols
                    # merge)
                    if len(line.split()) in (15, 16):
                        atom_row = line.split()
                        if atom_row[3] == "C":
                            # Split columns if they get merged
                            if atom_row[-3][0] == "0":
                                atom_row[-3] = atom_row[-3][1:]
                            met_mapping.append(atom_row[-3])

                        # Check if reached the last atom row
                        if len(lines[j + 1].split()) not in (15, 16):
                            # Check if current metabolite is reactant or
                            # product
                            if not productBool:
                                # Check if any carbons are present
                                if met_mapping:
                                    c_tracked = ["C" for atom in met_mapping]
                                    pos_tracked = list(range(len(met_mapping)))
                                    mapping_dict[
                                        "reactants_ids_tracked"
                                    ].append(met_id)
                                    mapping_dict["reactants_mapping"].append(
                                        met_mapping
                                    )
                                    mapping_dict[
                                        "reactants_elements_tracked"
                                    ].append(c_tracked)
                                    mapping_dict[
                                        "reactants_positions_tracked"
                                    ].append(pos_tracked)
                                react_cnt += 1
                                if react_cnt == react_lim:
                                    productBool = True

                            # Assign metabolite to products if reached reactant
                            # limit
                            else:
                                if met_mapping:
                                    c_tracked = ["C" for atom in met_mapping]
                                    pos_tracked = list(range(len(met_mapping)))
                                    mapping_dict[
                                        "products_ids_tracked"
                                    ].append(met_id)
                                    mapping_dict["products_mapping"].append(
                                        met_mapping
                                    )
                                    mapping_dict[
                                        "products_elements_tracked"
                                    ].append(c_tracked)
                                    mapping_dict[
                                        "products_positions_tracked"
                                    ].append(pos_tracked)
                                prod_cnt += 1

                                if prod_cnt == prod_lim:
                                    react_stoich = [
                                        "-1"
                                        for met in range(
                                            len(
                                                mapping_dict[
                                                    "reactants_mapping"
                                                ]
                                            )
                                        )
                                    ]
                                    prod_stoich = [
                                        "1"
                                        for met in range(
                                            len(
                                                mapping_dict[
                                                    "products_mapping"
                                                ]
                                            )
                                        )
                                    ]
                                    mapping_dict[
                                        "reactants_stoichiometry_tracked"
                                    ] = react_stoich
                                    mapping_dict[
                                        "products_stoichiometry_tracked"
                                    ] = prod_stoich

                            met_mapping = []

        mapping_dict["rxn_id"] = rxn[:-4]
        mapping_dict["used_"] = True
        # Fill all empty fields
        mapping_dict["Unnamed: 0"] = "NULL"
        mapping_dict["Unnamed: 0.1"] = "NULL"
        mapping_dict["id"] = "NULL"
        mapping_dict["mapping_id"] = "NULL"
        mapping_dict["rxn_description"] = "NULL"
        mapping_dict["rxn_equation"] = "NULL"
        mapping_dict["comment_"] = "NULL"

        mapping_dict_tmp[i] = mapping_dict

    mapping_data = pd.DataFrame.from_dict(mapping_dict_tmp, "index")

    # alphabet for number-letter matching. Max capacity is 63 characters,
    # which is a limit set in INCA for this format.
    alphabet = (
        list(map(chr, range(97, 123)))
        + list(map(chr, range(65, 91)))
        + list(map(chr, range(48, 58)))
        + ["_"]
    )

    # Loop through all reactions
    for i, rxn in mapping_data.iterrows():
        try:
            # Convert number mappings to letters
            carbons_list = [
                atom for met in rxn["reactants_mapping"] for atom in met
            ]
            carbon_map_dict = dict(zip(carbons_list, alphabet))

            # Compile alphabetical mapping in curly bracket format
            carbon_str = "{"
            for j, met in enumerate(rxn["reactants_mapping"]):
                if j != 0:
                    carbon_str += ","
                for atom in met:
                    carbon_str += carbon_map_dict[atom]
            carbon_str += "}"
            mapping_data.at[i, "reactants_mapping"] = carbon_str

            carbon_str = "{"
            for j, met in enumerate(rxn["products_mapping"]):
                if j != 0:
                    carbon_str += ","
                for atom in met:
                    carbon_str += carbon_map_dict[atom]
            carbon_str += "}"
            mapping_data.at[i, "products_mapping"] = carbon_str

        except KeyError:
            if len(carbons_list) > 63:
                print(
                    f'Reaction {rxn["rxn_id"]} contains '
                    f"more than 63 carbon atoms"
                )
            else:
                # Mostly happens when one of the metabolites has (R)
                # group in the Molfile, and other has a C in that spot
                print(f'{rxn["rxn_id"]} has unmapped carbon(-s)')
            mapping_data.at[i, "reactants_mapping"] = "{}"
            mapping_data.at[i, "products_mapping"] = "{}"

        # Convert metabolite lists/stoichiometries to strings in curly brackets
        metabolite_str = "{%s}" % (",".join(rxn["reactants_ids_tracked"]))
        mapping_data.at[i, "reactants_ids_tracked"] = metabolite_str

        metabolite_str = "{%s}" % (",".join(rxn["products_ids_tracked"]))
        mapping_data.at[i, "products_ids_tracked"] = metabolite_str

        stoich_str = "{%s}" % (
            ",".join(rxn["reactants_stoichiometry_tracked"])
        )
        mapping_data.at[i, "reactants_stoichiometry_tracked"] = stoich_str

        stoich_str = "{%s}" % (",".join(rxn["products_stoichiometry_tracked"]))
        mapping_data.at[i, "products_stoichiometry_tracked"] = stoich_str

    return mapping_data


def parse_reaction_mappings(mapped_rxn_path, rxn_data):
    """
    """
    if not os.path.isdir("mappedRxns"):
        raise RuntimeError(
            "'mappedRxns' directory not present in current working directory"
        )

    rxn_list = sorted(os.listdir(mapped_rxn_path))
    rxn_list = [rxn[:-4] for rxn in rxn_list]
    rxn_mapping = {
        'rxn_id': [],
        'equation': [],
    }
    for _, rxn in rxn_data.iterrows():
        rxn_id = rxn['rxn_id']
        if rxn_id in rxn_list:
            rxn_file_path = f'/Users/krv114/Documents/GitHub/incawrapper/mappedRxns/rxnFiles/{rxn_id}.rxn'
            rxn_equation_unmapped = rxn['equation']
            try:
                equation = parse_single_reaction_mappings(
                    rxn_file_path, rxn_equation_unmapped)
                if equation is None:
                    continue
                else:
                    rxn_mapping['rxn_id'].append(rxn_id)
                    rxn_mapping['equation'].append(equation)
            except Exception as e:
                print(f'Could not parse {rxn_id}, ', e)
                continue
        else:
            print(f'{rxn_id} not mapped')
            continue
    rxn_mapping = pd.DataFrame(rxn_mapping)

    return rxn_mapping


def parse_metabolite_mappings():
    """ Parses metabolite mapping and symmetry data into
    INCA suitable format. Requires all Molfiles to be present
    in the working_dir/metabolites directory.

    Returns
    -------
    metabolite_data : pandas.DataFrame
        Dataframe containing mapped metabolite data.
    """
    metabolite_list = sorted(os.listdir("metabolites"))
    keys = [
        "mapping_id",
        "met_id",
        "met_elements",
        "met_atompositions",
        "met_symmetry_elements",
        "met_symmetry_atompositions",
        "used_",
        "comment_",
        "met_mapping",
        "base_met_ids",
        "base_met_elements",
        "base_met_atompositions",
        "base_met_symmetry_elements",
        "base_met_symmetry_atompositions",
        "base_met_indices",
    ]
    metabolite_dict_tmp = {}

    # Works in a similar fashion to parse_reaction_mappings()
    for i, met in enumerate(metabolite_list):
        met_dict = {k: "NULL" for k in keys}
        with open(f"metabolites/{met}", "r") as f:
            lines = f.readlines()
            carbon_count = 0
            for j, line in enumerate(lines):
                if j == 0:
                    met_dict["met_id"] = line.rstrip()
                if len(line.split()) == 16:
                    atom_row = line.split()
                    if atom_row[3] == "C":
                        carbon_count += 1
            # Generate carbon atom lists/mappings
            carbon_count_list = ["C" for x in range(carbon_count)]
            carbon_count_string = "{%s}" % (",".join(carbon_count_list))
            carbon_count_range = "{%s}" % (
                ",".join([str(x) for x in range(carbon_count)])
            )

            met_dict["met_elements"] = carbon_count_string
            met_dict["met_atompositions"] = carbon_count_range
            # Check if the metabolite is symmetrical
            if check_symmetry(met):
                carbon_count_range_rev = "{%s}" % (
                    ",".join([str(x) for x in range(carbon_count - 1, -1, -1)])
                )
                met_dict["met_symmetry_elements"] = carbon_count_string
                met_dict["met_symmetry_atompositions"] = carbon_count_range_rev

            metabolite_dict_tmp[i] = met_dict

    metabolite_data = pd.DataFrame.from_dict(metabolite_dict_tmp, "index")

    return metabolite_data


def generate_INCA_mapping_input(reaction_df, metabolite_df):
    """ Function to export reaction and metabolite mapping dataframes
    to CSV files.

    Parameters
    ----------
    reaction_df : pandas.DataFrame
        Dataframe that contains reaction mapping data.
    metabolite_df : pandas.DataFrame
        Dataframe that contains metabolite mapping data.

    Outputs
    -------
    MappingReactions : .csv file
    MappingMetabolites : .csv file
    """
    # Would be a good idea to make the filenames more informative.
    reaction_df.to_csv(
        path_or_buf=os.path.join(os.getcwd(), "MappingReactions.csv")
    )
    metabolite_df.to_csv(
        path_or_buf=os.path.join(os.getcwd(), "MappingMetabolites.csv")
    )


def check_symmetry(met_filename):
    """ Function that checks if the given metabolite is symmetric.
    Uses pymatgen package for symmetry related operations, and
    RDKit for Molfile conversion to XYZ format. Requires Molfiles
    of the metabolites to be present in the working_dir/metabolites
    folder.
    Current criterion for symmetricity is for every carbon except one
    (central, if molecule consists of odd number of carbons) to have
    at least one equivalent carbon in the structure.

    Parameters
    ----------
    met_filename : str
        Filename of the specific Molfile

    Returns
    -------
    symmetrical : bool
        True if metabolite is symmetric, False if not.

    """
    symmetrical = False
    # Disable RDKit warnings
    RDLogger.DisableLog("rdApp.*")
    # Counter for non symmetrical carbon atoms
    non_eq_carbons = 0
    carbons = 0
    # Convert Molfile to XYZ string
    molecule = Chem.MolFromMolFile(f"metabolites/{met_filename}")
    molecule_xyz = Chem.rdmolfiles.MolToXYZBlock(molecule)

    # Create IMolecule object to analyze its' symmetricity
    try:
        molecule_obj = structure.IMolecule.from_str(molecule_xyz, fmt="xyz")
        if len(molecule_obj) == 1:
            return symmetrical
        # Initialize point group analyzer
        pg_analyzer = analyzer.PointGroupAnalyzer(molecule_obj)

    except (IndexError, ValueError):
        # '*' is unrecognized in particular
        print(f"{met_filename} contains unrecognized symbols")
        return symmetrical
    # Extract equal atom sets
    eq_atoms = pg_analyzer.get_equivalent_atoms()
    for i in eq_atoms["eq_sets"].keys():
        if str(molecule_obj[i].specie) == "C":
            carbons += 1
            if len(eq_atoms["eq_sets"].get(i)) == 1:
                non_eq_carbons += 1
                if non_eq_carbons > 1:
                    return symmetrical

    # Molecule has more than 1 carbon, and at most 1 non-symmetrical carbon
    if carbons > 1:
        symmetrical = True

    return symmetrical


def clean_output(base_path, metabolites=True, reactions=True, mappings=True, csv=False):
    """ Utility function.
    Deletes all possible output of other mapping functions.
    Deletes everything by default.

    Parameters
    ----------
    base_path : str
        Path to the base directory.
    metabolites : bool, optional
        Removes /metabolites folder recursively.
    reactions : bool, optional
        Removes /unmappedRxns folder recursively.
    mappings : bool, optional
        Removes /mappedRxns folder recursively.
    csv : bool, optional
        Removes MappingReactions.csv and MappingMetabolites.csv.
    """
    # mo
    if metabolites:
        shutil.rmtree("metabolites")
    if reactions:
        shutil.rmtree("unmappedRxns")
    if mappings:
        shutil.rmtree("mappedRxns")
    if csv:
        os.remove("MappingReactions.csv")
        os.remove("MappingMetabolites.csv")


# molfile_downloader_descr = MolfileDownloader()
# """A class to find and fetch metabolite structures in Molfile
# format.

# Examples
# --------
# >>> downloader = MolfileDownloader(met_df)
# >>> downloader.generate_molfile_database()
# The database will be generated in working_dir/metabolites folder

# To change the order of databases for fetching, pass a tuple of
# integers when initiating an instance, f.e.:
# >>> downloader = MolfileDownloader(met_df, (2,1,0,3))
# >>> downloader.generate_molfile_database()

# For full workflow check, the example notebook. """
