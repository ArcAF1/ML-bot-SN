"""CSV exporter for crawler results."""

import os
import csv
from typing import Any


def export_results(
    results: list[dict[str, Any]],
    output_path: str = 'results',
    file_name: str = 'output.csv',
) -> None:
    """Write extraction results to ``output_path/file_name``."""
    os.makedirs(output_path, exist_ok=True)
    rows = []
    for item in results:
        kommun = item['kommun']
        data = item['data']
        rows.append({
            'kommun': kommun,
            'timtaxa': data.get('timtaxa'),
            'debiteringsmodell': data.get('debiteringsmodell'),
            'confidence': data.get('confidence'),
            'källa': data.get('källa'),
        })

    if not rows:
        print("No results to export")
        return

    output_file = os.path.join(output_path, file_name)
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"Saved {len(rows)} rows to {output_file}")
