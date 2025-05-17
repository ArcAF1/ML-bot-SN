from urllib.parse import urljoin, urlparse
from urllib.request import urlopen, Request
from html.parser import HTMLParser
import re

DEFAULT_MAX_DEPTH = 5
MAX_PAGES_PER_LEVEL = 100  # upper bound per level to avoid infinite crawl
MAX_TOTAL_PAGES = 500      # global page limit


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    self.links.append(value)


def _fetch(url: str) -> str:
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=10) as resp:
            charset = resp.headers.get_content_charset() or 'utf-8'
            return resp.read().decode(charset, errors='ignore')
    except Exception:
        return ''


def _is_internal(link: str, base_url: str) -> bool:
    if link.startswith('http'):
        return urlparse(link).netloc == urlparse(base_url).netloc
    return True


def crawl_site(base_url: str, max_depth: int = DEFAULT_MAX_DEPTH, max_pages: int = MAX_TOTAL_PAGES) -> list:
    """Breadth-first crawl within the same domain up to a depth and page limit."""
    queue = [(base_url, 0)]
    visited = set()
    results = []
    pages_seen = 0

    while queue and pages_seen < max_pages:
        url, depth = queue.pop(0)
        if url in visited or depth > max_depth:
            continue
        visited.add(url)

        text = _fetch(url)
        if not text:
            continue
        results.append((text, url))
        pages_seen += 1

        if depth < max_depth and pages_seen < max_pages:
            parser = LinkParser()
            parser.feed(text)
            count = 0
            for href in parser.links:
                full = urljoin(url, href)
                if _is_internal(full, base_url) and full not in visited:
                    queue.append((full, depth + 1))
                    count += 1
                    if count >= MAX_PAGES_PER_LEVEL or pages_seen + len(queue) >= max_pages:
                        break
    return results
