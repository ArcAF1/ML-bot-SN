import re


def extract_tax_info_from_text(text: str) -> dict:
    """Extracts tax info such as hourly rate and billing model from text."""
    result = {
        "timtaxa": None,
        "debiteringsmodell": None,
        "confidence": 0.0,
    }

    text = text.lower()
    hits = []

    number_pattern = r"\d+(?:[\s\u202f,.]\d{3})*(?:[.,]\d+)?"

    tax_patterns = [
        rf"timtaxa\s*[:=]?\s*({number_pattern})\s*(?:kr|kronor)",
        rf"timavgift(en)?\s*(är|på)?\s*({number_pattern})\s*(kr|kronor)",
        rf"({number_pattern})\s*(kr|kronor)\s*(per|\/)?\s*tim(me)?",
        rf"({number_pattern})\s*(kr|kronor)\s*\/\s*tim(me)?"
    ]

    for pattern in tax_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                raw_number = next(filter(lambda x: re.match(r"\d", x), match))
                cleaned = (
                    raw_number.replace(" ", "")
                    .replace("\u202f", "")
                    .replace(",", ".")
                )
                parts = cleaned.split(".")
                if len(parts) > 2:
                    cleaned = "".join(parts[:-1]) + "." + parts[-1]
                number = float(cleaned)
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

    return result
