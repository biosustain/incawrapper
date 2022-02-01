import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pyopenms import FeatureMap, FeatureXMLFile
from scipy.stats import linregress

__version__ = "0.0.1"


def get_filename(row):
    """
    Assembles the name of the feature file.

    Parameters
    ----------
    row : pandas.Series
        A row fom the sequence dataframe. Must have the following index values:
        "sample_name", "inj_number", "batch_name", "acquisition_date_and_time".

    Returns
    -------
    filename : str
        The filename of the feature file.
    """
    acquisition = row.acquisition_date_and_time
    if pd.isna(acquisition):
        acquisition = "1900-01-01_000000"
    filename = (
        "_".join(
            [
                str(row.sample_name),
                str(row.inj_number),
                str(row.batch_name),
                acquisition,
            ]
        )
        + ".featureXML"
    )
    return filename


def extract_concentrations(df_sequence, feature_dir, dil=1):
    """
    Takes a sequence dataframe and extracts the metabolite concentrations of
    each sample from the associated feature files.

    Parameters
    ----------
    df_sequence : pandas.DataFrame
        Dataframe obtained from the HPLC sequence file. Must have the
        following index values: "sample_name", "inj_number", "batch_name",
        "acquisition_date_and_time".
    feature_dir : path
        Path of the feature files
    dil : int
        Dilution factor, in case the samples have been diltued prior to
        measurement.

    Returns
    -------
    df_concentrations : pandas.DataFrame
        Dataframe with information about the sample name, metabolite and the
        metabolite concentration in g/L.

    Raises
    ------
    RuntimeError
        If the feature file can not be found.
    ValueError
        If the "concentration_units" for an metabolite in the feature file is
        not "g/L".
    """
    if not feature_dir.endswith("/"):
        feature_dir += "/"

    dict_concentrations = {}
    cnt = 0

    for index, row in df_sequence.iterrows():
        # Open the feature file
        filename = get_filename(row)
        features = FeatureMap()
        try:
            FeatureXMLFile().load(feature_dir + filename, features)
        except RuntimeError as error:
            print("Error:", error)
            continue
        for f in features:
            # Get metabolite name
            try:
                metabolite = f.getMetaValue("PeptideRef").decode("utf-8")
            except AttributeError:
                metabolite = f.getMetaValue("PeptideRef")
            # Get metabolite concentration
            concentration = f.getSubordinates()[0].getMetaValue(
                "calculated_concentration"
            )
            if concentration is not None:
                # Check that the concentration unit is g/L
                try:
                    unit = (
                        f.getSubordinates()[0]
                        .getMetaValue("concentration_units")
                        .decode("utf-8")
                    )
                except AttributeError:
                    unit = f.getSubordinates()[0].getMetaValue(
                        "concentration_units"
                    )
                if unit != "g/L":
                    raise ValueError(
                        "Unit has to be g/L. File {}: Unit of {} is {}".format(
                            filename, metabolite, unit
                        )
                    )

                # Add the concentration to the dict
                dict_concentrations[cnt] = {
                    "sample_name_original": row.sample_name_original,
                    "samplename_HPLC": row.sample_name,
                    "metabolite": metabolite,
                    "conc[g/L]": concentration * dil,
                }
                cnt = cnt + 1

    # Create a dataframe from the dict
    df_concentrations = pd.DataFrame.from_dict(dict_concentrations, "index")
    return df_concentrations


def extract_OD600(df_DataSeries):
    """
    Extracts the last OD600 measurement for each sample.

    Parameters
    ----------
    df_DataSeries : pandas.DataFrame
        A dataframe that contains the OD600 measurements over time. For each
        sample there is one column for the time points and one column for the
        OD 600 measurements.

    Returns
    -------
    df_OD600 : pandas.DataFrame
        A dataframe that shows the OD600 measurement at the last time point for
        each sample.
    """
    # Select only the columns that contain OD 600 measurements
    col_names = [
        name for name in list(df_DataSeries.columns) if name.endswith("data")
    ]
    df_OD600 = df_DataSeries[col_names]
    # Fill all NaN with the last value and transform
    df_OD600 = df_OD600.ffill(axis=0).T
    # Take only sample name and last OD measurement
    df_OD600.reset_index(inplace=True)
    df_OD600 = df_OD600.iloc[:, [0, -1]]
    df_OD600.columns = ["samplename_OD", "OD600"]
    df_OD600["samplename_OD"] = df_OD600["samplename_OD"].str[:6]
    return df_OD600


def extract_muMax(df_Annotations):
    """
    Extracts the growth rate (Slope) for each sample.

    Parameters
    ----------
    df_Annotations : pandas.DataFrame
        The dataframe contains the results of a linear fit through the
        exponential growth phase.

    Returns
    -------
    df_mu : pandas.DataFrame
        A dataframe that shows the calculated maximal growth rate for each
        sample.
    """
    # Delete index name and transform
    df_Annotations.index.name = None
    df_mu = df_Annotations.T
    # Keep only sample name and slope
    df_mu.reset_index(inplace=True)
    df_mu = df_mu.rename(columns={"index": "samplename_OD"})
    df_mu = df_mu[["samplename_OD", "Slope"]]
    df_mu["samplename_OD"] = df_mu["samplename_OD"].str[:6]
    # Rename slope
    df_mu.rename(columns={"Slope": "mu[/h]"}, inplace=True)
    return df_mu


def extract_growthData(df_DataSeries, df_Annotations):
    """
    Extracts the last OD600 measurement and the growth rate (Slope) for each
    sample.

    Parameters
    ----------
    df_DataSeries : pandas.DataFrame
        A dataframe that contains the OD600 measurements over time. The
        columns specify the time points and the OD 600 measurements for each
        sample.
    df_Annotations : pandas.DataFrame
        The dataframe contains the results of a linear fit through the
        exponential growth phase.

    Returns
    -------
    df_OD : pandas.DataFrame
        A dataframe with three columns specifying the sample name, the OD600
        at the last measured time point and the calculated maximal growth rate
        mu.
    """
    df_OD600 = extract_OD600(df_DataSeries)
    df_mu = extract_muMax(df_Annotations)
    df_OD = pd.merge(df_OD600, df_mu, how="outer", on="samplename_OD")
    return df_OD


def calculate_rates(df_data, n_min=2):
    """
    Calculates the specific uptake/secretion rates from the metabolite
    concentrations and growth rates using the differently diluted samples,
    which mimic a time course.

    Parameters
    ----------
    df_data : pandas.DataFrame
        Dataframe containing exometabolome concentrations and growth
        information for each metabolite, dilution step and replica. Must
        contain the columns "metabolite", "conc[mM]", "replica", "mu[/h]",
        "CDW[g/L]".
    n_min : int
        The minimum number of samples for a fixed replica and metabolite
        needed to calculate the slope and rate.

    Returns
    -------
    df_rates : pandas.DataFrame
        Dataframe containing the maximum growth rate, slope + r-squared and
        rate for each metabolite and replica.
    """
    slopes_dict = dict()
    cnt = 0

    # Filter for each metabolite
    for metabolite in df_data.metabolite.unique():
        df2 = df_data[df_data["metabolite"] == metabolite]
        # Second filter for each replica
        for replica in df_data.replica.unique():
            df3 = df2[df2["replica"] == replica]
            mu_max = df3["mu[/h]"].max()
            # Only continue, if a enough samples available
            if len(df3.index) >= n_min:

                # fit linear regression model
                X = df3["CDW[g/L]"]
                y = df3["conc[mM]"]
                slope, intercept, r_value, p_value, std_err = linregress(X, y)

                # Add to dict
                slopes_dict[cnt] = {
                    "metabolite": metabolite,
                    "replica": replica,
                    "mu[/h]": mu_max,
                    "intercept[mM]": intercept,
                    "slope[mmol/gDCW]": slope,
                    "r-squared": r_value ** 2,
                    "rate[mmol/gDCW/h]": slope * mu_max,
                }
                cnt = cnt + 1

    # Create a dataframe from the dict
    df_rates = pd.DataFrame.from_dict(slopes_dict, "index")
    return df_rates


def plot_oneReplica(
    df_data, df_rates, metabolite, replica, annotation=True, size=(7, 5)
):
    """
    Creates one plot for one replica:
    Plots metabolite concentration over the dry cell weight. Adds the linear
    fit as a line and the dilution steps
    as annotations.

    Parameters
    ----------
    df_data : pandas.DataFrame
        Dataframe containing exometabolome concentrations and growth
        information for each metabolite, dilution step and replica. Must
        contain the columns "metabolite", "dilution_step", "replica",
        "CDW[g/L]" and "conc[mM]".
    df_rates : pandas.DataFrame
        Dataframe containing the growth rate and the metabolite
        uptake rates for each metabolite and replica.
        Must contain the columns "replica", "metabolite", "intercept", "slope"
        and "r-squared".
    metabolite : str
        A string specifing the metabolite.
    replica : numpy.int64
        A numpy integer specifing the replica.
    annotation : bool, default True
        Adds the dilution step as annotation when True.
    size : tuple
        A tuple of two integers that specify the figure size.
    """
    # Get the data points from the data dataframe
    df_data = df_data.loc[
        (df_data.replica == replica) & (df_data.metabolite == metabolite)
    ]
    X = df_data["CDW[g/L]"]
    y = df_data["conc[mM]"]
    annotations = df_data["dilution_step"]
    # Get the linear regresson parameters from the rates dataframe
    df_rates = df_rates.loc[
        (df_rates.replica == replica) & (df_rates.metabolite == metabolite)
    ]
    intercept = df_rates.iloc[0]["intercept[mM]"]
    slope = df_rates.iloc[0]["slope[mmol/gDCW]"]
    rsquared = df_rates.iloc[0]["r-squared"]
    # Plot
    plt.figure(figsize=size)
    plt.scatter(X, y)
    plt.plot(X, slope * X + intercept, "r", alpha=0.7)
    plt.suptitle(
        "{}, replica {}".format(metabolite, replica), fontsize=15, y=1.02
    )
    plt.title(
        "Slope:{}, R-squared:{}".format(round(slope, 3), round(rsquared, 3))
    )
    plt.xlabel("cell dry weight [g/L]")
    plt.ylabel("concentration [mM]")
    if annotation is True:
        for i, label in zip(df_data.index, annotations):
            plt.annotate(str(label), (X[i], y[i]))


def plot_allReplica(
    df_data, df_rates, metabolite, annotation=True, size=(12, 8)
):
    """
    Creates one plot for all replicas.
    Plots metabolite concentration over the dry cell weight, Adds the linear
    fit as a line and the dilution steps
    as annotations.

    Parameters
    ----------
    df_data : pandas.DataFrame
        Dataframe containing exometabolome concentrations and growth
        information for each metabolite, dilution step and replica. Must
        contain the columns "metabolite", "dilution_step", "replica",
        "CDW[g/L]" and "conc[mM]".
    df_rates : pandas.DataFrame
        Dataframe containing the growth rate and the metabolite
        uptake rates for each metabolite and replica. Must contain the column
        "replica", "metabolite", "intercept", "slope" and "r-squared".
    metabolite : str
        A string specifing the metabolite.
    annotation : bool, default True
        Adds the dilution step as annotation when True.
    size : tuple, default (12, 8)
        A tuple of two integers specifying the figure size.
    """
    fig, ax = plt.subplots(figsize=size)
    for replica in df_rates.replica.unique():
        # Get the data points from the data dataframe
        df_data2 = df_data.loc[
            (df_data.replica == replica) & (df_data.metabolite == metabolite)
        ]
        X = df_data2["CDW[g/L]"]
        y = df_data2["conc[mM]"]
        annotations = df_data2["dilution_step"]
        # Get the linear regresson parameters from the rates dataframe
        df_rates2 = df_rates.loc[
            (df_rates.replica == replica) & (df_rates.metabolite == metabolite)
        ]
        intercept = df_rates2.iloc[0]["intercept[mM]"]
        slope = df_rates2.iloc[0]["slope[mmol/gDCW]"]
        # Plot
        ax.scatter(X, y)
        ax.plot(X, slope * X + intercept, alpha=0.7)
        if annotation is True:
            for i, label in zip(df_data2.index, annotations):
                ax.annotate(str(label), (X[i], y[i]))
    # Add title, labels and legend
    plt.title("{}".format(metabolite), fontsize=15)
    plt.xlabel("cell dry weight [g/L]")
    plt.ylabel("concentration [mM]")
    ax.legend(df_rates.replica.unique(), title="replica")


def calculate_mean(df_rates):
    """
    Calculates the mean of the specific uptake rates for each metabolite.

    Parameters
    ----------
    df_rates : pandas.DataFrame
        Dataframe containing the growth rate and the metabolite uptake
        rates for each metabolite and replica. Must contain the columns
        "metabolite" and "rate[mmol/gDCW/h]".

    Returns
    -------
    df_results : pandas.DataFrame
        Dataframe containing the calculated mean[mmol/(gDCW*h)] and standard
        deviation[mmol/(gDCW*h)] for the uptake rates of each metabolite
    """
    df_results = df_rates.groupby("metabolite")["rate[mmol/gDCW/h]"]
    df_results = df_results.agg([np.mean, np.std])
    df_results.reset_index(inplace=True)
    df_results.columns = ["metabolite", "mean", "std"]
    return df_results
