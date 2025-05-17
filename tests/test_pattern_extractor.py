import unittest
from kommuncrawler.pattern_extractor import extract_tax_info_from_text


class TestPatternExtractor(unittest.TestCase):
    def test_extract_tax_info_positive(self):
        text = "Timtaxa 1200 kronor per timme. Debitering sker i efterskott."
        result = extract_tax_info_from_text(text)
        self.assertEqual(result["timtaxa"], 1200)
        self.assertEqual(result["debiteringsmodell"], "efteråt")
        self.assertGreater(result["confidence"], 0)

    def test_extract_tax_info_none(self):
        result = extract_tax_info_from_text("Detta är en testtext utan belopp.")
        self.assertIsNone(result["timtaxa"])
        self.assertIsNone(result["debiteringsmodell"])


if __name__ == "__main__":
    unittest.main()
