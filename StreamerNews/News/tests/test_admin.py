from News.admin import NewsAdmin
import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token

from News.models import Category, News
from django.test import Client


# class AdminTestCase(TestCase):
#     def test_create_news_on_adminpanel(self):
#         user1 = User.objects.create_superuser(pk=1, username='user1')
#         user1.set_password('12itcom12')
#         user1.save()
#         category1 = Category.objects.create(pk=1, title="c1")
#         data = {"title": "1", "content": 'dadsadsad', "category": category1}
#         data1 = {"title": "2", "content": 'dadsadsad', "category": category1}
#         self.client.login(username="user1",
#                           password="12itcom12")
#         # self.news1 = News.objects.create(pk=1, title="news1", author=user1,
#         #                                  category=category1)
#
#         response = self.client.post("/admin/News/news/add/", data1, headers=)
#         self.assertEqual(response.redirect_chain, 200)
#         self.assertEqual(News.objects.all(), 'dddd')
