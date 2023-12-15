import json

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from ..models import Category


class CategoryViewTestCase(APITestCase):
    client = APIClient()
    client.credentials()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        no_user = APIClient()

        user1 = User.objects.create(pk=1, username='user1')
        token = Token.objects.create(user=user1)
        client_user1 = APIClient()
        client_user1.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        admin_user = User.objects.create(pk=2, username='admin', is_staff=True)
        token = Token.objects.create(user=admin_user)
        admin_user = APIClient()
        admin_user.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        cls.url = reverse('categories-list')

        cls.CATEGORIES_ID = [1, 2]

        cls.INFO_FOR_GET = (
            {
                "client": no_user,
                "code": 200,
            },
            {
                "client": client_user1,
                "code": 200,
            },
            {
                "client": admin_user,
                "code": 200,
            }
        )

        cls.INFO_FOR_POST = (
            {
                "client": no_user,
                "code": 401,
            },
            {
                "client": client_user1,
                "code": 403,
            },
            {
                "client": admin_user,
                "code": 201,
            }
        )
        cls.INFO_FOR_DELETE = (
            {
                "client": no_user,
                "code": 401,
            },
            {
                "client": client_user1,
                "code": 403,
            },
            {
                "client": admin_user,
                "code": 204,
            }
        )
        cls.INFO_FOR_PATCH = (
            {
                "client": no_user,
                "code": 401,
            },
            {
                "client": client_user1,
                "code": 403,
            },
            {
                "client": admin_user,
                "code": 200,
            }
        )
        cls.INFO_FOR_PUT = (
            {
                "client": no_user,
                "code": 401,
            },
            {
                "client": client_user1,
                "code": 403,
            },
            {
                "client": admin_user,
                "code": 200,
            }
        )

        # cls.TOKENS_GET = {
        #     "Token ": 200,
        #     "Token " + cls.user1_token.key: 200,
        #     "Token " + cls.admin_token.key: 200,
        # }
        #
        # cls.TOKENS_POST = {
        #     "Token ": 401,
        #     "Token " + cls.user1_token.key: 403,
        #     "Token " + cls.admin_token.key: 201,
        # }
        # cls.TOKENS_DELETE = {
        #     "Token ": 401,
        #     "Token " + cls.user1_token.key: 403,
        #     "Token " + cls.admin_token.key: 204,
        # }
        # cls.TOKENS_PATCH = {
        #     "Token ": 401,
        #     "Token " + cls.user1_token.key: 403,
        #     "Token " + cls.admin_token.key: 200,
        # }
        #
        # cls.TOKENS_PUT = {
        #     "Token ": 401,
        #     "Token " + cls.user1_token.key: 403,
        #     "Token " + cls.admin_token.key: 200,
        # }

    def setUp(self):
        self.category1 = Category.objects.create(pk=1, title="category1")
        self.category1 = Category.objects.create(pk=2, title="category2")

    # def test_get_categories(self):
    #     for token, code in self.TOKENS_GET.items():
    #         with self.subTest(f'{token}:{code}'):
    #             categories_client = self.client.get(
    #                 self.url,
    #                 {"Authorization": token}
    #             )
    #             self.assertEqual(categories_client.status_code, code)
    #             self.assertEqual(categories_client.data["count"], 2)
    #
    #             for a in categories_client.data["results"]:
    #                 with self.subTest(f'TYT: {a["title"]}'):
    #                     self.assertTrue(a["title"] in self.categories_NAME)

    def test_get_categories(self):
        ''' Тест проверяет, сможет ли мы получить список всех категорий, их кол-во и правильность'''
        for info in self.INFO_FOR_GET:
            response = info['client'].get(self.url)
            self.assertEqual(response.status_code, info['code'])
            self.assertEqual(response.data['count'], 2)

            for news in response.data['results']:
                with (
                    self.subTest(
                        f'Получили новость с несуществующим id'
                        f' {news.get('id')} : {news}'
                    )
                ):
                    id = news.get('id')
                    self.assertTrue(id in self.CATEGORIES_ID)

    def test_get_single_category(self):
        ''' Тест проверяет: сможет ли пользователь получить одну определённуюю категорию по id'''
        for info in self.INFO_FOR_GET:
            response = info['client'].get(self.url + '1/')
            self.assertEqual(response.status_code, info['code'])
            self.assertEqual(response.data.get('id'), 1)

    def test_post_category(self):
        '''Тест проверяеn: сможет ли только админ добавить категорию'''
        for info in self.INFO_FOR_POST:
            response = info['client'].post(self.url,
                                           {'title': 'some_category'})
            self.assertEqual(response.status_code, info['code'])
        self.assertTrue(Category.objects.get(pk=3))
        self.assertEqual(Category.objects.get(pk=3).title, 'some_category')

    def test_delete_category(self):
        '''Тест проверяеn: сможет ли только админ удалить категорию'''
        for info in self.INFO_FOR_DELETE:
            response = info['client'].delete(self.url + '1/', )
            self.assertEqual(response.status_code, info['code'])
        self.assertEqual(Category.objects.all().count(), 1)

    def test_patch_category(self):
        '''Тест проверяеn: сможет ли только админ изменить часть категории'''
        data = json.dumps({"title": "mynewtitle"})
        for info in self.INFO_FOR_PATCH:
            response = info['client'].patch(self.url + '1/', data,
                                           content_type="application/json")
            self.assertEqual(response.status_code, info['code'])
        self.assertEqual(Category.objects.get(pk=1).title,"mynewtitle")

    def test_put_category(self):
        '''Тест проверяеn: сможет ли только админ изменить всю категорию'''
        data = json.dumps({"title": "mynewtitle"})
        for info in self.INFO_FOR_PUT:
            response = info['client'].put(self.url + '1/', data,
                                           content_type="application/json")
            self.assertEqual(response.status_code, info['code'])
        self.assertEqual(Category.objects.get(pk=1).title,"mynewtitle")



    # def test_post_category(self):
    #     for token, code in self.TOKENS_POST.items():
    #         with self.subTest(f'{token}:{code}'):
    #             categories_client = (
    #                 self.client.post(self.url,
    #                                  {"title": "SomeCategory"},
    #                                  headers={"Authorization": token})
    #             )
    #             self.assertEqual(categories_client.status_code, code)
    #     self.assertEqual(Category.objects.all().count(), 3)
    #     self.assertEqual(
    #         Category.objects.get(pk=3).title,
    #         "SomeCategory"
    #     )
    #
    # def test_delete_category(self):
    #     for token, code in self.TOKENS_DELETE.items():
    #         with (self.subTest(f'{token}:{code}')):
    #             categories_client = (
    #                 self
    #                 .client
    #                 .delete(self.url + "1/",
    #                         headers={"Authorization": token})
    #             )
    #
    #             self.assertEqual(categories_client.status_code, code)
    #
    #     self.assertEqual(Category.objects.all().count(), 1)
    #
    # def test_path_category(self):
    #     data = json.dumps({"title": "mynewtitle"})
    #     for token, code in self.TOKENS_PATCH.items():
    #         with self.subTest(f'{token}:{code}'):
    #             categories_client = (
    #                 self
    #                 .client
    #                 .patch(self.url + "1/", data,
    #                        content_type='application/json',
    #                        headers={"Authorization": token})
    #             )
    #             self.assertEqual(categories_client.status_code, code)
    #     self.assertEqual(
    #         Category.objects.get(pk=1).title,
    #         "mynewtitle"
    #     )
    #
    # def test_put_category(self):
    #     data = json.dumps({"title": "mynewtitle"})
    #     for token, code in self.TOKENS_PUT.items():
    #         with self.subTest(f'{token}:{code}'):
    #             categories_client = (self
    #                                  .client
    #                                  .put(self.url + "1/", data,
    #                                       content_type='application/json',
    #                                       headers={"Authorization": token})
    #                                  )
    #             self.assertEqual(categories_client.status_code, code)
    #     self.assertEqual(
    #         Category.objects.get(pk=1).title,
    #         "mynewtitle"
    #     )
