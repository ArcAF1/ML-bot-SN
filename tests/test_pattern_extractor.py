import unittest
from kommuncrawler.pattern_extractor import extract_tax_info_from_text

class TestPatternExtractor(unittest.TestCase):
    def test_extracts_tax_rate_and_model(self):
        text = 'Avgiften baseras på en timtaxa 1200 kronor och betalas i efterskott.'
        result = extract_tax_info_from_text(text)
        self.assertEqual(result['timtaxa'], 1200)
        self.assertEqual(result['debiteringsmodell'], 'efteråt')
        self.assertGreater(result['confidence'], 0)

    def test_no_match(self):
        text = 'Denna text innehåller ingen relevant information.'
        result = extract_tax_info_from_text(text)
        self.assertIsNone(result['timtaxa'])
        self.assertIsNone(result['debiteringsmodell'])
        self.assertEqual(result['confidence'], 0.0)

if __name__ == '__main__':
    unittest.main()
