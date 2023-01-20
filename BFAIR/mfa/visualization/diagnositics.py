import altair as alt
from BFAIR.mfa.INCA.INCA_results import INCA_results
import numpy as np
import pandas as pd
from typing import Union, Tuple
import scipy.stats
import matplotlib.pyplot as plt

def plot_residuals_vs_fitted(INCA_results: INCA_results) -> alt.Chart:
    df = INCA_results.measurements_and_fit_detailed.drop(columns=["base"])
    return (
        alt.Chart(df)
        .mark_point()
        .encode(
            x=alt.X("fit:Q", scale=alt.Scale(type="log")),
            y=alt.Y(
                "weighted residual:Q",
            ),
            tooltip=["type", "id:N", "peak"],
        )
    )


def plot_norm_probplot(
    INCA_results: INCA_results, interactive: bool = False
) -> Union[alt.Chart, Tuple[plt.Figure, plt.Axes]]:

    if not interactive:
        fig, ax = plt.subplots()
        _, _ = scipy.stats.probplot(
            INCA_results.measurements_and_fit_detailed["weighted residual"],
            dist="norm",
            plot=ax,
        )
        return fig, ax 

    # Making interactive plot with altair
    rankits, fit = scipy.stats.probplot(
        INCA_results.measurements_and_fit_detailed["weighted residual"],
        dist="norm",
        plot=None,
    )

    plot_df = (
        INCA_results.measurements_and_fit_detailed.sort_values("weighted residual")
        .drop(columns="base")
        .copy()
    )
    plot_df["Theoretical normal quantile"] = rankits[0]

    points = (
        alt.Chart(plot_df)
        .mark_point()
        .encode(
            x=alt.X(
                "Theoretical normal quantile:Q",
            ),
            y=alt.Y(
                "weighted residual:Q",
            ),
            tooltip=["type", "id:N", "peak", "weighted residual:Q"],
        )
    )

    # Create data for the line
    x = np.linspace(
        plot_df["Theoretical normal quantile"].min(),
        plot_df["Theoretical normal quantile"].max(),
        10,
    )
    y = fit[1] + fit[0] * x

    fit_df = pd.DataFrame({"x": x, "y": y})

    line = alt.Chart(fit_df).mark_line().encode(x="x", y="y")
    return points + line