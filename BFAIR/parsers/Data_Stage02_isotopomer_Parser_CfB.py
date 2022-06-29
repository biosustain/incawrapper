"""INCA reaction input parser.
Methods to prepare  reaction input data to fit the BFAIR INCA tools format.
"""

import pandas as pd

def reaction_parser(equation_string):
    """
    Parses a string representing a reaction into the form of 
    (reactant_list, product_list, reversible)

    Parameters
    ----------
    equation_string : str
        String representing a reaction

    Returns
    -------
    reactant_list : list
        List of reactants in the reaction
    product_list : list
        List of products in the reaction
    reversible : bool
        Whether the reaction is reversible

    Examples:
    >>> reaction_parser('A (abc) + B -> 2*C + D')
    ([('A', 1, 'abc'), ('B', 1, None)], [('C', 2, None), ('D', 1, None)], False)
    >>> reaction_parser('A + 8*B <-> C + D (ab) + E')
    ([('A', 1, None), ('B', 8, None)], [('C', 1, None), ('D', 1, 'ab'), ('E', 1, None)], True)
    """
    if '<->' in equation_string:
        reversible = True
        reaction_arrow = '<->'
    elif '->' in equation_string:
        reversible = False
        reaction_arrow = '->'
    else:
        reversible = False
        reaction_arrow = '<-'
    
    reactant_string, product_string = equation_string.split(reaction_arrow)

    if reaction_arrow == '<-':
        reactant_string, product_string = product_string, reactant_string


    # Split the reactant string into reactants by the '+'
    reactant_list = reactant_string.split('+')

    # Split the product string into products by the '+' 
    product_list = product_string.split('+')

    # Strip the whitespace from the reactant and product strings
    reactant_list = [reactant.strip() for reactant in reactant_list]
    product_list = [product.strip() for product in product_list]

    def parse_reactant(reactant):
        """
        Parses a reactant string into a tuple of (reactant, stoichiometry, carbon_map)
        """
        # Check if a * is in the reactant string
        if '*' in reactant:
            # Split the reactant string into the reactant and stoichiometry
            stoichiometry, reactant_and_carbon = reactant.split('*')
            # Strip the whitespace from the reactant and stoichiometry
            reactant_and_carbon = reactant_and_carbon.strip()
            stoichiometry = stoichiometry.strip()
            # Convert the stoichiometry to an int
            stoichiometry = float(stoichiometry)
        else:
            stoichiometry = 1.0
            reactant_and_carbon = reactant.strip()
        
        # Check if a carbon map is in the reactant string
        if '(' in reactant_and_carbon:
            # Split the reactant string into the reactant and carbon map
            compound, carbon_map = reactant_and_carbon.split('(')
            # Strip the whitespace from the reactant and carbon map
            compound = compound.strip()
            carbon_map = carbon_map.strip()
            # Remove the closing ')' from the carbon map
            carbon_map = carbon_map[:-1]
        else:
            carbon_map = None
            compound = reactant_and_carbon.strip()
        
        # Return the parsed reactant tuple
        return (compound, stoichiometry, carbon_map)

    # Parse the reactants
    reactant_list = [parse_reactant(reactant) for reactant in reactant_list]
    product_list = [parse_reactant(product) for product in product_list]

    # Return the parsed reaction tuple
    return (reactant_list, product_list, reversible)


def modelReactions_file_parser(file_path, model_id, reaction_id_col_name='Reaction ID', equation_col_name='Equations (Carbon atom transition)'):
    """
    Parses a file containing reaction data into a pandas dataframe

    Parameters
    ----------
    file_path : str
        Path to the file containing the reaction data
    model_id : str
        ID of the model
    reaction_id_col_name : str
        Name of the column containing the reaction IDs
    equation_col_name : str 
        Name of the column containing the reaction equations
    
    Returns
    -------
    model_reaction_data : pandas.DataFrame
        Dataframe containing the reaction data
    """
    # Check if the file is a csv or excel file
    if file_path.endswith('.csv'):
        # Read the csv file
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        # Read the excel file
        df = pd.read_excel(file_path)
    else:
        # Raise an error if the file is not a csv or excel file
        raise ValueError('File must be a csv or excel file.')
    
    # Check if the reaction id column name is in the dataframe
    if reaction_id_col_name not in df.columns:
        # Raise an error if the reaction id column name is not in the dataframe
        raise ValueError(f"""
        Equation column name not in dataframe.
        Column names: {df.columns}
        """)
    
    # Check if the equation column name is in the dataframe
    if equation_col_name not in df.columns:
        # Raise an error if the equation column name is not in the dataframe
        raise ValueError(f"""
        Equation column name not in dataframe.
        Column names: {df.columns}
        """)
    
    model_reaction_data = []
    # Loop over each row
    for reaction_id, equation in zip(df[reaction_id_col_name], df[equation_col_name]):
        try:
            reactants, products, reversible = reaction_parser(equation)
        except ValueError:
            # Raise an error if the equation is not a valid reaction
            raise ValueError(f"""
            Equation {equation} is not a valid reaction.
            """)

        # Create a dictionary containing the reaction data
        left_side = " + ".join([f'{reactant[1]} {reactant[0]}' for reactant in reactants])
        right_side = " + ".join([f'{product[1]} {product[0]}' for product in products])
        reaction_stoichiometry = ",".join([f'{-reactant[1]}' for reactant in reactants])
        product_stoichiometry = ",".join([f'{product[1]}' for product in products])
        
        model_reaction_output_dict = {
            "id": reaction_id,
            "model_id": model_id,
            "rxn_id": reaction_id,
            "rxn_name": "NULL",
            "equation": f"{left_side} {'<-->' if reversible else '-->'} {right_side}",
            "subsystem": "",
            "gpr": "",
            "genes": "{}",
            "reactant_stoichiometry": f"{{{reaction_stoichiometry}}}",
            "product_stoichiometry": f"{{{product_stoichiometry}}}",
            "reactants_ids": f"{{{','.join([reactant[0] for reactant in reactants])}}}",
            "products_ids": f"{{{','.join([product[0] for product in products])}}}",
            "lower_bound": "0",
            "upper_bound": "1000",
            "objective_coefficient": "0",
            "flux_units": "mmol*gDW-1*hr-1",
            "fixed": "NULL",
            "free": "NULL",
            "reversibility": f"{reversible}",
            "weight": "NULL",
            "used": "True",
            "comment_": "" 
        }
        model_reaction_data.append(model_reaction_output_dict)

    return pd.DataFrame(model_reaction_data) 

source_file = r'PATH/pputida_model.xlsx'
datafile = modelReactions_file_parser(source_file, 'my_model')
filename = r'PATH/pputida_model_Reaction.csv'
datafile.to_csv(filename, index=False)


def atomMapping_reactions2_file_parser(file_path, model_id, reaction_id_col_name='Reaction ID', equation_col_name='Equations (Carbon atom transition)'):
    """
    Parses a file containing reaction data into a pandas dataframe containing the carbon atom mapping data, only considering compounds with carbon

    Parameters
    ----------
    file_path : str
        Path to the file containing the reaction data
    model_id : str
        ID of the model
    reaction_id_col_name : str
        Name of the column containing the reaction IDs
    equation_col_name : str 
        Name of the column containing the reaction equations

    Returns
    -------
    atom_mapping_data : pandas.DataFrame
        Dataframe containing the reaction data
    """
    # Check if the file is a csv or excel file
    if file_path.endswith('.csv'):
        # Read the csv file
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        # Read the excel file
        df = pd.read_excel(file_path)
    else:
        # Raise an error if the file is not a csv or excel file
        raise ValueError('File must be a csv or excel file.')

    # Check if the reaction id column name is in the dataframe
    if reaction_id_col_name not in df.columns:
        # Raise an error if the reaction id column name is not in the dataframe
        raise ValueError(f"""
        Equation column name not in dataframe.
        Column names: {df.columns}
        """)
        # Check if the equation column name is in the dataframe
    if equation_col_name not in df.columns:
        # Raise an error if the equation column name is not in the dataframe
        raise ValueError(f"""
        Equation column name not in dataframe.
        Column names: {df.columns}
        """)

    atom_mapping_data = []
    # Loop over each row
    for reaction_id, equation in zip(df[reaction_id_col_name], df[equation_col_name]):
        try:
            reactants, products, reversible = reaction_parser(equation)
        except ValueError:
            # Raise an error if the equation is not a valid reaction
            raise ValueError(f"""
            Equation {equation} is not a valid reaction.
            """)

        # Create a dictionary containing the atom mapping data

        # Only include reactants/products with carbon mapping in the stoichiometry
        reactants_with_carbon = [
            reactant for reactant in reactants if reactant[2] is not None]
        products_with_carbon = [
            product for product in products if product[2] is not None]
        left_side = " + ".join(
            [f'{reactant[1]} {reactant[0]}' for reactant in reactants])
        right_side = " + ".join(
            [f'{product[1]} {product[0]}' for product in products])
        tracked_Cs_reactants = [len(reactant[2])*['"C"']
                                for reactant in reactants_with_carbon]
        tracked_Cs_products = [len(product[2])*['"C"']
                               for product in products_with_carbon]
        reactants_positions_tracked = [
            list(range(len(reactant[2]))) for reactant in reactants_with_carbon
        ]
        products_positions_tracked = [
            list(range(len(product[2]))) for product in products_with_carbon
        ]

        atom_mapping_output_dict = {
            "id": reaction_id,
            "mapping_id": model_id,
            "rxn_id": reaction_id,
            "rxn_description": "",
            "reactants_stoichiometry": f"{{{','.join([str(-reactant[1]) for reactant in reactants_with_carbon])}}}",
            "products_stoichiometry": f"{{{','.join([str(product[1]) for product in products_with_carbon])}}}",
            "reactants_ids": f"{{{','.join([reactant[0] for reactant in reactants_with_carbon])}}}",
            "products_ids": f"{{{','.join([product[0] for product in products_with_carbon])}}}",
            "reactants_mapping": f"{{{','.join([reactant[2] for reactant in reactants_with_carbon])}}}",
            "products_mapping": f"{{{','.join([product[2] for product in products_with_carbon])}}}",
            "rxn_equation": left_side + " " + ("<-->" if reversible else "-->") + " " + right_side,
            "used_": "True",
            "comment_": "",
            "reactants_elements_tracked": tracked_Cs_reactants,
            "products_elements_tracked": tracked_Cs_products,
            "reactants_positions_tracked": f"{reactants_positions_tracked}",
            "products_positions_tracked": f"{products_positions_tracked}"
        }
        atom_mapping_data.append(atom_mapping_output_dict)

    return pd.DataFrame(atom_mapping_data)

source_file = r'PATH/pputida_model.xlsx'
datafile = atomMapping_reactions2_file_parser(source_file, 'my_model')
filename = r'PATH/pputida_atom_mappings3.csv'
datafile.to_csv(filename, index=False)

def atom_mapping_metabolites_file_parser(file_path, model_id, reaction_id_col_name ='Reaction ID', equation_col_name='Equations (Carbon atom transition)'):
    """
    Parses a file containing metabolite data into a pandas dataframe containing every meatbolite that contains carbon including the metabolites atom positions.
    
    Parameters
    ----------
    file_path : str
        Path to the file containing the metabolite data
        
    model_id : str
        ID of the model
        
    reaction_id : str
        Name of the column containing the reaction IDs                
    
    element_col_name : str
        Name of the column containing the metabolite elements
    
    Returns 
    -------
    metabolite_df : pandas.DataFrame
        Dataframe containing the metabolite data
        
    """

    # Check if the file is a csv or excel file
    if file_path.endswith('.csv'):
        # Read the csv file
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        # Read the excel file
        df = pd.read_excel(file_path)
    else:
        # Raise an error if the file is not a csv or excel file
        raise ValueError('File must be a csv or excel file.')

     # Check if the reaction id column name is in the dataframe
    if reaction_id_col_name not in df.columns:
        # Raise an error if the reaction id column name is not in the dataframe
        raise ValueError(f"""
        Equation column name not in dataframe.
        Column names: {df.columns}
        """)
        # Check if the equation column name is in the dataframe
    if equation_col_name not in df.columns:
        # Raise an error if the equation column name is not in the dataframe
        raise ValueError(f"""
        Equation column name not in dataframe.
        Column names: {df.columns}
        """)

    metabolite_data = []
    reactants_list = []
    products_list = []
    # Loop over each row
    for reaction_id, equation in zip(df[reaction_id_col_name], df[equation_col_name]):
        try:
            reactants, products, _reversible = reaction_parser(equation)
            reactants_list += reactants
            products_list += products
        except ValueError:
            # Raise an error if the equation is not a valid reaction
            raise ValueError(f"""
            Equation {equation} is not a valid reaction.
            """)
    
    # Create a dictionary containing the atom mapping metabolites data
    # Only include metabolites with carbon mapping
    reactants_with_carbon = [
            reactant for reactant in reactants_list if reactant[2] is not None]
    products_with_carbon = [
            product for product in products_list if product[2] is not None]
    all_metabolites = reactants_with_carbon + products_with_carbon

    # Make a list of all unique metabolites by name
    unique_metabolites_index = set([])
    unique_metabolites = []
    for metabolite in all_metabolites:
        if metabolite[0] not in unique_metabolites_index:
            unique_metabolites_index.add(metabolite[0])
            unique_metabolites.append(metabolite)



    for i, metabolite in enumerate(unique_metabolites):
        metabolite_mapping_output_dict = {
            "id": i+1, 
            "mapping_id": model_id,
            "met_id": metabolite[0],
            "met_elements": f"{{{','.join(['C']*len(metabolite[2]))}}}", 
            "met_atompositions": f"{{{ ','.join([str(j) for j in range(len(metabolite[2]))])}}}",
            "met_symmetry_atompositions": "NULL",
            "used_": "True",
            "comment_": "NULL",
            "met_mapping": "NULL", 
            "base_met_ids": "NULL",	
            "base_met_elements": "NULL",
            "base_met_atompositions": "NULL",
            "base_met_symmetry_elements": "NULL", 
            "base_met_symmetry_atompositions": "NULL",
            "base_met_indices": "NULL",
        }

        metabolite_data.append(metabolite_mapping_output_dict)

    return pd.DataFrame(metabolite_data)

source_file = r'PATH/pputida_model.xlsx'
datafile = atom_mapping_metabolites_file_parser(source_file, 'my_model')
filename = r'PATH/pputida_metabolites_atom_mappings.csv'
datafile.to_csv(filename, index=False)
        
