from unittest import TestCase

from django.test import Client


class ApiTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
        response = self.client.get('News.news')
        self.assertEqual(response.status_code, 200)
