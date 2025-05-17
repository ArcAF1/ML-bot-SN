from .crawler import crawl_site
from .pattern_extractor import extract_tax_info_from_text
from .utils.text import normalize_text


MAX_CHARS = 15000


def process_municipality(name: str, url: str) -> dict:
    pages = crawl_site(url)
    best_score = -1
    best_result = None
    best_url = url

    for text, page_url in pages:
        clean_text = normalize_text(text[:MAX_CHARS])
        result = extract_tax_info_from_text(clean_text)
        score = result['confidence']
        if score > best_score:
            best_score = score
            best_result = result
            best_url = page_url

    if not best_result:
        best_result = {
            'timtaxa': None,
            'debiteringsmodell': None,
            'confidence': 0.0,
        }

    best_result['källa'] = best_url
    return {'kommun': name, 'data': best_result}
