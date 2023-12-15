import json

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from ..models import Category, News, UserNewsRelation


class NewsViewTestCase(APITestCase):
    admin_client = None
    user1 = None
    admin_user = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse('news-list')

        cls.category1 = Category.objects.create(pk=1, title='category1')

        cls.guest_client = APIClient()

        cls.user1 = User.objects.create(pk=1, username='user1')
        token = Token.objects.create(user=cls.user1)
        cls.simple_user_client = APIClient()
        cls.simple_user_client.credentials(
            HTTP_AUTHORIZATION='Token ' + token.key)

        cls.admin_user = User.objects.create(pk=2, username='admin',
                                             is_staff=True)
        token = Token.objects.create(user=cls.admin_user)
        cls.admin_client = APIClient()
        cls.admin_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        cls.NEWS_TITLE = {
            'news1',
            'news2'
        }

    def setUp(self):
        self.news1 = News.objects.create(pk=1, title='news1',
                                         author=self.user1,
                                         category=self.category1)
        self.news2 = News.objects.create(pk=2, title='news2',
                                         author=self.user1,
                                         category=self.category1)
        self.user_news_relation1 = (
            UserNewsRelation.objects.create(pk=1,
                                            user=self.user1,
                                            news=self.news1,
                                            like=True)
        )

    def test_get_all_news(self):
        """ Получает список всех новостей """
        self.INFO_FOR_GET = (
            {
                'client': self.guest_client,
                'code': 200,
            },
            {
                'client': self.simple_user_client,
                'code': 200,
            },
            {
                'client': self.admin_client,
                'code': 200,
            }
        )
        for info in self.INFO_FOR_GET:
            response = info['client'].get(self.url)
            self.assertEqual(response.status_code, info['code'])
            self.assertEqual(response.data['count'], 2)

            for news in response.data['results']:
                with (
                    self.subTest(
                        f'Получили новость с несуществующим id'
                        f' {news.get("title")} : {news}'
                    )
                ):
                    id = news.get('title')
                    self.assertTrue(id in self.NEWS_TITLE)

    def test_get_single_news(self):
        """ Получает одну новость """
        self.INFO_FOR_GET = (
            {
                'client': self.guest_client,
                'code': 200,
            },
            {
                'client': self.simple_user_client,
                'code': 200,
            },
            {
                'client': self.admin_client,
                'code': 200,
            }
        )
        for info in self.INFO_FOR_GET:
            response = info['client'].get(self.url + '1/')
            self.assertEqual(response.status_code, info['code'])
            self.assertEqual(response.data.get('title'), 'news1')
            a = response.data.get('author')
            self.assertEqual(a.get('id'), self.user1.id)

    def test_post_category(self):
        """ Создать категорию может только админ """
        self.INFO_FOR_POST = (
            {
                'client': self.guest_client,
                'code': 401,
            },
            {
                'client': self.simple_user_client,
                'code': 201,
            },
            {
                'client': self.admin_client,
                'code': 201,
            }
        )
        for info in self.INFO_FOR_POST:
            response = info['client'].post(self.url,
                                           {'title': 'title_new_news',
                                            'content': 'content_new_news',
                                            'category': 1})
            self.assertEqual(response.status_code, info['code'])
        self.assertTrue(News.objects.get(pk=3))

        self.assertEqual(
            News.objects.get(pk=3).title, 'title_new_news'
        )
        self.assertEqual(
            News.objects.all().count(), 4,
            'Создаётся 2 новости,'
            ' первая от авторизованого пользователя,'
            ' вторая от админа '
        )

    def test_delete_category(self):
        """ Удалить новость может только её автор"""
        self.INFO_FOR_DELETE = (
            {
                'client': self.guest_client,
                'code': 401,
            },
            {
                'client': self.admin_client,
                'code': 403,
            },
            {
                'client': self.simple_user_client,
                'code': 204,
            },

        )
        for info in self.INFO_FOR_DELETE:
            response = info['client'].delete(self.url + '1/', )
            self.assertEqual(response.status_code, info['code'])

        self.assertEqual(News.objects.all().count(), 1)

    def test_patch_category(self):
        """ Изменить часть новости может только админ """
        self.INFO_FOR_PATCH = (
            {
                'client': self.guest_client,
                'code': 401,
            },
            {
                'client': self.admin_client,
                'code': 403,
            },
            {
                'client': self.simple_user_client,
                'code': 200,
            },
        )
        data = json.dumps({'title': 'mynewtitle'})
        for info in self.INFO_FOR_PATCH:
            response = info['client'].patch(self.url + '1/', data,
                                            content_type='application/json')
            self.assertEqual(response.status_code, info['code'])

        self.assertEqual(
            News.objects.get(pk=1).title, 'mynewtitle'
        )

    def test_put_category(self):
        """ Изменить всю новость может только автор """
        self.INFO_FOR_PUT = (
            {
                'client': self.guest_client,
                'code': 401,
            },
            {
                'client': self.admin_client,
                'code': 403,
            },
            {
                'client': self.simple_user_client,
                'code': 200,
            },
        )
        data = json.dumps({'title': 'mynew_title',
                           'content': 'mynewcontent',
                           'category': self.category1.pk})
        for info in self.INFO_FOR_PUT:
            response = info['client'].put(self.url + '1/', data,
                                          content_type='application/json')
            self.assertEqual(response.status_code, info['code'])

        self.assertEqual(
            News.objects.get(pk=1).title, 'mynew_title'
        )
        self.assertEqual(
            News.objects.get(pk=1).content, 'mynewcontent'
        )
        self.assertEqual(
            News.objects.get(pk=1).category, self.category1
        )
