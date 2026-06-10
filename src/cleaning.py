import re
from typing import Dict


def basic_clean(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\n", " ").strip()
    text = re.sub(r"\s+", " ", text)
    return text


def normalize_submission(raw: Dict) -> Dict:
    return {
        "id": raw.get("id"),
        "title": basic_clean(raw.get("title", "")),
        "selftext": basic_clean(raw.get("selftext", "")),
        "created_utc": raw.get("created_utc"),
    }
