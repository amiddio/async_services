import unittest
import requests
import json
import os

from dotenv import load_dotenv

load_dotenv()


class ParseTextTest(unittest.TestCase):
    url = f"http://localhost:{int(os.environ.get('PORT'))}/parse_text"
    books = [
        'https://tululu.org/txt.php?id=77440', 'https://tululu.org/txt.php?id=77441',
        'https://tululu.org/txt.php?id=77442', 'https://tululu.org/txt.php?id=77443',
    ]

    def test_service_general(self):
        data = {
            'urls': ','.join(self.books)
        }
        response = requests.post(self.url, data=data)

        self.assertEqual(200, response.status_code)

    def test_service_with_limit(self):
        data = {
            'urls': ','.join(self.books),
            'limit': 10,
        }
        response = requests.post(self.url, data=data)

        self.assertEqual(200, response.status_code)
        data_dct = json.loads(response.text)
        self.assertEqual(10, len(data_dct.get('data')))

    def test_service_words_only(self):
        data = {
            'urls': ','.join(self.books),
            'include_words_only': 'княжна,наполеон,мы,война,мир,государь',
        }
        response = requests.post(self.url, data=data)

        self.assertEqual(200, response.status_code)
        data_dct = json.loads(response.text)
        self.assertEqual(6, len(data_dct.get('data')))


if __name__ == '__main__':
    unittest.main()
