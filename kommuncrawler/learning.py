import os
import json
import re

MODEL_FILE = os.path.join('results', 'pattern_counts.json')


def _load_counts():
    if os.path.exists(MODEL_FILE):
        with open(MODEL_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except Exception:
                return {}
    return {}


def _save_counts(data):
    os.makedirs(os.path.dirname(MODEL_FILE), exist_ok=True)
    with open(MODEL_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def _extract_tokens(text: str) -> list:
    """Return words around the first number."""
    m = re.search(r"(\d{3,5})", text)
    if not m:
        return []
    start = max(0, m.start() - 40)
    end = m.end() + 40
    context = text[start:end].lower()
    return re.findall(r"[a-zåäöA-ZÅÄÖ]{3,}", context)


def update_model(text: str):
    counts = _load_counts()
    for token in _extract_tokens(text):
        counts[token] = counts.get(token, 0) + 1
    _save_counts(counts)


def score_text(text: str) -> float:
    counts = _load_counts()
    tokens = _extract_tokens(text)
    if not tokens or not counts:
        return 0.0
    total = sum(counts.get(t, 0) for t in tokens)
    return total / (len(tokens) * max(counts.values()))
