# KommunCrawler

KommunCrawler crawls Swedish municipal websites and extracts hourly tax
information. The extracted data is written to a CSV file for further analysis.

## Prerequisites

- Python 3.9 or later
- Dependencies installed via `pip install -r requirements.txt`

## Usage

Run the pipeline from the project root:

```bash
python -m kommuncrawler.run_pipeline -m kommuner.csv -o results
```

### Command line options

- `-m`, `--municipalities` – path to the CSV with municipality names and URLs
- `-o`, `--output` – directory where the result CSV will be stored
- `--depth` – maximum crawl depth (default: 2)
- `--pages-per-level` – pages to crawl per level (default: 20)

- `--concurrency` – number of worker threads (default: 5)


### GUI

You can launch a minimal Tkinter interface with:

```bash
python -m kommuncrawler.gui
```

Use the dialogs to pick the municipalities CSV and output directory.
You can also set the crawl `Depth` and number of `Pages per level`.
The GUI requires a graphical environment to run.

## Running tests

Execute the unit test suite with:

```bash
python -m unittest discover -s tests -v
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for
details.


