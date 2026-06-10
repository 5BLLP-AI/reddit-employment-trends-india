from src.cleaning import basic_clean, normalize_submission


def test_basic_clean():
    assert basic_clean(" hello \n world ") == "hello world"


def test_normalize_submission():
    raw = {"id": "1", "title": " t ", "selftext": None, "created_utc": 0}
    out = normalize_submission(raw)
    assert out["id"] == "1"
    assert out["title"] == "t"
