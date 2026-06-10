import pandas as pd
from src.feature_engineering import build_basic_features


def test_build_basic_features():
    df = pd.DataFrame([{"title": "a", "selftext": "t"}])
    out = build_basic_features(df)
    assert "title_len" in out.columns
    assert "has_text" in out.columns
