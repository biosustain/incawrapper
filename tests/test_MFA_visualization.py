import unittest
import pickle
import pathlib
import cobra
import matplotlib
import pandas as pd
from BFAIR.mfa.visualization import (
    reshape_fluxes_escher,
    sampled_fluxes_minrange,
    show_reactions,
    plot_sampled_reaction_fluxes,
    plot_all_subsystem_fluxes,
    get_subsytem_reactions,
    show_subsystems,
    plot_subsystem_fluxes,
)
from BFAIR.mfa.visualization.distributions import (
    _sampled_reaction_fit
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

    def setUp(self):
        file_obj = open(
            current_dir
            + "/test_data/MFA_sampling/visualization_test_data.obj",
            "rb",
        )
        (
            solution,
            relaxed_sampled_fluxes,
            fluxes_relaxed,
            relaxed_fluxes_sampling,
            reduced_relaxed_sampled_fluxes,
            reactions,
            subsystems,
            reactions_indeces,
            subsystems_indices,
        ) = pickle.load(file_obj)
        file_obj.close()

        self.model = cobra.io.load_json_model(
            current_dir + "/test_data/MFA_modelInputsData/iJO1366.json")
        self.solution = solution
        self.relaxed_sampled_fluxes = relaxed_sampled_fluxes
        self.fluxes_relaxed = fluxes_relaxed
        self.relaxed_fluxes_sampling = relaxed_fluxes_sampling
        self.reduced_relaxed_sampled_fluxes = reduced_relaxed_sampled_fluxes
        self.reactions = reactions
        self.subsystems = subsystems
        self.reactions_indeces = reactions_indeces
        self.subsystems_indices = subsystems_indices

        # Add the method to compare dataframes in the class
        self.addTypeEqualityFunc(pd.DataFrame, self.assertDataframeEqual)

    def test_reshape_fluxes_escher(self):
        fluxes_relaxed_ = reshape_fluxes_escher(self.solution)
        self.assertEqual(self.fluxes_relaxed, fluxes_relaxed_)
        relaxed_fluxes_sampling_ = reshape_fluxes_escher(
            self.relaxed_sampled_fluxes)
        self.assertEqual(
            self.relaxed_fluxes_sampling, relaxed_fluxes_sampling_)

    def test_sampled_fluxes_minrange(self):
        reduced_relaxed_sampled_fluxes_ = sampled_fluxes_minrange(
            self.relaxed_sampled_fluxes, min_val=-1, max_val=1)
        self.assertEqual(
            self.reduced_relaxed_sampled_fluxes,
            reduced_relaxed_sampled_fluxes_)

    def test_show_reactions(self):
        reactions, _ = get_subsytem_reactions(self.model, 14)
        reactions_indeces_ = show_reactions(reactions)
        self.assertEqual(self.reactions_indeces, reactions_indeces_)

    def test_plot_sampled_reaction_fluxes(self):
        # Also test helper function
        sampled_reaction_fluxes_plot_norm = plot_sampled_reaction_fluxes(
            self.relaxed_sampled_fluxes, self.reactions, reaction_id=2)
        sampled_values = self.relaxed_sampled_fluxes[self.reactions[2]]
        _, _, norm_dist_true = _sampled_reaction_fit(
            sampled_values, alpha=1e-3)
        sampled_reaction_fluxes_plot_not_norm = plot_sampled_reaction_fluxes(
            self.relaxed_sampled_fluxes, self.reactions, reaction_id=0)
        sampled_values = self.relaxed_sampled_fluxes[
            self.reactions[0]]
        _, _, norm_dist_false = _sampled_reaction_fit(
            sampled_values, alpha=1e-3)
        self.assertIsInstance(
            sampled_reaction_fluxes_plot_norm[0], matplotlib.lines.Line2D)
        self.assertTrue(norm_dist_true)
        self.assertIsInstance(
            sampled_reaction_fluxes_plot_not_norm[0], matplotlib.lines.Line2D)
        self.assertFalse(norm_dist_false)

    def test_plot_all_subsystem_fluxes(self):
        all_subsystem_fluxes_plot = plot_all_subsystem_fluxes(
            self.relaxed_sampled_fluxes, self.reactions, bins=10)
        self.assertIsInstance(
            all_subsystem_fluxes_plot, matplotlib.figure.Figure)

    def test_get_subsytem_reactions(self):
        reactions_, subsystems_ = get_subsytem_reactions(self.model, 14)
        self.assertEqual(self.reactions, reactions_)
        self.assertEqual(self.subsystems, subsystems_)

    def test_show_subsystems(self):
        subsystems_indices_ = show_subsystems(self.model)
        self.assertEqual(self.subsystems_indices, subsystems_indices_)

    def test_plot_subsystem_fluxes(self):
        subsystem_fluxes_plot = plot_subsystem_fluxes(
            self.model,
            self.reduced_relaxed_sampled_fluxes,
            subsystem_id=14,
            no_zero_cols=True)
        self.assertIsInstance(
            subsystem_fluxes_plot, matplotlib.figure.SubplotBase)


if __name__ == "__main__":
    unittest.main()
