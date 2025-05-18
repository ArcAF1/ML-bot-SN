import unittest
from unittest.mock import patch

from kommuncrawler import crawler


class TestCrawler(unittest.TestCase):
    def test_crawl_site_depth_and_internal_links(self):
        html_index = '<a href="/page2">next</a><a href="http://ext.com">ext</a>'
        html_page2 = 'page2'
        mapping = {
            'http://example.com': html_index,
            'http://example.com/page2': html_page2,
        }

        def fake_fetch(url):
            return mapping.get(url, '')

        with patch('kommuncrawler.crawler._fetch', side_effect=fake_fetch):
            pages = crawler.crawl_site(
                'http://example.com',
                max_depth=1,
                max_pages_per_level=5,
                use_concurrent=False,
            )

        urls = [u for _, u in pages]
        self.assertIn('http://example.com', urls)
        self.assertIn('http://example.com/page2', urls)
        self.assertNotIn('http://ext.com', urls)
        self.assertEqual(len(urls), 2)


    def test_concurrent_failure_logs_warning(self):
        with patch('kommuncrawler.crawler._crawl_concurrent', side_effect=Exception('boom')):
            with self.assertLogs(crawler.logger, level='WARNING') as cm:
                crawler.crawl_site('http://example.com', use_concurrent=True)
        self.assertTrue(any('Concurrent crawl failed' in msg for msg in cm.output))

    def test_fetch_pdf_returns_extracted_text(self):
        class FakeResp:
            def __init__(self):
                self.headers = {'Content-Type': 'application/pdf'}

            def read(self):
                return b'%PDF-1.4 dummy'

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                pass

            def get_content_charset(self):
                return None

        with patch('kommuncrawler.crawler.urlopen', return_value=FakeResp()), \
             patch('kommuncrawler.crawler.pdf_extract_text', return_value='hello'):
            text = crawler._fetch('http://example.com/test.pdf')

        self.assertEqual(text, 'hello')

    def test_fetch_pdf_detects_extension(self):
        class FakeResp:
            def __init__(self):
                self.headers = {}

            def read(self):
                return b'%PDF-1.4 dummy'

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                pass

            def get_content_charset(self):
                return None

        with patch('kommuncrawler.crawler.urlopen', return_value=FakeResp()), \
             patch('kommuncrawler.crawler.pdf_extract_text', return_value='bye'):
            text = crawler._fetch('http://example.com/doc.pdf')

        self.assertEqual(text, 'bye')



if __name__ == '__main__':
    unittest.main()
