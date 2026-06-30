from src.feature_engineering import extract_skill, extract_role

def test_skill():
    assert extract_skill("python developer") == "Python"

def test_role():
    assert extract_role("python software engineer") == "Software Engineer"