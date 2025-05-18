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



    def test_crawl_site_concurrent_exception_warning(self):
        with patch('kommuncrawler.crawler._crawl_concurrent', side_effect=ValueError('boom')), \
             patch('kommuncrawler.crawler._crawl_sync', return_value=[('t', 'u')]) as mock_sync, \
             patch('kommuncrawler.crawler.logger.warning') as mock_warn:
            pages = crawler.crawl_site('http://example.com', use_concurrent=True)

        self.assertEqual(pages, [('t', 'u')])
        mock_sync.assert_called_once()
        mock_warn.assert_called_once()
        args = mock_warn.call_args[0]
        self.assertEqual(args[0], 'Concurrent crawl failed for %s: %s')
        self.assertEqual(args[1], 'http://example.com')
        self.assertIn('boom', str(args[2]))


if __name__ == '__main__':
    unittest.main()
