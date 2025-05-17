"""Simple depth-limited crawler used by the pipeline."""

from urllib.parse import urljoin, urlparse
from urllib.request import urlopen, Request
from html.parser import HTMLParser
try:
    from concurrent.futures import ThreadPoolExecutor, as_completed
    CONCURRENCY_AVAILABLE = True
except Exception:  # pragma: no cover
    ThreadPoolExecutor = None  # type: ignore
    as_completed = None  # type: ignore
    CONCURRENCY_AVAILABLE = False

DEFAULT_MAX_DEPTH = 2
MAX_PAGES_PER_LEVEL = 20
DEFAULT_MAX_CONCURRENCY = 5


class LinkParser(HTMLParser):
    """HTML parser that collects ``href`` links."""

    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    self.links.append(value)


def _fetch(url: str) -> str:
    """Retrieve the page content at ``url``.

    Returns an empty string on any failure."""
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=10) as resp:
            charset = resp.headers.get_content_charset() or 'utf-8'
            return resp.read().decode(charset, errors='ignore')
    except Exception:
        return ''


def _is_internal(link: str, base_url: str) -> bool:
    """Return ``True`` if ``link`` points to the same host as ``base_url``."""
    if link.startswith('http'):
        return urlparse(link).netloc == urlparse(base_url).netloc
    return True



def _crawl_sync(
    base_url: str,
    max_depth: int,
    max_pages_per_level: int = MAX_PAGES_PER_LEVEL,
) -> list:
    """Simple synchronous crawler using a queue."""

    queue = [(base_url, 0)]
    visited: set[str] = set()
    results = []

    while queue:
        url, depth = queue.pop(0)
        if url in visited or depth > max_depth:
            continue
        visited.add(url)

        text = _fetch(url)
        if not text:
            continue
        results.append((text, url))

        if depth < max_depth:
            parser = LinkParser()
            parser.feed(text)
            count = 0
            for href in parser.links:
                full = urljoin(url, href)
                if _is_internal(full, base_url) and full not in visited:
                    queue.append((full, depth + 1))
                    count += 1
                    if count >= max_pages_per_level:
                        break
    return results


def _crawl_concurrent(
    base_url: str,
    max_depth: int,
    max_workers: int,
    max_pages_per_level: int = MAX_PAGES_PER_LEVEL,
) -> list:
    """Concurrent crawler using threads."""
    visited = set()
    results = []
    current_level = [base_url]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for depth in range(max_depth + 1):
            futures = {executor.submit(_fetch, url): url for url in current_level if url not in visited}
            next_level = []
            visited.update(current_level)

            for future in as_completed(futures):
                url = futures[future]
                text = future.result()
                if not text:
                    continue
                results.append((text, url))

                if depth < max_depth:
                    parser = LinkParser()
                    parser.feed(text)
                    count = 0
                    for href in parser.links:
                        full = urljoin(url, href)
                        if _is_internal(full, base_url) and full not in visited and full not in next_level:
                            next_level.append(full)
                            count += 1
                            if count >= max_pages_per_level:
                                break

            current_level = next_level

    return results


def crawl_site(
    base_url: str,
    max_depth: int = DEFAULT_MAX_DEPTH,
    use_concurrent: bool | None = None,
    max_concurrency: int = DEFAULT_MAX_CONCURRENCY,
    max_pages_per_level: int = MAX_PAGES_PER_LEVEL,
) -> list:
    """Crawl ``base_url`` and return page contents up to ``max_depth``."""

    if use_concurrent is None:
        use_concurrent = CONCURRENCY_AVAILABLE

    if use_concurrent and CONCURRENCY_AVAILABLE:
        try:
            return _crawl_concurrent(
                base_url,
                max_depth,
                max_concurrency,
                max_pages_per_level,
            )
        except Exception:
            pass  # fall back to synchronous on any failure

    # Fallback to synchronous crawling
    return _crawl_sync(base_url, max_depth, max_pages_per_level)
