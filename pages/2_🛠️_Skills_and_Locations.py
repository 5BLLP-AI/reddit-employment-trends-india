from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "dashboard"))

from utils import apply_sidebar_filters, load_dashboard_data, render_filter_summary, render_locations_page, render_skills_page  # noqa: E402


st.set_page_config(
    page_title="Skills and Locations | Reddit Employment Trends",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    df = load_dashboard_data()
    filtered = apply_sidebar_filters(df)
    render_filter_summary(filtered, df)
    tabs = st.tabs(["Skills", "Locations"])
    with tabs[0]:
        render_skills_page(df, filtered_df=filtered)
    with tabs[1]:
        render_locations_page(df, filtered_df=filtered)


if __name__ == "__main__":
    main()