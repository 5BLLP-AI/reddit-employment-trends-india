import pandas as pd


def build_basic_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["title_len"] = df["title"].str.len()
    df["has_text"] = df["selftext"].notna() & (df["selftext"].str.strip() != "")
    return df
