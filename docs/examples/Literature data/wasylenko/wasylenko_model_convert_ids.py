import pandas as pd
import warnings
import re
import pathlib

MODEL_FILE_PATH = pathlib.Path(__file__).parent.resolve() / "wasylenko_model.txt"
ID_MAP_FILE_PATH = (
    pathlib.Path(__file__).parent.resolve() / "wasylenko_metabolite_id_map.csv"
)
OUTPUT_FILE = pathlib.Path(__file__).parent.resolve() / "wasylenko_model_KEGG.csv"


def replace_metabolite_ids_in_reaction(
    reaction_string: str,
    id_map: dict,
) -> str:
    """Replace metabolite ids in a reaction string."""
    for key, value in id_map.items():
        if pd.isna(value) or value == "nan":
            warnings.warn("No id for {}, original ID kept.".format(key))
            continue
        print(key)
        reaction_string = re.sub(
            r"\b{}\b".format(key), value, reaction_string
        )  # replace the metabolite id
    return reaction_string


def main():
    model_original_ids = pd.read_table(MODEL_FILE_PATH, index_col=None, header=None)
    id_maps = pd.read_csv(ID_MAP_FILE_PATH, index_col=0, sep=";")
    model_new_ids = pd.Series()
    for idx, val in model_original_ids.iterrows():
        model_new_ids[idx] = replace_metabolite_ids_in_reaction(
            reaction_string=val[0], id_map=id_maps.to_dict()["Kegg"]
        )
    model_new_ids.to_csv(OUTPUT_FILE)


if __name__ == "__main__":
    main()
