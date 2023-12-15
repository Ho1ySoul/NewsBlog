import json

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from ..models import Category


class CategoryViewTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.no_user = APIClient()

        cls.user1 = User.objects.create(pk=1, username='user1')
        token = Token.objects.create(user=cls.user1)
        cls.client_self = APIClient()
        cls.client_self.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        cls.admin_user = User.objects.create(pk=2, username='admin',
                                             is_staff=True)
        token = Token.objects.create(user=cls.admin_user)
        cls.admin_user = APIClient()
        cls.admin_user.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        cls.url = reverse('categories-list')

        cls.CATEGORIES_ID = [1, 2]

    def setUp(self):
        self.category1 = Category.objects.create(pk=1, title='category1')
        self.category1 = Category.objects.create(pk=2, title='category2')

    def test_get_categories(self):
        """ Получает список всех категорий """
        self.INFO_FOR_GET = (
            {
                'client': self.no_user,
                'code': 200,
            },
            {
                'client': self.client_self,
                'code': 200,
            },
            {
                'client': self.admin_user,
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
                        f' {news.get("id")} : {news}'
                    )
                ):
                    id = news.get('id')
                    self.assertTrue(id in self.CATEGORIES_ID)

    def test_get_single_category(self):
        """ Получает одну категорию """
        self.INFO_FOR_GET = (
            {
                'client': self.no_user,
                'code': 200,
            },
            {
                'client': self.client_self,
                'code': 200,
            },
            {
                'client': self.admin_user,
                'code': 200,
            }
        )
        for info in self.INFO_FOR_GET:
            response = info['client'].get(self.url + '1/')
            self.assertEqual(response.status_code, info['code'])
            self.assertEqual(response.data.get('id'), 1)

    def test_post_category(self):
        """ Создать категорию может только админ """
        self.INFO_FOR_POST = (
            {
                'client': self.no_user,
                'code': 401,
            },
            {
                'client': self.client_self,
                'code': 403,
            },
            {
                'client': self.admin_user,
                'code': 201,
            }
        )
        for info in self.INFO_FOR_POST:
            response = info['client'].post(self.url,
                                           {'title': 'some_category'})
            self.assertEqual(response.status_code, info['code'])
        self.assertTrue(Category.objects.get(pk=3))

        self.assertEqual(
            Category.objects.get(pk=3).title, 'some_category'
        )

    def test_delete_category(self):
        """ Удалить категорию может только админ """
        self.INFO_FOR_DELETE = (
            {
                'client': self.no_user,
                'code': 401,
            },
            {
                'client': self.client_self,
                'code': 403,
            },
            {
                'client': self.admin_user,
                'code': 204,
            }
        )
        for info in self.INFO_FOR_DELETE:
            response = info['client'].delete(self.url + '1/', )
            self.assertEqual(response.status_code, info['code'])

        self.assertEqual(Category.objects.all().count(), 1)

    def test_patch_category(self):
        """ Изменить часть категории может только админ """
        self.INFO_FOR_PATCH = (
            {
                'client': self.no_user,
                'code': 401,
            },
            {
                'client': self.client_self,
                'code': 403,
            },
            {
                'client': self.admin_user,
                'code': 200,
            }
        )
        data = json.dumps({'title': 'mynewtitle'})
        for info in self.INFO_FOR_PATCH:
            response = info['client'].patch(self.url + '1/', data,
                                            content_type='application/json')
            self.assertEqual(response.status_code, info['code'])

        self.assertEqual(
            Category.objects.get(pk=1).title, 'mynewtitle'
        )

    def test_put_category(self):
        """ Изменить всю категорию может только админ """
        self.INFO_FOR_PUT = (
            {
                'client': self.no_user,
                'code': 401,
            },
            {
                'client': self.client_self,
                'code': 403,
            },
            {
                'client': self.admin_user,
                'code': 200,
            }
        )
        data = json.dumps({'title': 'mynewtitle'})
        for info in self.INFO_FOR_PUT:
            response = info['client'].put(self.url + '1/', data,
                                          content_type='application/json')
            self.assertEqual(response.status_code, info['code'])

        self.assertEqual(
            Category.objects.get(pk=1).title, 'mynewtitle'
        )
