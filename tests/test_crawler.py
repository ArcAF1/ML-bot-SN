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
            pages = crawler.crawl_site('http://example.com', max_depth=1)

        urls = [u for _, u in pages]
        self.assertIn('http://example.com', urls)
        self.assertIn('http://example.com/page2', urls)
        self.assertNotIn('http://ext.com', urls)
        self.assertEqual(len(urls), 2)

    def test_crawl_site_pages_per_level_limit(self):
        html_index = (
            '<a href="/p1">p1</a>'
            '<a href="/p2">p2</a>'
            '<a href="/p3">p3</a>'
        )
        mapping = {
            'http://example.com': html_index,
            'http://example.com/p1': 'p1',
            'http://example.com/p2': 'p2',
            'http://example.com/p3': 'p3',
        }

        def fake_fetch(url):
            return mapping.get(url, '')

        with patch('kommuncrawler.crawler._fetch', side_effect=fake_fetch):
            pages = crawler.crawl_site(
                'http://example.com',
                max_depth=1,
                max_pages_per_level=1,
            )

        urls = [u for _, u in pages]
        # Only index and first page should be crawled
        self.assertIn('http://example.com', urls)
        self.assertIn('http://example.com/p1', urls)
        self.assertEqual(len(urls), 2)


if __name__ == '__main__':
    unittest.main()
