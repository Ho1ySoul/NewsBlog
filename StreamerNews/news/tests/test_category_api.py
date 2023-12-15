import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework.authtoken.models import Token

from ..models import Category


class CategoryViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse('categories-list')
        user1 = User.objects.create(pk=1, username='user1')
        user1.set_password('12itcom12')
        user1.save()
        cls.user1_token = Token.objects.create(user=user1)

        admin_user = User.objects.create(pk=2, username='admin', is_staff=True)
        admin_user.set_password('12itcom12')
        admin_user.save()
        cls.admin_token = Token.objects.create(user=admin_user)

        cls.TOKENS_GET = {
            "Token ": 200,
            "Token " + cls.user1_token.key: 200,
            "Token " + cls.admin_token.key: 200,
        }

        cls.TOKENS_POST = {
            "Token ": 401,
            "Token " + cls.user1_token.key: 403,
            "Token " + cls.admin_token.key: 201,
        }
        cls.TOKENS_DELETE = {
            "Token ": 401,
            "Token " + cls.user1_token.key: 403,
            "Token " + cls.admin_token.key: 204,
        }
        cls.TOKENS_PATCH = {
            "Token ": 401,
            "Token " + cls.user1_token.key: 403,
            "Token " + cls.admin_token.key: 200,
        }

        cls.TOKENS_PUT = {
            "Token ": 401,
            "Token " + cls.user1_token.key: 403,
            "Token " + cls.admin_token.key: 200,
        }

    def setUp(self):
        self.category1 = Category.objects.create(pk=1, title="category1")
        self.category1 = Category.objects.create(pk=2, title="category2")

        self.categories_NAME = ["category1", 'category2']

    def test_get_categories(self):
        for token, code in self.TOKENS_GET.items():
            with self.subTest(f'{token}:{code}'):
                categories_client = self.client.get(
                    self.url,
                    {"Authorization": token}
                )
                self.assertEqual(categories_client.status_code, code)
                self.assertEqual(categories_client.data["count"], 2)

                for a in categories_client.data["results"]:
                    with self.subTest(f'TYT: {a['title']=}'):
                        self.assertTrue(a["title"] in self.categories_NAME)

    def test_get_single_category(self):
        for token, code in self.TOKENS_GET.items():
            with (self.subTest(f'{token}:{code}')):
                categories_client = self.client.get(
                    self.url + "1/",
                    {"Authorization": token}
                )
                self.assertEqual(categories_client.status_code, code)
                self.assertEqual(
                    categories_client.data["title"],
                    "category1"
                )

    def test_post_category(self):
        for token, code in self.TOKENS_POST.items():
            with self.subTest(f'{token}:{code}'):
                categories_client = (
                    self.client.post(self.url,
                                     {"title": "SomeCategory"},
                                     headers={"Authorization": token})
                )
                self.assertEqual(categories_client.status_code, code)
        self.assertEqual(Category.objects.all().count(), 3)
        self.assertEqual(
            Category.objects.get(pk=3).title,
            "SomeCategory"
        )

    def test_delete_category(self):
        for token, code in self.TOKENS_DELETE.items():
            with (self.subTest(f'{token}:{code}')):
                categories_client = (
                    self
                    .client
                    .delete(self.url + "1/",
                            headers={"Authorization": token})
                )

                self.assertEqual(categories_client.status_code, code)

        self.assertEqual(Category.objects.all().count(), 1)

    def test_path_category(self):
        data = json.dumps({"title": "mynewtitle"})
        for token, code in self.TOKENS_PATCH.items():
            with self.subTest(f'{token}:{code}'):
                categories_client = (
                    self
                    .client
                    .patch(self.url + "1/", data,
                           content_type='application/json',
                           headers={"Authorization": token})
                )
                self.assertEqual(categories_client.status_code, code)
        self.assertEqual(
            Category.objects.get(pk=1).title,
            "mynewtitle"
        )

    def test_put_category(self):
        data = json.dumps({"title": "mynewtitle"})
        for token, code in self.TOKENS_PUT.items():
            with self.subTest(f'{token}:{code}'):
                categories_client = (self
                                     .client
                                     .put(self.url + "1/", data,
                                          content_type='application/json',
                                          headers={"Authorization": token})
                                     )
                self.assertEqual(categories_client.status_code, code)
        self.assertEqual(
            Category.objects.get(pk=1).title,
            "mynewtitle"
        )
