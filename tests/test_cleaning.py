from src.cleaning import clean_text

def test_clean_text():
    assert clean_text("Hello!!!") == "hello"
