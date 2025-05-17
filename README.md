# KommunCrawler (Simplified)

This project provides a lightweight crawler that tries to locate tax information from Swedish municipalities.
It relies solely on Python's standard library and requires **Python&nbsp;3.9+**.
`requirements.txt` is intentionally empty as a reminder that no extra packages are needed.

## Usage

1. (Optional) install packages listed in `requirements.txt` (there are none).

2. Prepare a `kommuner.csv` file with the columns `kommun` and `url`. Example:

   ```csv
   kommun,url
   Ale,https://www.ale.se/
   Alingsås,https://www.alingsas.se/
   ```

3. Run the pipeline:

```bash
python -m kommuncrawler.run_pipeline
```

Results will be written to `results/output.csv`.
