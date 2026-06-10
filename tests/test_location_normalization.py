from src.location_normalization import extract_location_from_text


def test_extract_location_none():
    assert extract_location_from_text("") is None


def test_extract_location_simple():
    assert extract_location_from_text("Hiring in Bangalore") == "Bangalore"
