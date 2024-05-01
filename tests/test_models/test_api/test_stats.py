import unittest
from api.v1.views.index import stats
from unittest.mock import patch
from flask import Flask


class TestStatsEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    @patch('api.v1.views.index.storage')
    def test_stats_endpoint(self, mock_storage):
        mock_storage.count.side_effect = {
            'Amenity': 47, 'City': 36, 'Place': 154, 'Review': 718,
            'State': 27, 'User': 31}.get
        response = self.client.get('/api/v1/stats')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['amenities'], 47)
        self.assertEqual(data['cities'], 36)
        self.assertEqual(data['places'], 154)
        self.assertEqual(data['reviews'], 718)
        self.assertEqual(data['states'], 27)
        self.assertEqual(data['users'], 31)


if __name__ == '__main__':
    unittest.main()
