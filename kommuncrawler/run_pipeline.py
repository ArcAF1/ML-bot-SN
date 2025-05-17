"""Utilities for running the full crawling pipeline."""

import argparse
import csv
from .processor import process_municipality
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


def run(municipalities_csv: str = 'kommuner.csv', output_dir: str = 'results') -> None:
    """Run the complete crawling and extraction pipeline.

    Parameters
    ----------
    municipalities_csv:
        Path to the CSV file with municipalities.
    output_dir:
        Directory where the result CSV will be stored.
    """

    municipalities = load_municipalities(municipalities_csv)
    if not municipalities:
        print('No municipalities to process.')
        return

    results = []
    for name, url in municipalities:
        print(f'Processing {name}...')
        res = process_municipality(name, url)
        results.append(res)

    export_results(results, output_path=output_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the kommun crawler pipeline')
    parser.add_argument('-m', '--municipalities', default='kommuner.csv', help='Path to municipalities CSV')
    parser.add_argument('-o', '--output', default='results', help='Directory for output CSV')
    args = parser.parse_args()

    run(args.municipalities, args.output)
