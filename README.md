# KommunCrawler (Simplified)

This project provides a lightweight crawler that tries to locate tax information from Swedish municipalities.

Requires **Python 3.8+** and only uses the standard library.

## Usage

1. (Optional) install packages listed in `requirements.txt` (empty by default).

2. Prepare a `kommuner.csv` file with the columns `kommun` and `url`. Example:

```
kommun,url
Ale,https://www.ale.se/
Alingsås,https://www.alingsas.se/
```

3. Run the pipeline:

```bash
python -m kommuncrawler.run_pipeline
```

Results will be written to `results/output.csv`.
