import plotly.express as px


def plot_count_by_location(df, location_col="location"):
    fig = px.histogram(df, x=location_col)
    return fig
