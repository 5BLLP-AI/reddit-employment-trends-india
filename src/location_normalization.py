from typing import Optional


def extract_location_from_text(text: str) -> Optional[str]:
    # Placeholder: simple heuristic to find 'in <Location>' phrases
    if not text:
        return None
    lower = text.lower()
    tokens = lower.split()
    if " in " in lower:
        # naive parse
        try:
            idx = tokens.index("in")
            return tokens[idx + 1].capitalize()
        except Exception:
            return None
    return None
