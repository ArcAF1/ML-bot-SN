# KommunCrawler (Simplified)

This project provides a lightweight crawler that tries to locate tax information from Swedish municipalities.
It requires **Python 3.9+** and uses only the standard library.

## Usage

1. (Optional) install packages listed in `requirements.txt`. The file is empty because no additional packages are needed.

2. Prepare a `kommuner.csv` file with the columns `kommun` and `url`. Example:

 
```csv
kommun,url
Ale,https://www.ale.se/
Alingsås,https://www.alingsas.se/
```

3. Run the pipeline (or double-click `run.sh`/`run.bat`):

```bash
python -m kommuncrawler.run_pipeline
```

Results will be written to `results/output.csv`.
