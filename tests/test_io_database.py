import pickle
import unittest
from pathlib import Path
from unittest import mock

import pandas as pd

from BFAIR.io import struct, mapping


TEST_DATA_DIR = Path(__file__).parent / "test_data"


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(TEST_DATA_DIR / "database_test.pickle", "rb") as file:
            (
                cls.expected_mapping,
                cls.expected_struct,
                cls.expected_merged_mapping,
                cls.expected_struct_from_inchis,
                cls.expected_struct_from_products_dict,
                cls.expected_struct_renamed
            ) = pickle.load(file)

    def test_mapping_from_struct(self):
        actual_mapping = mapping.from_struct(self.expected_struct, "ecoli_core", "NA")
        pd.testing.assert_frame_equal(actual_mapping, self.expected_mapping)

    def test_mapping_merge(self):
        struct_a = struct.from_inchis(pd.DataFrame({
            "inchi": [
                "InChI=1S/C8H10N4O2/c1-10-4-9-6-5(10)7(13)12(3)8(14)11(6)2/h4H,1-3H3",
                "InChI=1S/C7H8N4O2/c1-10-3-8-5-4(10)6(12)9-7(13)11(5)2/h3H,1-2H3,(H,9,12,13)"
            ]
        }, index=["caffeine", "theobromine"]))
        struct_b = struct.from_inchis(pd.DataFrame({
            "inchi": [
                "InChI=1S/C7H8N4O2/c1-10-3-8-5-4(10)6(12)11(2)7(13)9-5/h3H,1-2H3,(H,9,13)"
            ]
        }, index=["paraxanthine"]))
        pd.testing.assert_frame_equal(
            mapping.merge(mapping.from_struct(struct_a), mapping.from_struct(struct_b)),
            self.expected_merged_mapping
        )

    def test_mapping_read(self):
        actual_mapping = mapping.read(TEST_DATA_DIR / "mapping_test.tsv")
        pd.testing.assert_frame_equal(actual_mapping, self.expected_mapping)

    def test_mapping_write(self):
        with mock.patch("builtins.open", mock.mock_open(), create=True) as mock_open:
            mapping.write(self.expected_mapping, "test.tsv")
        mock_open.assert_called_with("test.tsv", "w", newline="", encoding="utf-8")
        calls = [
            mock.call(f"database_name\t{self.expected_mapping.attrs['database_name']}\r\n"),
            mock.call(f"database_version\t{self.expected_mapping.attrs['database_version']}\r\n"),
        ]
        calls.extend([
            mock.call("\t".join([str(row[0]), row[1], *row[2]]) + "\r\n")
            for row in self.expected_mapping.itertuples(index=False, name=None)
        ])
        mock_open.return_value.write.assert_has_calls(calls)

    def test_mapping_write_exceptions(self):
        with self.assertRaisesRegex(ValueError, r"Attribute '\w+' missing."):
            with mock.patch("builtins.open", mock.mock_open(), create=True) as mock_open:
                mapping.write(self.expected_merged_mapping, "test.tsv", None, None)
        mock_open.assert_not_called()

    def test_struct_from_inchis(self):
        data = pd.DataFrame({
            "inchi": [
                "InChI=1S/C8H10N4O2/c1-10-4-9-6-5(10)7(13)12(3)8(14)11(6)2/h4H,1-3H3",
                "InChI=1S/C7H8N4O2/c1-10-3-8-5-4(10)6(12)9-7(13)11(5)2/h3H,1-2H3,(H,9,12,13)",
                "InChI=1S/C7H8N4O2/c1-10-3-8-5-4(10)6(12)11(2)7(13)9-5/h3H,1-2H3,(H,9,13)"
            ]
        }, index=["caffeine", "theobromine", "paraxanthine"])
        actual_struct = struct.from_inchis(data)
        pd.testing.assert_frame_equal(actual_struct, self.expected_struct_from_inchis)

    def test_struct_from_products_dict(self):
        products = {
            "theobromine": {
                "InChI=1S/C7H8N4O2/c1-10-3-8-5-4(10)6(12)9-7(13)11(5)2/h3H,1-2H3,(H,9,12,13)":
                    ("RR-02-c9bb498ec42daefa-16-F", "MNXR111503")
            }
        }
        actual_struct = struct.from_products_dict(products)
        pd.testing.assert_frame_equal(actual_struct, self.expected_struct_from_products_dict)

    def test_struct_merge(self):
        struct_a = struct.from_inchis(pd.DataFrame({
            "inchi": [
                "InChI=1S/C8H10N4O2/c1-10-4-9-6-5(10)7(13)12(3)8(14)11(6)2/h4H,1-3H3",
                "InChI=1S/C7H8N4O2/c1-10-3-8-5-4(10)6(12)9-7(13)11(5)2/h3H,1-2H3,(H,9,12,13)"
            ]
        }, index=["caffeine", "theobromine"]))
        struct_b = struct.from_inchis(pd.DataFrame({
            "inchi": [
                "InChI=1S/C7H8N4O2/c1-10-3-8-5-4(10)6(12)11(2)7(13)9-5/h3H,1-2H3,(H,9,13)"
            ]
        }, index=["paraxanthine"]))
        pd.testing.assert_frame_equal(
            struct.merge(struct_a, struct_b).drop_duplicates(),
            self.expected_struct_from_inchis
        )

    def test_struct_read(self):
        actual_struct = struct.read(TEST_DATA_DIR / "struct_test.tsv")
        pd.testing.assert_frame_equal(actual_struct, self.expected_struct)

    def test_struct_rename_metabolites(self):
        actual_struct = self.expected_struct_from_products_dict.copy()
        struct.rename_metabolites(actual_struct)
        pd.testing.assert_frame_equal(actual_struct, self.expected_struct_renamed)

    def test_struct_write(self):
        with mock.patch.object(self.expected_struct, "to_csv", mock.Mock()) as mock_fun:
            struct.write(self.expected_struct, "test.tsv")
        mock_fun.assert_called_once_with("test.tsv", header=None, index=None, sep="\t")
