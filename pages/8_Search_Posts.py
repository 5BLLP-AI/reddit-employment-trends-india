from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "dashboard"))

from utils import load_dashboard_data, render_search_page  # noqa: E402


st.set_page_config(
    page_title="Search Posts | Reddit Employment Trends",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    df = load_dashboard_data()
    render_search_page(df)


if __name__ == "__main__":
    main()