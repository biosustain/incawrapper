import incawrapper.utils.merge_reversible_reactions as mrr
import pandas as pd

def test_Reaction_is_inverse():
    rxn_test = mrr.Reaction("G3P + B -> 3PG")
    assert rxn_test.is_inverse(mrr.Reaction("3PG -> G3P + B")) == True
    assert rxn_test.is_inverse(mrr.Reaction("3PG -> G3P + A")) == False 

def test_merge_reversible_reactions():
    df_in = pd.DataFrame(
        {
            "rxn_id": ["R1", "R2", "R3", "R4"],
            "rxn_eqn": ["G3P + B -> 3PG", "3PG -> G3P + B", "A -> B", "C -> D"],
        }
    )
    df_out = mrr.merge_reaverible_reaction(df_in)
    assert df_out.shape[0] == 3
    assert df_out.iloc[0]["rxn_eqn"] == "G3P + B <-> 3PG"