import csv
from .processor import process_municipality
from .exporter import export_results


def load_municipalities(path='kommuner.csv'):



def run():
    municipalities = load_municipalities()

    results = []
    for name, url in municipalities:
        print(f'Processing {name}...')
        res = process_municipality(name, url)
        results.append(res)
    export_results(results)


if __name__ == '__main__':
    run()
