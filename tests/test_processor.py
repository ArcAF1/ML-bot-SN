import unittest
from unittest.mock import patch
from kommuncrawler import processor


class TestProcessor(unittest.TestCase):
    def test_process_municipality_selects_best(self):
        fake_pages = [('text1', 'url1'), ('text2', 'url2')]

        def fake_crawl(url):
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


if __name__ == '__main__':
    unittest.main()
