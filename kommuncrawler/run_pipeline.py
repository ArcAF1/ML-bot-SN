import csv
from .processor import process_municipality
from .exporter import export_results
from typing import Callable, Optional


def load_municipalities(path: str = 'kommuner.csv'):
    """Return a list of (municipality, url) tuples from a CSV file."""
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [
            (row['kommun'], row['url'])
            for row in reader
            if row.get('kommun') and row.get('url')
        ]


def run(progress_callback: Optional[Callable[[str], None]] = None, every: int = 10):
    """Process municipalities and export results.

    ``progress_callback`` can be provided to receive status messages.
    Results are written after every ``every`` municipalities.
    """
    municipalities = load_municipalities()
    results = []
    total = len(municipalities)
    for idx, (name, url) in enumerate(municipalities, start=1):
        msg = f'Processing {name} ({idx}/{total})...'
        print(msg)
        if progress_callback:
            progress_callback(msg)
        res = process_municipality(name, url)
        results.append(res)
        if idx % every == 0:
            export_results(results)
    export_results(results)


if __name__ == '__main__':
    run()
