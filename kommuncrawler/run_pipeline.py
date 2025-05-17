import csv
from .processor import process_municipality
from .exporter import export_results


def load_municipalities(path='kommuner.csv'):
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


def run():
    municipalities = load_municipalities()
    if not municipalities:
        print('No municipalities to process.')
        return
    results = []
    for name, url in municipalities:
        print(f'Processing {name}...')
        res = process_municipality(name, url)
        results.append(res)
    export_results(results)


if __name__ == '__main__':
    run()
