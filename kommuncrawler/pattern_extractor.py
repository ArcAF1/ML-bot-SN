import re
from .learning import score_text


def extract_tax_info_from_text(text: str) -> dict:
    """Extracts tax info such as hourly rate and billing model from text."""
    result = {
        "timtaxa": None,
        "debiteringsmodell": None,
        "confidence": 0.0,
    }

    text = text.lower()
    hits = []

    tax_patterns = [
        r"timtaxa\s*[:=]?\s*(\d{1,3}(?:[\s\u202f]?\d{3})*)\s*(?:kr|kronor)",
        r"timavgift(en)?\s*(är|på)?\s*(\d{1,3}(?:[\s\u202f]?\d{3})*)\s*(kr|kronor)",
        r"(\d{1,3}(?:[\s\u202f]?\d{3})*)\s*(kr|kronor)\s*(per|\/)?\s*tim(me)?",
        r"(\d{3,5})\s*(kr|kronor)\s*\/\s*tim(me)?"
    ]

    for pattern in tax_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                raw_number = next(filter(lambda x: re.match(r"\d", x), match))
                number = int(raw_number.replace(" ", "").replace("\u202f", ""))
                if 500 <= number <= 5000:
                    hits.append(number)
            except Exception:
                continue

    if hits:
        result["timtaxa"] = max(hits)
        result["confidence"] += 0.6

    if "efterskott" in text or "efterhandsdebitering" in text:
        result["debiteringsmodell"] = "efteråt"
        result["confidence"] += 0.3
    elif "förskott" in text or "förhandsdebitering" in text:
        result["debiteringsmodell"] = "förskott"
        result["confidence"] += 0.3

    # self-learning score based on previous runs
    result["confidence"] += 0.1 * score_text(text)

    return result
