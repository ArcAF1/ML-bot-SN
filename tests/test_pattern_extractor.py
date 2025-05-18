import unittest
from kommuncrawler.pattern_extractor import extract_tax_info_from_text


class TestPatternExtractor(unittest.TestCase):
    def test_extract_tax_info_positive(self):
        text = "Timtaxa 1200 kronor per timme. Debitering sker i efterskott."
        result = extract_tax_info_from_text(text)
        self.assertEqual(result["timtaxa"], 1200.0)
        self.assertEqual(result["debiteringsmodell"], "efteråt")
        self.assertGreater(result["confidence"], 0)

    def test_extract_tax_info_decimal(self):
        text = "Timavgiften är 1 200,50 kronor per timme."
        result = extract_tax_info_from_text(text)
        self.assertAlmostEqual(result["timtaxa"], 1200.50)

    def test_extract_tax_info_decimal_comma_period(self):
        text = "Timtaxa 1,200.75 kronor per timme."
        result = extract_tax_info_from_text(text)
        self.assertAlmostEqual(result["timtaxa"], 1200.75)


    def test_extract_tax_info_colon(self):
        result = extract_tax_info_from_text("Timtaxa: 1200 kr")
        self.assertEqual(result["timtaxa"], 1200.0)


    def test_extract_tax_info_none(self):
        result = extract_tax_info_from_text("Detta är en testtext utan belopp.")
        self.assertIsNone(result["timtaxa"])
        self.assertIsNone(result["debiteringsmodell"])


if __name__ == "__main__":
    unittest.main()
