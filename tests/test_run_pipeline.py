import unittest
import os
import csv
import tempfile
from unittest.mock import patch
from kommuncrawler import run_pipeline


class TestRunPipeline(unittest.TestCase):
    def test_run_writes_output_csv(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "municipalities.csv")
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["kommun", "url"])
                writer.writeheader()
                writer.writerow({"kommun": "A", "url": "http://a"})
                writer.writerow({"kommun": "B", "url": "http://b"})


            def fake_crawl(url, max_depth=2, max_pages_per_level=20, max_concurrency=5):

            def fake_crawl(url, max_depth=2, max_pages_per_level=20):

                return [("dummy", f"{url}/page")]

            def fake_extract(text):
                return {
                    "timtaxa": 42,
                    "debiteringsmodell": "efteråt",
                    "confidence": 1.0,
                }

            out_dir = os.path.join(tmpdir, "out")
            with patch("kommuncrawler.processor.crawl_site", side_effect=fake_crawl), \
                 patch("kommuncrawler.processor.extract_tax_info_from_text", side_effect=fake_extract):
                run_pipeline.run(csv_path, output_dir=out_dir, max_concurrency=3)

            output_file = os.path.join(out_dir, "output.csv")
            self.assertTrue(os.path.exists(output_file))

            with open(output_file, newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))

            self.assertEqual(len(rows), 2)
            for row, (kommun, url) in zip(rows, [("A", "http://a"), ("B", "http://b")]):
                self.assertEqual(row["kommun"], kommun)
                self.assertEqual(row["timtaxa"], "42")
                self.assertEqual(row["debiteringsmodell"], "efteråt")
                self.assertEqual(row["confidence"], "1.0")
                self.assertEqual(row["källa"], f"{url}/page")


if __name__ == "__main__":
    unittest.main()
