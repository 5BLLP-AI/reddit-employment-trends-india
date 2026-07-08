import streamlit as st

from utils import load_dashboard_data, render_overview_page


st.set_page_config(
    page_title="Overview | Reddit Employment Trends",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    df = load_dashboard_data()
    render_overview_page(df)


if __name__ == "__main__":
    main()