import pandas as pd
import numpy as np


def min_max_norm(
    df,
    value_colname="Intensity",
    groupname_colname="sample_group_name",
    element_name="Metabolite",
):
    """
    Function that applies min/max scaling to the input dataframe; the data
    will range from 0 for the min- to 1 for the max value

    Parameters
    ----------
    df : pandas.DataFrame
        input dataframe, output of either the extractNamesAndIntensities()
        or the calculateMeanVarRSD() function
    groupname_colname : string
        the name of the column with the data that needs to be
        normalized, defaults to 'Intensity'
    groupname_colname : string
        the name of the column with the sample group names,
        defaults to 'sample_group_name'
    element_name: string
        the name of the column with the identifiers of the tested elements
        (e.g. metabolites or genes). Defaults to 'Metabolite'

    Returns
    -------
    output_df : pandas.DataFrame
        the output dataframe. It follows the same architecture as
        the input dataframe, just with normalized values
    """
    pivot_df = df.pivot(
        index=element_name, columns=groupname_colname, values=value_colname
    )
    output_df = pd.DataFrame()
    sample_group_names = df[groupname_colname].unique()
    for i, sample_group_name in enumerate(sample_group_names):
        red_df = df[df[groupname_colname] == sample_group_name]
        pivot_df = red_df.pivot(
            index=element_name, columns=groupname_colname, values=value_colname
        )
        new_df = pivot_df
        min_val = min(new_df[sample_group_name])
        max_val = max(new_df[sample_group_name])
        new_df[sample_group_name] = new_df[sample_group_name].sub(min_val)
        new_df[sample_group_name] = new_df[sample_group_name].div(
            (max_val - min_val)
        )
        temp_df = (
            new_df.stack()  # back to original shape
            .reset_index()  # reset index, making a "0" column with intensities
            .merge(
                red_df.drop(columns=value_colname), how="right"
            )  # add missing data
            .rename(columns={0: value_colname})  # renaming the "0" column
        )[
            df.columns
        ]  # match original column order
        if i == 0:
            output_df = temp_df
        else:
            output_df = output_df.append(temp_df)
    return output_df


def tsi_norm(
    df,
    value_colname="Intensity",
    groupname_colname="sample_group_name",
    element_name="Metabolite",
):
    """
    Applies Total Sum Intensity normalization; all values will be divided by
    the sum of all values. Like that, summing up all the values would
    amount to '1'

    Parameters
    ----------
    df : pandas.DataFrame
        input dataframe, output of either the extractNamesAndIntensities()
        or the calculateMeanVarRSD() function
    columnname : string
        the name of the column with the data that needs to be
        normalized, defaults to 'Intensity'
    groupname_colname : string
        the name of the column with the sample group names,
        defaults to 'sample_group_name'
    element_name: string
        the name of the column with the identifiers of the tested elements
        (e.g. metabolites or genes). Defaults to 'Metabolite'

    Returns
    -------
    output_df : pandas.DataFrame
        the output dataframe. It follows the same architecture as
        the input dataframe, just with normalized values
    """
    pivot_df = df.pivot(
        index=element_name, columns=groupname_colname, values=value_colname
    )
    pivot_df = pivot_df.div(pivot_df.sum(axis=0), axis=1)
    output_df = (
        pivot_df.stack()  # back to original shape
        .reset_index()  # reset index, making a "0" column with intensities
        .merge(df.drop(columns=value_colname), how="right")  # add missing data
        .rename(columns={0: value_colname})  # renaming the "0" column
    )[
        df.columns
    ]  # match original column order
    return output_df


def lim_tsi_norm(
    metabolite_input,
    df,
    biomass_value=None,
    value_colname="Intensity",
    groupname_colname="sample_group_name",
    element_name="Metabolite",
):
    """
    Applies a modified version of Total Sum Intensity normalization; all
    values will be divided by the sum of all the values of metabolites
    that are a) amino acids, b) part of the biomass function of a model of the
    organism of interest or c) are part of the biomass function of a model of
    the organism of interest weighted by their multipliers in said model.
    Like that, summing up all the values for the metabolites
    contributing to the biomass function would amount to '1'

    Parameters
    ----------
    metabolite_input : list, pandas.Series, np.ndarray or
        pandas.DataFrame
        either an object listing the metabolites of interest, e.g
        metabolites that are part of the biomass function, or a
        dataframe with the metabolties in one columns and another
        column with their corresponding multipliers
    df : pandas.DataFrame
        input dataframe, output of either the extractNamesAndIntensities()
        or the calculateMeanVarRSD() function
    biomass_value : float
        the multiplier of biomass on the product side of the
        biomass function in the corresponding metabolic model.
        Defaults to 'None'
    columnname : string
        the name of the column with the data that needs to be
        normalized, defaults to 'Intensity'.
        Defaults to 'Intensity'
    groupname_colname : string
        the name of the column with the sample group names,
        defaults to 'sample_group_name'.
        Defaults to "sample_group_name"
    element_name: string
        the name of the column with the identifiers of the tested elements
        (e.g. metabolites or genes). Defaults to 'Metabolite'

    Returns
    -------
    output_df : pandas.DataFrame
        the output dataframe. It follows the same architecture as
        the input dataframe, just with normalized values

    Raises
    ------
    ValueError
        Alerts user if 'biomass_value' is needed but missing
    ValueError
        Wrong type of input
    """
    lim_tsi = 0
    output_df = pd.DataFrame()
    sample_group_names = df[groupname_colname].unique()
    for i, sample_group_name in enumerate(sample_group_names):
        red_df = df[df[groupname_colname] == sample_group_name]
        pivot_df = red_df.pivot(
            index=element_name, columns=groupname_colname, values=value_colname
        )
        new_df = pivot_df
        if isinstance(
            metabolite_input, (list, pd.core.series.Series, np.ndarray)
        ):
            for metabolite in metabolite_input:
                if metabolite in new_df.index:
                    met_tsi = sum(new_df[new_df.index == metabolite].values[0])
                    if not pd.isna(met_tsi):
                        lim_tsi += met_tsi
        elif type(metabolite_input) == pd.core.frame.DataFrame:

            if biomass_value is None:
                raise ValueError("'biomass_value' is missing!")
            for cnt, biomass_met in enumerate(metabolite_input[element_name]):
                if biomass_met in new_df.index:
                    met_tsi = sum(
                        new_df[new_df.index == biomass_met].values[0]
                    )
                    norm_met_tsi = met_tsi * (
                        metabolite_input["Value"][cnt] / biomass_value
                    )
                    if not pd.isna(met_tsi):
                        lim_tsi += norm_met_tsi
        else:
            raise ValueError(
                "Wrong type of input! Input must be either "
                "'list', 'pd.core.series.Series', 'np.ndarray' or "
                "'pd.core.frame.DataFrame', not '"
                + type(metabolite_input)
                + "'"
            )
        temp_pivot_df = new_df.div(lim_tsi)
        temp_df = (
            temp_pivot_df.stack()  # back to original shape
            .reset_index()  # reset index, making a "0" column with intensities
            .merge(
                red_df.drop(columns=value_colname), how="right"
            )  # add missing data
            .rename(columns={0: value_colname})  # renaming the "0" column
        )[
            df.columns
        ]  # match original column order
        if i == 0:
            output_df = temp_df
        else:
            output_df = output_df.append(temp_df)
    return output_df


def pqn_norm(
    df,
    groupname_colname="sample_group_name",
    value_colname="Intensity",
    corr_type="median",
    qc_vector=None,
    element_name="Metabolite",
):
    """
    Probabilistic Quotient Normalization: This method adjusts for dilutions.
    This is a modified version of Total Sum Intensity normalization

    Parameters
    ----------
    df : pandas.DataFrame
        input dataframe, output of either the extractNamesAndIntensities()
        or the calculateMeanVarRSD() function
    groupname_colname : string
        the name of the column with the sample group names,
        defaults to ‘sample_group_name’
    value_colname : string
        the name of the column with the data that needs to be
        normalized, defaults to ‘Intensity’
    corr_type : string
        type of midpoint determination, ‘median’ or ‘mean’
    qc_vector : list
        an optional QC vector that can be provided
    element_name: string
        the name of the column with the identifiers of the tested elements
        (e.g. metabolites or genes). Defaults to 'Metabolite'

    Returns
    -------
    output_df : pandas.DataFrame
        the output dataframe. It follows the same architecture as
        the input dataframe, just with normalized values
    """
    # 0, pivot table
    pivot_df = df.pivot(
        index=element_name, columns=groupname_colname, values=value_colname
    )
    # 1, divide each column by its total intensity
    pivot_df = pivot_df.div(pivot_df.sum(axis=0), axis=1)
    # 2, calculate QC vector as mean/median per row (i.e., metabolite)
    qc_df = (
        qc_vector
        if qc_vector is not None
        else getattr(pivot_df, corr_type)(axis=1, skipna=True)
    )
    # 3, normalize TSI by diving each row by corresponding value in QC vector
    # 4, calculate dilution factor as mean/median per column
    # (i.e., sample group name)
    dilution = getattr(pivot_df.div(qc_df, axis=0), corr_type)(
        axis=0, skipna=True
    )
    # 5, multiply each column by its dilution factor
    pivot_df = pivot_df.multiply(dilution, axis=1)
    # 6, output
    pqn = (
        pivot_df.stack()  # back to original shape
        .reset_index()  # reset index, making a "0" column with intensities
        .merge(df.drop(columns=value_colname), how="right")  # add missing data
        .rename(columns={0: value_colname})  # renaming the "0" column
    )[
        df.columns
    ]  # match original column order
    return pqn
