import unittest
import os
from kommuncrawler.exporter import export_results

class TestExporter(unittest.TestCase):
    def setUp(self):
        self.output_dir = 'test_results'
        os.makedirs(self.output_dir, exist_ok=True)

    def tearDown(self):
        for f in os.listdir(self.output_dir):
            os.remove(os.path.join(self.output_dir, f))
        os.rmdir(self.output_dir)

    def test_empty_results(self):
        # Should not raise error when results list is empty
        export_results([], output_path=self.output_dir, file_name='out.csv')
        self.assertFalse(os.listdir(self.output_dir))

if __name__ == '__main__':
    unittest.main()
