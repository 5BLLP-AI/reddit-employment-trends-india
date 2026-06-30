from src.location_normalization import extract_location

def test_location():
    assert extract_location("software engineer bangalore") == "Bangalore"