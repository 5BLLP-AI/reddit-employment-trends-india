import pandas as pd

df = pd.read_csv(
    "data/processed/reddit_posts_cleaned.csv"
)

def test_dataset_not_empty():
    assert len(df) > 0

def test_title_exists():
    assert "title" in df.columns

def test_clean_title_exists():
    assert "clean_title" in df.columns

def test_location_exists():
    assert "location" in df.columns

def test_skill_exists():
    assert "skill" in df.columns

def test_role_exists():
    assert "role" in df.columns