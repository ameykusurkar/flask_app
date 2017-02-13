from app import app

import unittest

class AppTestCase(unittest.TestCase):
    def test_hello(self):
        test_app = app.test_client()
        response = test_app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'{"hello": "world"}')

if __name__ == '__main__':
    unittest.main()
