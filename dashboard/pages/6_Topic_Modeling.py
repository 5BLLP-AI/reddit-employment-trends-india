import streamlit as st

from utils import load_dashboard_data, render_topics_page


st.set_page_config(
    page_title="Topic Modeling | Reddit Employment Trends",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    df = load_dashboard_data()
    render_topics_page(df)


if __name__ == "__main__":
    main()