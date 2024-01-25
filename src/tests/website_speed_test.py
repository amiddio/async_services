import unittest
import requests
import os

from dotenv import load_dotenv

load_dotenv()


class WebsiteSpeedTest(unittest.TestCase):
    domain = 'localhost'
    port = int(os.environ.get('PORT'))

    def test_service(self):
        url = f"http://{self.domain}:{self.port}/website_speed?url=https://example.com&times=10"
        response = requests.get(url)
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
