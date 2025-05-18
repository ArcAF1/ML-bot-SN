"""Utilities for running the full crawling pipeline."""

import argparse
import csv
from .processor import (
    process_municipality,
    DEFAULT_MAX_DEPTH,
    MAX_PAGES_PER_LEVEL,
    DEFAULT_MAX_CONCURRENCY,
)
from .exporter import export_results


def load_municipalities(path: str = 'kommuner.csv') -> list:
    """Load municipalities and their URLs from a CSV file.

    Parameters
    ----------
    path:
        Path to the CSV file containing ``kommun`` and ``url`` columns.

    Returns
    -------
    list of tuple[str, str]
        Tuples of municipality name and URL.
    """
    try:
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return [
                (row['kommun'], row['url'])
                for row in reader
                if row.get('kommun') and row.get('url')
            ]
    except FileNotFoundError:
        print(f'File not found: {path}')
        return []


def run(
    municipalities_csv: str = 'kommuner.csv',
    output_dir: str = 'results',
    depth: int = DEFAULT_MAX_DEPTH,
    pages_per_level: int = MAX_PAGES_PER_LEVEL,
    max_concurrency: int = DEFAULT_MAX_CONCURRENCY,
) -> None:
    """Run the complete crawling and extraction pipeline.

    Parameters
    ----------
    municipalities_csv:
        Path to the CSV file with municipalities.
    output_dir:
        Directory where the result CSV will be stored.
    depth:
        How many link levels deep to follow while crawling.
    pages_per_level:
        Number of pages to queue from each page.
    max_concurrency:

        Number of worker threads for concurrent crawling.

    """

    municipalities = load_municipalities(municipalities_csv)
    if not municipalities:
        print('No municipalities to process.')
        return

    results = []
    for name, url in municipalities:
        print(f'Processing {name}...')
        res = process_municipality(
            name,
            url,
            max_depth=depth,
            max_pages_per_level=pages_per_level,
            max_concurrency=max_concurrency,
        )
        results.append(res)

    export_results(results, output_path=output_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the kommun crawler pipeline')
    parser.add_argument('-m', '--municipalities', default='kommuner.csv', help='Path to municipalities CSV')
    parser.add_argument('-o', '--output', default='results', help='Directory for output CSV')
    parser.add_argument('--depth', type=int, default=DEFAULT_MAX_DEPTH, help='Maximum crawl depth')
    parser.add_argument('--pages-per-level', type=int, default=MAX_PAGES_PER_LEVEL, help='Pages to crawl per level')

    parser.add_argument('--concurrency', type=int, default=DEFAULT_MAX_CONCURRENCY, help='Number of concurrent workers')

    args = parser.parse_args()

    run(
        args.municipalities,
        args.output,
        args.depth,
        args.pages_per_level,
        args.concurrency,
    )
