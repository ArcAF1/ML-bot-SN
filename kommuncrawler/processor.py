"""Processing utilities for a single municipality."""

from .crawler import crawl_site, DEFAULT_MAX_DEPTH, MAX_PAGES_PER_LEVEL
from .pattern_extractor import extract_tax_info_from_text
from .utils.text import normalize_text


MAX_CHARS = 15000


def process_municipality(
    name: str,
    url: str,
    max_depth: int = DEFAULT_MAX_DEPTH,
    max_pages_per_level: int = MAX_PAGES_PER_LEVEL,
) -> dict:
    """Crawl ``url`` and extract tax information for ``name``.

    Parameters
    ----------
    name:
        Municipality name for the result entry.
    url:
        Starting URL for the crawl.
    max_depth:
        How many link levels deep to follow.
    max_pages_per_level:
        Limit for how many pages to queue from a single page.
    """
    pages = crawl_site(url, max_depth=max_depth, max_pages_per_level=max_pages_per_level)
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
