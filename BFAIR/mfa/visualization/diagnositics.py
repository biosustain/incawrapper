import altair as alt
from BFAIR.mfa.INCA.INCA_results import INCA_results

def plot_residuals_vs_fitted(INCA_results: INCA_results):
    df = INCA_results.measurements_and_fit_detailed.drop(columns=['base'])
    return alt.Chart(df).mark_point().encode(
        x = alt.X(
            'fit:Q',
            scale=alt.Scale(type="log")
        ),
        y = alt.Y(
            'weighted residual:Q',
        ),
        tooltip = ['type', 'id:N', 'peak']
    )