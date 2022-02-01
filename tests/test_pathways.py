import unittest
from pathlib import Path

import pandas as pd

from BFAIR.pathways import RuleLibrary
from BFAIR.pathways import utils
from BFAIR.pathways.rules import q


class TestRuleLibrary(unittest.TestCase):
    EXPECTED_RULES = 174
    EXPECTED_RULES_16_DIAMETER = 23
    EXPECTED_RULES_SMALL_ECOLI = 166
    EXPECTED_RULES_THEOBROMINE = 8
    EXPECTED_RULES_UNCERTAINTY = 39
    CAFFEINE_SYNTHASE_REACTION_ID = "MNXR111503"
    CAFFEINE_SYNTHASE_RULE_ID = "RR-02-c9bb498ec42daefa-16-F"

    @classmethod
    def setUpClass(cls):
        cls.rules = RuleLibrary(Path(__file__).parent / "test_data" / "rules_test.db")

    @classmethod
    def tearDownClass(cls):
        cls.rules.close()

    def tearDown(self):
        self.rules.reset()

    def test_rules(self):
        actual_rules = self.rules.available
        self.assertIsInstance(actual_rules, pd.DataFrame)
        self.assertTupleEqual(actual_rules.shape, (self.EXPECTED_RULES, 2))
        self.assertEqual(actual_rules.index.name, "rule_id")
        self.assertTupleEqual(tuple(actual_rules.columns), ("reaction_id", "smarts"))

    def test_pop_filter(self):
        self.rules.filter_by_diameter(16)
        self.rules.filter_by_uncertainty(0.5)
        self.assertEqual(len(self.rules._filters), 2)
        # Test that filter at position 0 (diameter) is removed
        self.rules.pop_filter(0)
        self.assertEqual(len(self.rules._filters), 1)
        self.assertEqual(str(self.rules._filters[0]), '"score">=0.5')
        # Test that no filters are left
        self.rules.pop_filter()
        self.assertEqual(len(self.rules._filters), 0)

    def test_unsupported_diameter(self):
        for diameter in range(1, 16, 2):
            with self.assertRaisesRegex(ValueError, "^Unsupported diameter.*$"):
                self.rules.filter_by_diameter(diameter)

    def test_filter_by_diameter(self):
        self.rules.filter_by_diameter(16)
        self.assertEqual(len(self.rules), self.EXPECTED_RULES_16_DIAMETER)

    def test_filter_by_organism(self):
        self.rules.filter_by_organism("small_ecoli")
        self.assertEqual(len(self.rules), self.EXPECTED_RULES_SMALL_ECOLI)

    def test_filter_by_compound(self):
        self.rules.filter_by_compound(TestUtils.THEOBROMINE_INCHI)
        self.assertEqual(len(self.rules), self.EXPECTED_RULES_THEOBROMINE)

    def test_filter_by_uncertainty(self):
        self.rules.filter_by_uncertainty(0.5)
        self.assertEqual(len(self.rules), self.EXPECTED_RULES_UNCERTAINTY)

    def test_list_products(self):
        # Test caffeine synthase produces caffeine from theobromine
        self.rules._filters.append(q.rules.rule_id == self.CAFFEINE_SYNTHASE_RULE_ID)
        actual_products = self.rules.list_products(TestUtils.THEOBROMINE_INCHI)
        expected_products = {
            TestUtils.CAFFEINE_INCHI: [(self.CAFFEINE_SYNTHASE_RULE_ID, self.CAFFEINE_SYNTHASE_REACTION_ID)]
        }
        self.assertDictEqual(actual_products, expected_products)


class TestUtils(unittest.TestCase):
    THEOBROMINE_INCHI = "InChI=1S/C7H8N4O2/c1-10-3-8-5-4(10)6(12)9-7(13)11(5)2/h3H,1-2H3,(H,9,12,13)"
    THEOBROMINE_SMILES = "Cn1cnc2c1c(=O)[nH]c(=O)n2C"
    THEOBROMINE_FINGERPRINT = [
        106,
        114,
        213,
        235,
        303,
        312,
        314,
        340,
        353,
        356,
        378,
        395,
        401,
        416,
        442,
        453,
        482,
        507,
        548,
        628,
        650,
        664,
        672,
        695,
        720,
        831,
        863,
        899,
        906,
        935,
        1019,
    ]
    CAFFEINE_INCHI = "InChI=1S/C8H10N4O2/c1-10-4-9-6-5(10)7(13)12(3)8(14)11(6)2/h4H,1-3H3"

    @classmethod
    def setUpClass(cls):
        cls.theobromine_fp_from_inchi = utils.get_molecular_fingerprint(cls.THEOBROMINE_INCHI)
        cls.theobromine_fp_from_smiles = utils.get_molecular_fingerprint(cls.THEOBROMINE_SMILES, "smiles")

    def test_unsupported_depiction(self):
        with self.assertRaisesRegex(ValueError, "^Unsupported input type.*$"):
            utils.get_compound(self.THEOBROMINE_SMILES, "smarts")

    def test_fingerprints(self):
        self.assertIsInstance(self.theobromine_fp_from_inchi, list)
        self.assertListEqual(self.theobromine_fp_from_inchi, self.THEOBROMINE_FINGERPRINT)
        self.assertIsInstance(self.theobromine_fp_from_smiles, list)
        self.assertListEqual(self.theobromine_fp_from_smiles, self.THEOBROMINE_FINGERPRINT)

    def test_calculate_similarity(self):
        # Test two identical compounds
        actual_sim = utils.calculate_similarity(self.theobromine_fp_from_inchi, self.theobromine_fp_from_smiles)
        self.assertEqual(actual_sim, 1.0)
        # Test two different compounds
        caffeine_fp = utils.get_molecular_fingerprint(self.CAFFEINE_INCHI)
        actual_sim = utils.calculate_similarity(self.theobromine_fp_from_inchi, caffeine_fp)
        self.assertAlmostEqual(actual_sim, 0.5263157894736842)
