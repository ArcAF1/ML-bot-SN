# KommunCrawler (Simplified)

This project provides a crawler that locates tax information from Swedish municipalities.
It gradually improves by remembering patterns from pages where a tax was successfully found.

## Usage

1. (Optional) install packages listed in `requirements.txt`.

2. Prepare a `kommuner.csv` file with the columns `kommun` and `url`.

3. Run the pipeline:

```bash
python -m kommuncrawler.run_pipeline
```

Results will be written to `results/output.csv`.

After each successful extraction the crawler updates a simple model
(`results/pattern_counts.json`) used to score future pages, so it
gradually learns which words often appear near the correct values.
