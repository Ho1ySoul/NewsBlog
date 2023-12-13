from django.contrib.auth.models import User
from django.test import TestCase, Client
from rest_framework import status
from rest_framework.reverse import reverse

from News.models import News, Category, NewsQuerySet, UserNewsRelation
from News.serializers import NewsSerializer


class NewsTestCase(TestCase):

    def setUp(self):
        self.client.post('/auth/users/',
                         {"username": "username2",
                          "password": "12itcom12",
                          "email": "1@mail.ru",
                          "first_name": "d",
                          "last_name": "ddd", }
                         )
        self.client.login(username="username2",
                          password="12itcom12")


        self.user1 = User.objects.create(username='user1',
                                         password="12itcom12")
        self.category1 = Category.objects.create(title="category1")
        self.news1 = News.objects.create(title="news1", author=self.user1,
                                         category=self.category1)
        self.news2 = News.objects.create(title="news2", author=self.user1,
                                         category=self.category1)
        self.usernewsrelation1 = UserNewsRelation.objects.create(
            user=self.user1, news=self.news1, like=False)

    def test1(self):
        url = reverse('news-list')
        response = self.client.get(url)
        # news = News.objects.with_readers_count().with_author_full_name().with_is_like()
        news = self.client.get("/news/")
        news1 = self.client.get("/news/1/")
        # serializer_data = NewsSerializer(news, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # self.assertEqual(serializer_data[0]["title"], "news1")
        # self.assertEqual(news, "news1")
        self.assertEqual(news1.json()["title"], "news1")
    # def setUp(self):
    #     self.client.post('/auth/users/',
    #                      {"username": "username2",
    #                       "password": "12itcom12",
    #                       "email": "1@mail.ru",
    #                       "first_name": "d",
    #                       "last_name": "ddd", }
    #                      )
    #     # self.client.login(username="username2",
    #     #                                              password="12itcom12")
    #     # self.client.post('/categorys/', {"title": "category1"})
    #
    # def test_ckech(self):
    #     login = self.client.login(username="username2",
    #                       password="12itcom12")
    #
    #     b = self.client.post('/categorys/', {"title": "category1"})
    #     c = self.client.get('/categorys/1/')
    #     self.assertEqual(b.status_code, 201)
    #     self.assertTrue(login)
    #     self.assertEqual(c.status_code, 200)
    # def test_correctly_login(self):
    #     client_post = self.client.post('/auth/token/login/',
    #                                    {"username": "username2",
    #                                     "password": "12itcom12", }
    #                                    )
    #
    #     self.assertEqual(client_post.status_code, 200)
    #
    # def test_uncorrectly_login(self):
    #     client_post = self.client.post('/auth/token/login/',
    #                                    {"username": "username222",
    #                                     "password": "12itcom1d2", }
    #                                    )
    #
    #     self.assertEqual(client_post.status_code, 400)
    #
    # def test_logout(self):
    #     self.client.login(username="username2",
    #                       password="12itcom12")
    #     client_post = self.client.post('/auth/token/logout/')
    #     self.assertEqual(client_post.status_code, 204)
    #
    # def test_get_news(self):
    #     news = self.client.get('/news/')
    #     self.assertEqual(news.status_code, 200)
    #
    # def test_post_news_without_login(self):
    #     a = self.client.post('/news/', {"title": "title2",
    #                                     "author": self.client.get(
    #                                         '/auth/users/me'),
    #                                     "category": self.client.get(
    #                                         '/categorys/0')})
    #     self.assertEqual(a.status_code, 401)

    # def test_post_news_with_login(self):
    #     self.client.login(username="username2",
    #                           password="12itcom12")
    #     b = self.client.get('/categorys/0')
    #     a = self.client.post('/news/', {"title": "title22",
    #                                     # "author": self.client.get('/auth/users/me'),
    #                                     "content": "content1",
    #                                     "category": self.client.get('/categorys/id/0'),
    #                                     "is_active": True,
    #                                     # "date_created":"",
    #                                     # "like":False
    #                                     })
    #     print("YA TYT")
    #     print(b.json())
    #     self.assertEqual(b.status_code, 200)

    # self.assertEqual(self.client.get('/news/1'), 1)
