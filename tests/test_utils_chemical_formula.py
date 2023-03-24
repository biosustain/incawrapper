import pytest
import incawrapper.utils.chemical_formula as chemical_formula


def test_create_compound_dict_creates_correct_dict():
    formula = "C6H12O6"
    compound_dict = chemical_formula._create_compound_dict(formula)
    assert compound_dict == {"C": 6, "H": 12, "O": 6}


def test_create_compound_dict_no_stoichiometric_coefficient():
    formula = "C6HO6"
    compound_dict = chemical_formula._create_compound_dict(formula)
    assert compound_dict == {"C": 6, "H": 1, "O": 6}


def test_create_forumla_from_dict():
    formula_dict = {"C": 6, "H": 1, "O": 6}
    formula = chemical_formula.create_formula_from_dict(formula_dict)
    assert formula == "C6HO6"


def test_subtract_formula_subtracts_one_element():
    formula = "C6H12O6"
    subtract_formula = "C3H6O3"
    new_formula = chemical_formula.subtract_formula(formula, subtract_formula)
    assert new_formula == "C3H6O3"


def test_subtract_formula_subtracts_multiple_elements():
    formula = "C6H12O6"
    subtract_formula = "C3H6O3"
    new_formula = chemical_formula.subtract_formula(formula, subtract_formula)
    assert new_formula == "C3H6O3"


def test_subtract_formula_subtracts_non_present_element():
    formula = "C6H12O6"
    subtract_formula = "C3H6O3Si"

    with pytest.raises(ValueError):
        chemical_formula.subtract_formula(formula, subtract_formula)
