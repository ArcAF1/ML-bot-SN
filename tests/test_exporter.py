import unittest
import tempfile
from pathlib import Path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from kommuncrawler.exporter import export_results


class ExporterTest(unittest.TestCase):
    def test_export_results_empty(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            export_results([], output_path=tmpdir)
            self.assertEqual(list(Path(tmpdir).iterdir()), [])

if __name__ == '__main__':
    unittest.main()
