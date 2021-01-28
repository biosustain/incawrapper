import numpy as np
import pandas as pd
from pyopenms import FeatureMap, FeatureXMLFile


def extractNamesAndIntensities(feature_dir, sample_names, database):
    """
    This function takes .featureXML files, the output of SmartPeak
    pre-processing, and extracts the metabolite's reference and its measured
    intensity. Furthermore, the peptide references are compared with a
    database that has also been used for SmartPeak processing. Only
    metabolites that appear in the database are being used. Their formula is
    added to the output dataframe. The names of the files that should be
    processed are added via a SmartPeak sequence file

    Parameters
    ----------
    feature_dir: path
        the path to the directory holding the .featureXML files
    sample_names: string
        the extracted information from a sequence file
    database: pandas.DataFrame
        the organism specific database with the metabolite mapping

    Returns
    -------
    extracted_data_all: pandas.DataFrame
        a dataframe containing the extracted information,
        the 4 columns include the sample name, the peptide reference for
        the metabolites, their corresponding formulas and the measured
        intensity
    """
    metabolites_unique = database[0].unique()
    extracted_data_dict = {}
    cnt = 0
    for name in sample_names:
        features = FeatureMap()
        FeatureXMLFile().load(
            feature_dir + "/" + name + ".featureXML", features
        )
        for f in features:
            try:
                peptideRef = f.getMetaValue("PeptideRef").decode("utf-8")
            except AttributeError:
                peptideRef = f.getMetaValue("PeptideRef")
            if peptideRef in metabolites_unique:
                formula = database[database[0] == peptideRef][1]
                extracted_data_dict[cnt] = {
                    "sample_group_name": name,
                    "Metabolite": peptideRef,
                    "Formula": list(formula)[0],
                    "Intensity": f.getMetaValue("peak_apex_int"),
                }
                cnt = cnt + 1
    extracted_data_all = pd.DataFrame.from_dict(extracted_data_dict, "index")
    return extracted_data_all


def calculateMeanVarRSD(
    extracted_data_all, sample_name_2_replicate_groups, min_reps=3
):
    """
    The output of the extractNamesAndIntensities() function (or its output
    after normalization) is processed here to produce a dataframe that
    includes some basic statistics

    Parameters
    ----------
    extracted_data_all: pandas.DataFrame
        the output of the extractNamesAndIntensities()
        function (or its output after normalization)
    sample_name_2_replicate_groups: pandas.DataFrame
        the extracted information from a
        sequence file reduced to one entry per "sample_group_name"
    min_reps: int
        the number of replicates for each sample, corresponds to the
        file names (replicates should end with the replicate number)

    Returns
    -------
    stats_all_df: pandas.DataFrame
        a dataframe with some base statistics. The 6 columns
        include the sample group name, the metabolite reference, its
        formula and the mean, variance and relative stdev.
    """
    stats_all_dict = {}
    cnt = 0
    for replicate_group in sample_name_2_replicate_groups[
        "replicate_group_name"
    ].unique():
        list_of_compound_intensities = pd.DataFrame(
            columns=["Metabolite", "Formula", "Intensities"]
        )
        for sample_name_index, sample_name in sample_name_2_replicate_groups[
            sample_name_2_replicate_groups["replicate_group_name"]
            == replicate_group
        ].iterrows():
            for met_index, met in extracted_data_all[
                extracted_data_all["sample_group_name"]
                == sample_name["sample_group_name"]
            ].iterrows():
                list_of_compound_intensities = (
                    list_of_compound_intensities.append(
                        pd.DataFrame(
                            [
                                {
                                    "Metabolite": met["Metabolite"],
                                    "Formula": met["Formula"],
                                    "Intensities": met["Intensity"],
                                }
                            ]
                        ),
                        ignore_index=True,
                    )
                )
        for met_name in list_of_compound_intensities["Metabolite"].unique():
            intensities = list_of_compound_intensities[
                list_of_compound_intensities["Metabolite"] == met_name
            ]
            if len(intensities) >= min_reps:
                mean = np.mean(intensities["Intensities"])
                var = np.var(intensities["Intensities"])
                rsd = np.sqrt(var) / mean
                stats_all_dict[cnt] = {
                    "replicate_group_name": replicate_group,
                    "Metabolite": met_name,
                    "Formula": list(
                        list_of_compound_intensities[
                            list_of_compound_intensities["Metabolite"]
                            == met_name
                        ]["Formula"]
                    )[0],
                    "Mean": mean,
                    "Variance": var,
                    "RSD": rsd,
                }
                cnt = cnt + 1
    stats_all_df = pd.DataFrame.from_dict(stats_all_dict, "index")
    return stats_all_df
