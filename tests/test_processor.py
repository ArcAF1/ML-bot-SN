import unittest
from unittest.mock import patch
from kommuncrawler import processor


class TestProcessor(unittest.TestCase):
    def test_process_municipality_selects_best(self):
        fake_pages = [('text1', 'url1'), ('text2', 'url2')]

        def fake_crawl(url, max_depth=2, max_pages_per_level=20):
            return fake_pages

        def fake_extract(text):
            return {
                'timtaxa': 100 if text == 'text2' else 50,
                'debiteringsmodell': 'efteråt',
                'confidence': 0.9 if text == 'text2' else 0.2,
            }

        with patch('kommuncrawler.processor.crawl_site', side_effect=fake_crawl), \
             patch('kommuncrawler.processor.extract_tax_info_from_text', side_effect=fake_extract):
            result = processor.process_municipality('Test', 'http://example.com')

        self.assertEqual(result['data']['timtaxa'], 100)
        self.assertEqual(result['data']['källa'], 'url2')
        self.assertGreater(result['data']['confidence'], 0.8)

    def test_process_municipality_passes_depth_options(self):
        called = {}

        def fake_crawl(url, max_depth=2, max_pages_per_level=20):
            called['depth'] = max_depth
            called['pages'] = max_pages_per_level
            return [('text', url)]

        def fake_extract(text):
            return {'timtaxa': None, 'debiteringsmodell': None, 'confidence': 0}

        with patch('kommuncrawler.processor.crawl_site', side_effect=fake_crawl), \
             patch('kommuncrawler.processor.extract_tax_info_from_text', side_effect=fake_extract):
            processor.process_municipality(
                'Test',
                'http://example.com',
                max_depth=5,
                max_pages_per_level=7,
            )

        self.assertEqual(called['depth'], 5)
        self.assertEqual(called['pages'], 7)


if __name__ == '__main__':
    unittest.main()
