import unittest
import pickle
import pathlib
import cobra
import pandas as pd
from BFAIR.mfa.sampling import (
    model_rxn_overlap,
    rxn_coverage,
    split_lumped_rxns,
    split_lumped_reverse_rxns,
    find_reverse_rxns,
    combine_split_rxns,
    cobra_add_split_rxns,
    add_constraints,
    add_feasible_constraints,
    find_biomass_reaction,
    get_min_solution_val,
    replace_biomass_rxn_name,
    bound_relaxation,
)

current_dir = str(pathlib.Path(__file__).parent.absolute())


class test_methods(unittest.TestCase):

    maxDiff = None

    # Create method to compare dataframes
    def assertDataframeEqual(self, a, b, msg):
        try:
            pd.testing.assert_frame_equal(a, b)
        except AssertionError as e:
            raise self.failureException(msg) from e

    # Create method to compare Series
    def assertSeriesEqual(self, a, b, msg):
        try:
            pd.testing.assert_series_equal(a, b)
        except AssertionError as e:
            raise self.failureException(msg) from e

    def setUp(self):
        file_obj = open(
            current_dir
            + "/test_data/MFA_sampling/sampling_test_data.obj",
            "rb",
        )
        (
            fittedFluxes,
            unconstraint_bounds,
            biomass_rxn,
            adj_fittedFluxes,
            coverage,
            lumped_rxns,
            overlap,
            fittedFluxes_split_temp,
            lumped_reverse_rxns,
            reverse_df,
            fittedFluxes_split,
            fittedFluxes_split_combined,
            rxns_to_split,
            model_preproces_bounds,
            constrained_bounds,
            min_val,
            adj_fittedFluxes,
            problems,
            feasible_constrained_bounds,
            cons_table,
            relaxed_bounds,
        ) = pickle.load(file_obj)
        file_obj.close()

        self.simulation_info = pd.read_csv(
            current_dir
            + "/test_data/MFA_modelInputsData/experimentalMS_data_I.csv"
        )
        self.simulation_id = "WTEColi_113C80_U13C20_01"
        self.model = cobra.io.load_json_model(
            current_dir + "/test_data/MFA_modelInputsData/iJO1366.json")
        self.constrained_model = add_constraints(
            self.model.copy(), adj_fittedFluxes
        )
        self.fittedFluxes = fittedFluxes
        self.unconstraint_bounds = unconstraint_bounds
        self.biomass_rxn = biomass_rxn
        self.adj_fittedFluxes = adj_fittedFluxes
        self.coverage = coverage
        self.lumped_rxns = lumped_rxns
        self.overlap = overlap
        self.fittedFluxes_split_temp = fittedFluxes_split_temp
        self.lumped_reverse_rxns = lumped_reverse_rxns
        self.reverse_df = reverse_df
        self.fittedFluxes_split = fittedFluxes_split
        self.fittedFluxes_split_combined = fittedFluxes_split_combined
        self.rxns_to_split = rxns_to_split
        self.model_preproces_bounds = model_preproces_bounds
        self.constrained_bounds = constrained_bounds
        self.min_val = min_val
        self.adj_fittedFluxes = adj_fittedFluxes
        self.problems = problems
        self.feasible_constrained_bounds = feasible_constrained_bounds
        self.cons_table = cons_table
        self.relaxed_bounds = relaxed_bounds

        # Add the method to compare dataframes in the class
        self.addTypeEqualityFunc(pd.DataFrame, self.assertDataframeEqual)
        self.addTypeEqualityFunc(pd.Series, self.assertSeriesEqual)

    @staticmethod
    def get_bounds_df(model):
        # Helper function to have a way to compare the bounds
        bounds_temp = {}
        # Round to 5 decimal places to avoid issues in very low values
        for cnt, rxn in enumerate(model.reactions):
            bounds_temp[cnt] = {
                "rxn_id": rxn.id,
                "lb": rxn.lower_bound,
                "ub": rxn.upper_bound,
            }
        return pd.DataFrame.from_dict(bounds_temp, "index")

    def test_model_rxn_overlap(self):
        overlap = self.overlap
        overlap_ = model_rxn_overlap(self.adj_fittedFluxes, self.model)
        self.assertEqual(overlap, overlap_)

    def test_rxn_coverage(self):
        coverage_ = rxn_coverage(self.adj_fittedFluxes, self.model)
        self.assertEqual(self.coverage, coverage_)

    def test_split_lumped_rxns(self):
        lumped_rxns = self.lumped_rxns
        # Check the example notebook for details
        lumped_ids = [1, 21, 26, 27, 53, 54, 67, 74, 82]
        mask = []
        overlap = model_rxn_overlap(self.adj_fittedFluxes, self.model)
        for i in overlap.iteritems():
            if i[0] in lumped_ids:
                mask.append(True)
            else:
                mask.append(False)
        lumped_rxns_ = model_rxn_overlap(
            self.adj_fittedFluxes, self.model)[mask]
        self.assertEqual(lumped_rxns, lumped_rxns_)
        fittedFluxes_split_temp_ = split_lumped_rxns(
            lumped_rxns_, self.adj_fittedFluxes)
        self.assertEqual(
            self.fittedFluxes_split_temp, fittedFluxes_split_temp_)

    def test_split_lumped_reverse_rxns(self):
        lumped_reverse_rxns = self.lumped_reverse_rxns
        lumped_reverse_ids = [2, 28, 55, 68]
        mask_reverse = []
        for i in model_rxn_overlap(
                self.fittedFluxes_split_temp, self.model).iteritems():
            if i[0] in lumped_reverse_ids:
                mask_reverse.append(True)
            else:
                mask_reverse.append(False)
        lumped_reverse_rxns_ = model_rxn_overlap(
            self.fittedFluxes_split_temp, self.model)[mask_reverse]
        self.assertEqual(lumped_reverse_rxns, lumped_reverse_rxns_)
        fittedFluxes_split_ = split_lumped_reverse_rxns(
            lumped_reverse_rxns_, self.fittedFluxes_split_temp)
        self.assertEqual(self.fittedFluxes_split, fittedFluxes_split_)

    def test_find_reverse_rxns(self):
        reverse_df_ = find_reverse_rxns(self.fittedFluxes_split)
        self.assertEqual(self.reverse_df, reverse_df_)

    def test_combine_split_rxns(self):
        # Check the example notebook for details
        lumped_ids = [1, 21, 26, 27, 53, 54, 67, 74, 82]
        mask = []
        overlap = model_rxn_overlap(self.adj_fittedFluxes, self.model)
        for i in overlap.iteritems():
            if i[0] in lumped_ids:
                mask.append(True)
            else:
                mask.append(False)
        lumped_rxns = model_rxn_overlap(
            self.adj_fittedFluxes, self.model)[mask]
        fittedFluxes_split_temp = split_lumped_rxns(
            lumped_rxns, self.adj_fittedFluxes)
        lumped_reverse_ids = [2, 28, 55, 68]
        mask_reverse = []
        for i in model_rxn_overlap(
                fittedFluxes_split_temp, self.model).iteritems():
            if i[0] in lumped_reverse_ids:
                mask_reverse.append(True)
            else:
                mask_reverse.append(False)
        lumped_reverse_rxns = model_rxn_overlap(
            fittedFluxes_split_temp, self.model)[mask_reverse]
        fittedFluxes_split_ = split_lumped_reverse_rxns(
            lumped_reverse_rxns, fittedFluxes_split_temp)
        fittedFluxes_split_combined_, rxns_to_split_ = combine_split_rxns(
            fittedFluxes_split_)
        self.assertEqual(self.fittedFluxes_split_combined, fittedFluxes_split_combined_)
        self.assertEqual(self.rxns_to_split, rxns_to_split_)

    def test_cobra_add_split_rxns(self):
        model_split = self.model.copy()
        cobra_add_split_rxns(self.rxns_to_split, model_split)
        model_preproces_bounds_ = self.get_bounds_df(model_split)
        self.assertEqual(self.model_preproces_bounds, model_preproces_bounds_)

    def test_add_constraints(self):
        unconstraint_bounds = self.unconstraint_bounds
        constrained_bounds = self.constrained_bounds
        constrained_model = add_constraints(
            self.model.copy(),
            self.adj_fittedFluxes,
        )
        constrained_bounds_ = self.get_bounds_df(constrained_model)
        self.assertFalse(unconstraint_bounds.equals(constrained_bounds_))
        self.assertEqual(constrained_bounds, constrained_bounds_)

    def test_find_biomass_reaction(self):
        biomass_reaction_ids = find_biomass_reaction(
            self.constrained_model,
            biomass_string=["Biomass", "BIOMASS", "biomass"],
        )
        # This one basically just checks if there is an output
        self.assertIsInstance(biomass_reaction_ids, list)
        # This one makes sure that the output list contains a reaction name
        self.assertIsInstance(biomass_reaction_ids[0], str)

    def test_get_min_solution_val(self):
        # Find in fittedFluxes
        fittedFluxes = self.fittedFluxes
        min_val = self.min_val
        min_val_ = get_min_solution_val(
            fittedFluxes, biomass_string="Biomass"
        )
        self.assertEqual(min_val, min_val_)
        # Do not find in fake example (=0)
        fauxfittedFluxes = self.fittedFluxes
        fauxfittedFluxes.at[11, "rxn_id"] = "Removed_ID"
        no_BM_val = get_min_solution_val(
            fauxfittedFluxes, biomass_string="Biomass"
        )
        self.assertEqual(no_BM_val, 0)

    def test_replace_biomass_rxn_name(self):
        # Replace in fittedFluxes
        adj_fittedFluxes = self.adj_fittedFluxes
        adj_fittedFluxes_ = replace_biomass_rxn_name(
            self.fittedFluxes,
            biomass_rxn_name="BIOMASS_Ec_iJO1366_core_53p95M",
            biomass_string="Biomass",
        )
        self.assertEqual(adj_fittedFluxes, adj_fittedFluxes_)
        # Replace in a fake sample
        test_df = pd.DataFrame({"rxn_id": "Biomass"}, index=[0])
        test_df_replaced = replace_biomass_rxn_name(
            test_df, biomass_string="Biomass", biomass_rxn_name="It works!"
        )
        self.assertEqual(test_df_replaced["rxn_id"][0], "It works!")

    def test_add_feasible_constraints(self):
        problems = self.problems
        unconstraint_bounds = self.unconstraint_bounds
        feasible_constrained_bounds = self.feasible_constrained_bounds
        feasible_constrained_model, problems_ = add_feasible_constraints(
            self.model.copy(),
            self.adj_fittedFluxes,
            min_val=self.min_val,
        )
        feasible_constrained_bounds_ = self.get_bounds_df(
            feasible_constrained_model
        )
        self.assertEqual(problems, problems_)
        self.assertFalse(unconstraint_bounds.equals(
            feasible_constrained_bounds_))
        self.assertEqual(
            feasible_constrained_bounds, feasible_constrained_bounds_
        )

    def test_bound_relaxation(self):
        try:
            # regular test
            cons_table = self.cons_table
            cons_table_ = bound_relaxation(
                self.constrained_model.copy(),
                self.adj_fittedFluxes,
                destructive=True,
                fluxes_to_ignore=[],
            )
            self.assertEqual(cons_table, cons_table_)
        except Exception as exception:
            # Exception if can't find Gurobi
            self.assertIsInstance(exception, ModuleNotFoundError)
            self.assertEqual(str(exception), "Requires Gurobi solver.")


if __name__ == "__main__":
    unittest.main()
