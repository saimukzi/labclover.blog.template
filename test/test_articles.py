import unittest
import json
import os
from jinja2 import Environment, FileSystemLoader
from _feature_articles import get_article_data

class TestArticles(unittest.TestCase):
    def setUp(self):
        self.env = Environment(loader=FileSystemLoader("test/templates"))

    def test_article_parsing_and_rendering(self):
        fn = 'test/articles/2024/07/20240723-test.txt'
        article_data = get_article_data(fn)
        meta_data = article_data['meta']
        content = article_data['content']

        self.assertEqual(meta_data['title'], '這是一個測試')
        self.assertEqual(meta_data['date'], '2024-07-23')

        render_data = {**meta_data, '__article__': content}
        template = self.env.get_template("test.html")
        rendered_html = template.render(render_data)

        self.assertIn('<title>這是一個測試</title>', rendered_html)
        self.assertIn('<h1>這是一個測試</h1>', rendered_html)
        self.assertIn('<p>這是第一段</p>', rendered_html)

if __name__ == '__main__':
    unittest.main()
