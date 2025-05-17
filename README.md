# KommunCrawler (Simplified)

This project provides a lightweight crawler that tries to locate tax information
from Swedish municipalities. The crawler now explores much deeper so that it
searches the whole municipal domain rather than only a few sub pages.

## Usage

1. (Optional) install packages listed in `requirements.txt`. The program only
   uses Python standard library so no extra packages are required.

2. Prepare a `kommuner.csv` file with the columns `kommun` and `url`.

3. Run the pipeline:

```bash
python -m kommuncrawler.run_pipeline
```

Results will be written to `results/output.csv`.
The CSV includes a `källa` column linking to the page where the information was
found.
