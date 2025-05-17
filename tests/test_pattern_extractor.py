import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from kommuncrawler.pattern_extractor import extract_tax_info_from_text


class PatternExtractorTest(unittest.TestCase):
    def test_extract_tax_and_model(self):
        text = "Avgiften är timtaxa 1200 kr och betalas i efterskott."
        result = extract_tax_info_from_text(text)
        self.assertEqual(result["timtaxa"], 1200)
        self.assertEqual(result["debiteringsmodell"], "efteråt")

    def test_extract_none(self):
        result = extract_tax_info_from_text("Det finns ingen information här.")
        self.assertIsNone(result["timtaxa"])
        self.assertIsNone(result["debiteringsmodell"])

if __name__ == '__main__':
    unittest.main()
