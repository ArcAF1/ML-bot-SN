# KommunCrawler (Simplified)

This project provides a lightweight crawler that tries to locate tax information from Swedish municipalities.

## Usage

1. (Optional) install packages listed in `requirements.txt`. The program only uses Python standard library so no extra packages are required.

2. Prepare a `kommuner.csv` file with the columns `kommun` and `url`.

3. Run the pipeline:

```bash
python -m kommuncrawler.run_pipeline
```

Results will be written to `results/output.csv`.
