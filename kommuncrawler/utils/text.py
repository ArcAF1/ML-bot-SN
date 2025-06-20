import re

def normalize_text(text: str) -> str:
    """Simple whitespace normalization."""
    text = text.replace('\xa0', ' ')
    text = text.replace(',', '.')
    text = re.sub(r'\s+', ' ', text)
    return text
