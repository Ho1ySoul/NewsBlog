from django.contrib.auth.models import User
from django.test import TestCase

from news.models import Category, News


class UrlsTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category1 = Category.objects.create(pk=1, title="category1")

        cls.user1 = User.objects.create(pk=1, username='user1')
        cls.user1.set_password('12itcom12')
        cls.user1.save()

        cls.news1 = News.objects.create(pk=1, title='news1', author=cls.user1,
                                        category=cls.category1)

    def setUp(self):
        self.URLS = [
            '/categorys/',
            '/categorys/1',
            '/news/',
            '/news/1',
            '/auth/',
            '/auth/users/'
            '/auth/users/me/'
            '/auth/users/1/'
            '/auth/token/login/'
            '/auth/token/logout/'
        ]

    def test_urls(self):
        for url in self.URLS:
            status = self.client.get(url)
            self.assertTrue(status != 404)
