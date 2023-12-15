from unittest.mock import Mock

from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.test import TestCase

from news.admin import NewsAdmin
from news.models import Category, News


class AdminTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        site = AdminSite()
        cls.admin = NewsAdmin(News, site)
        cls.user1 = User.objects.create_superuser(pk=1, username='user1')
        cls.user1.set_password('12itcom12')
        cls.user1.save()

    def test_post_news_for_admin_panel(self):
        category1 = Category.objects.create(pk=1, title='c1')
        self.admin.save_model(obj=News(title='mydamintitle',
                                       content='my admin content',
                                       category=category1),
                              request=Mock(user=self.user1),
                              form=None, change=None)
        self.assertEqual(News.objects.get(pk=1).category.id, 1)
        self.assertEqual(News.objects.all().count(), 1)
