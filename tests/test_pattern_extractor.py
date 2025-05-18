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

    def test_extract_tax_info_avgift_per_timme(self):
        text = "Avgift per timme 900 kronor."
        result = extract_tax_info_from_text(text)
        self.assertEqual(result["timtaxa"], 900.0)

    def test_extract_tax_info_timpris(self):
        text = "Timpris är 1 100 kr."
        result = extract_tax_info_from_text(text)
        self.assertEqual(result["timtaxa"], 1100.0)

    def test_extract_tax_info_none(self):
        result = extract_tax_info_from_text("Detta är en testtext utan belopp.")
        self.assertIsNone(result["timtaxa"])
        self.assertIsNone(result["debiteringsmodell"])


if __name__ == "__main__":
    unittest.main()
