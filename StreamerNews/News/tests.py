from django.contrib.auth.models import User
from django.test import TestCase, Client
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from News.models import News, Category, NewsQuerySet, UserNewsRelation
from News.serializers import NewsSerializer


class NewsTestCase(TestCase):

    def setUp(self):
        # self.client.post('/auth/users/',
        #                  {"username": "username2",
        #                   "password": "12itcom12",
        #                   "email": "1@mail.ru",
        #                   "first_name": "d",
        #                   "last_name": "ddd", }
        #                  )
        # self.client.login(username="username2",
        #                   password="12itcom12")

        self.user1 = User.objects.create(pk=1, username='user1')
        self.user1.set_password('12itcom12')
        self.user1.save()

        self.category1 = Category.objects.create(pk=1, title="category1")
        self.news1 = News.objects.create(pk=1, title="news1", author=self.user1,
                                         category=self.category1)
        self.news2 = News.objects.create(pk=2, title="news2", author=self.user1,
                                         category=self.category1)
        self.usernewsrelation1 = UserNewsRelation.objects.create(pk=1,
                                                                 user=self.user1, news=self.news1, like=False)
        self.user1_token = self.client.post('/auth/token/login/',
                                            {"username": "user1",
                                             "password": "12itcom12"}
                                            ).json()["auth_token"]

    def test_correctly_user_login(self):
        client_me = self.client.get("/auth/users/me/", headers={"Authorization": "Token " + self.user1_token})
        print(client_me.json())
        self.assertEqual(client_me.status_code, 200)
        self.assertEqual(client_me.json()["username"], "user1")

    def test_uncorrectly_login(self):
        client_post = self.client.post('/auth/token/login/',
                                       {"username": "usedas2",
                                        "password": "12itcom12"}
                                       )
        self.assertEqual(client_post.status_code, 400)

    def test_logout(self):
        self.client.login(username="user1",
                          password="12itcom12")
        client_post = self.client.post('/auth/token/logout/')
        self.assertEqual(client_post.status_code, 204)

    def test_get_news(self):
        news = self.client.get("/news/")
        self.assertEqual(news.status_code, 200)
        self.assertEqual(news.data["count"], 2)

    def test_get_single_news(self):
        news1 = self.client.get("/news/1/")
        self.assertEqual(news1.status_code, 200)
        self.assertEqual(news1.json()["title"], "news1")

    def test_post_news_with_login(self):
        new_news = self.client.post("/news/", {"title": "title_new_news",
                                               "content": "content_new_news",
                                               },
                                    headers={"Authorization": "Token " + self.user1_token})

        self.assertEqual(new_news.status_code, 200)
