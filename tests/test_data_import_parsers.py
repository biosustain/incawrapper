from incawrapper.parsers.data_import_parsers import combine_duplicated_compounds

def test_combine_duplicated_compounds():
    '''Test with one duplicated compound'''
    reactants_in = [('r5p', 1.0, 'defgh'), ('pep', 1.0, 'ijk'), ('pep', 1.0, 'pqr'), ('gln__L', 1.0, 'stuvw')]
    reactants_out = [('r5p', 1.0, None), ('pep', 2.0, None), ('gln__L', 1.0, None)]

    assert combine_duplicated_compounds(reactants_in) == reactants_out, "combine_duplicated_compounds() fails duplicated compounds test"

def test_combine_duplicated_compounds_triplicate():
    '''Test with one triplicated compound'''
    reactants_in = [('r5p', 1.0, 'defgh'), ('tri', 1.0, 'yzx'), ('tri', 1.0, 'ijk'), ('tri', 1.0, 'pqr'), ('gln__L', 1.0, 'stuvw')]
    reactants_out = [('r5p', 1.0, None), ('tri', 3.0, None), ('gln__L', 1.0, None)]

    assert combine_duplicated_compounds(reactants_in) == reactants_out, "combine_duplicated_compounds() fails with triplicated compounds test"

def test_combine_duplicated_compounds_no_duplicates():
    '''Test with no duplicated compounds'''
    reactants_in = [('r5p', 1.0, 'defgh'), ('tri', 1.0, 'yzx'), ('gln__L', 1.0, 'stuvw')]
    reactants_out = [('r5p', 1.0, None), ('tri', 1.0, None), ('gln__L', 1.0, None)]

    assert combine_duplicated_compounds(reactants_in) == reactants_out, "combine_duplicated_compounds() fails with no duplicated compounds test"