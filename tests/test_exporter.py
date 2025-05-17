import unittest
import os
from kommuncrawler.exporter import export_results


class TestExporter(unittest.TestCase):
    def test_export_empty(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            out_dir = os.path.join(tmpdir, "results")
            export_results([], output_path=out_dir, file_name="test.csv")
            self.assertFalse(os.path.exists(os.path.join(out_dir, "test.csv")))


if __name__ == "__main__":
    unittest.main()
