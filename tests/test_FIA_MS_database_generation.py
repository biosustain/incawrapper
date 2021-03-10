import unittest
import pandas as pd
import pickle
import pathlib
import os
import shutil
from BFAIR.FIA_MS.database_construction import (
    print_formula,
    zero_charge,
    is_valid,
    make_struct,
    make_mapping,
    store_struct,
    store_mapping,
    import_mapping_tsv,
    create_database,
)

current_dir = str(pathlib.Path(__file__).parent.absolute())


class test_methods(unittest.TestCase):

    # Create method to compare dataframes
    def assertDataframeEqual(self, a, b, msg):
        try:
            pd.testing.assert_frame_equal(a, b)
        except AssertionError as e:
            raise self.failureException(msg) from e

    def setUp(self):
        file_obj = open(
            current_dir
            + "/test_data/FIA_MS_Data/database_files/unittest_data/test_data.obj",  # noqa E501
            "rb",
        )
        (
            elements,
            formula_print,
            metabolite,
            formula_zero_charge,
            formulas,
            ids,
            df_formulas,
            df_mapping,
            metabolites,
            store_struct_file,
            store_mapping_file1,
            store_mapping_file2,
            create_database_struct_file,
            create_database_mapping_file1,
            create_database_mapping_file2,
        ) = pickle.load(file_obj)
        file_obj.close()

        self.elements = elements
        self.formula_print = formula_print
        self.metabolite = metabolite
        self.formula_zero_charge = formula_zero_charge
        self.formulas = formulas
        self.ids = ids
        self.df_formulas = df_formulas
        self.df_mapping = df_mapping
        self.metabolites = metabolites
        self.store_struct_file = store_struct_file
        self.store_mapping_file1 = store_mapping_file1
        self.store_mapping_file2 = store_mapping_file2
        self.create_database_struct_file = create_database_struct_file
        self.create_database_mapping_file1 = create_database_mapping_file1
        self.create_database_mapping_file2 = create_database_mapping_file2

        # Add the method to compare dataframes in the class
        self.addTypeEqualityFunc(pd.DataFrame, self.assertDataframeEqual)

    def test_print_formula(self):
        formula_print = self.formula_print
        elements = self.elements
        formula_print_ = print_formula(elements)
        self.assertEqual(formula_print, formula_print_)

    def test_zero_charge(self):
        formula_zero_charge = self.formula_zero_charge
        metabolite = self.metabolite
        formula_zero_charge_ = zero_charge(metabolite)
        self.assertEqual(formula_zero_charge.elements,
                         formula_zero_charge_.elements)

    def test_is_valid(self):
        v_met = self.metabolites[87]
        valid_metabolite = is_valid(v_met)
        nof_met = self.metabolites[42]
        noformula_metabolite = is_valid(nof_met)
        inv_met = self.metabolites[45]
        invalid_metabolite = is_valid(inv_met)
        self.assertTrue(valid_metabolite)
        self.assertFalse(noformula_metabolite)
        self.assertFalse(invalid_metabolite)

    def test_make_struct(self):
        df_formulas = self.df_formulas
        formulas = self.formulas
        ids = self.ids
        df_formulas_ = make_struct(formulas, ids)
        self.assertEqual(df_formulas, df_formulas_)

    def test_make_mapping(self):
        df_mapping = self.df_mapping
        df_formulas = self.df_formulas
        df_mapping_ = make_mapping(df_formulas)
        self.assertEqual(df_mapping, df_mapping_)

    def test_store_struct(self):
        store_struct_file = self.store_struct_file
        df_formulas = self.df_formulas
        os.makedirs(current_dir + "/temporary_files")
        store_struct(
            df_formulas,
            "test_store_struct",
            current_dir + "/temporary_files",
        )
        store_struct_file_ = pd.read_csv(
            current_dir + "/temporary_files/test_store_struct_struct.tsv",
            sep="\t",
            header=None,
        )
        shutil.rmtree(current_dir + "/temporary_files")
        self.assertEqual(store_struct_file, store_struct_file_)

    def test_store_mapping(self):
        store_mapping_file1 = self.store_mapping_file1
        store_mapping_file2 = self.store_mapping_file2
        df_mapping = self.df_mapping
        os.makedirs(current_dir + "/temporary_files")
        store_mapping(
            df_mapping,
            "test_store_mapping",
            current_dir + "/temporary_files",
        )
        store_mapping_file1_ = import_mapping_tsv(
            current_dir + "/temporary_files/test_store_mapping_mapping.tsv"
        )
        store_mapping_file2_ = import_mapping_tsv(
            current_dir + "/temporary_files/test_store_mapping_mapping_csv.tsv"
        )
        shutil.rmtree(current_dir + "/temporary_files")
        self.assertEqual(store_mapping_file1, store_mapping_file1_)
        self.assertEqual(store_mapping_file2, store_mapping_file2_)

    def test_create_database(self):
        create_database_struct_file = self.create_database_struct_file
        create_database_mapping_file1 = self.create_database_mapping_file1
        create_database_mapping_file2 = self.create_database_mapping_file2
        metabolites = self.metabolites
        os.makedirs(current_dir + "/temporary_files")
        create_database(
            metabolites,
            "test_create_database",
            current_dir + "/temporary_files",
        )
        create_database_struct_file_ = pd.read_csv(
            current_dir + "/temporary_files/test_create_database_struct.tsv",
            sep="\t",
            header=None,
        )
        create_database_mapping_file1_ = import_mapping_tsv(
            current_dir + "/temporary_files/test_create_database_mapping.tsv"
        )
        create_database_mapping_file2_ = import_mapping_tsv(
            current_dir
            + "/temporary_files/test_create_database_mapping_csv.tsv"
        )
        shutil.rmtree(current_dir + "/temporary_files")
        self.assertEqual(
            create_database_struct_file, create_database_struct_file_
        )
        self.assertEqual(
            create_database_mapping_file1, create_database_mapping_file1_
        )
        self.assertEqual(
            create_database_mapping_file2, create_database_mapping_file2_
        )


if __name__ == "__main__":
    unittest.main()
