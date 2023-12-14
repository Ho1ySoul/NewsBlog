# import json
#
# from News.models import News, UserNewsRelation, Category
#
# from django.contrib.auth.models import User
# from django.test import TestCase
# from django.urls import reverse
# from rest_framework.authtoken.models import Token
#
#
# class NewsViewTestCase(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.url = reverse('news-list')
#         cls.category1 = Category.objects.create(pk=1, title="category1")
#
#         cls.user1 = User.objects.create(pk=1, username='user1')
#         cls.user1.set_password('12itcom12')
#         cls.user1.save()
#         cls.user1_token = Token.objects.create(user=cls.user1)
#
#         cls.admin_user = User.objects.create(pk=2, username='admin', is_staff=True)
#         cls.admin_user.set_password('12itcom12')
#         cls.admin_user.save()
#         cls.admin_token = Token.objects.create(user=cls.admin_user)
#
#         cls.TOKENS_GET = {
#             "Token ": 200,
#             "Token " + cls.user1_token.key: 200,
#             "Token " + cls.admin_token.key: 200,
#         }
#         cls.TOKENS_POST = {
#             "Token ": 401,
#             "Token " + cls.user1_token.key: 201,
#             "Token " + cls.admin_token.key: 201,
#         }
#         cls.TOKENS_DELETE = {
#             "Token ": 401,
#             "Token " + cls.admin_token.key: 403,
#             "Token " + cls.user1_token.key: 204,
#         }
#         cls.TOKENS_PATCH = {
#             "Token ": 401,
#             "Token " + cls.admin_token.key: 403,
#             "Token " + cls.user1_token.key: 200,
#         }
#         cls.TOKENS_PUT = {
#             "Token ": 401,
#             "Token " + cls.admin_token.key: 403,
#             "Token " + cls.user1_token.key: 200,
#
#         }
#
#         cls.NEWS_TITLE = {
#             "news1",
#             "news2"
#         }
#
#     def setUp(self):
#         self.news1 = News.objects.create(pk=1, title="news1", author=self.user1,
#                                          category=self.category1)
#         self.news2 = News.objects.create(pk=2, title="news2", author=self.user1,
#                                          category=self.category1)
#         self.user_news_relation1 = UserNewsRelation.objects.create(pk=1,
#                                                                    user=self.user1, news=self.news1, like=True)
#
#     def test_get_news(self):
#         for token, code in self.TOKENS_GET.items():
#             with self.subTest(f'{token}:{code}'):
#                 news_client = self.client.get(self.url, {"Authorization": token})
#                 self.assertEqual(news_client.status_code, code)
#                 self.assertEqual(news_client.data["count"], 2)
#                 for news_info in news_client.data["results"]:
#                     with self.subTest(f'TYT: {news_info['title']=}'):
#                         self.assertTrue(news_info["title"] in self.NEWS_TITLE)
#
#     def test_get_single_news(self):
#         for token, code in self.TOKENS_GET.items():
#             with self.subTest(f'{token}:{code}'):
#                 news_client = self.client.get(self.url + "1/", {"Authorization": token})
#                 self.assertEqual(news_client.status_code, code)
#                 self.assertEqual(news_client.data['title'], "news1")
#
#     def test_post_news(self):
#         for token, code in self.TOKENS_POST.items():
#             with self.subTest(f'{token}:{code}'):
#                 news_client = self.client.post(self.url, {"title": "title_new_news",
#                                                           "content": "content_new_news",
#                                                           "category": 1},
#                                                headers={"Authorization": token})
#                 self.assertEqual(news_client.status_code, code)
#         self.assertEqual(News.objects.all().count(),4)
#         self.assertEqual(News.objects.get(pk=3).title, 'title_new_news')
#         self.assertEqual(News.objects.get(pk=4).title, 'title_new_news')
#         self.assertEqual(News.objects.get(pk=3).content, 'content_new_news')
#         self.assertEqual(News.objects.get(pk=4).content, 'content_new_news')
#         self.assertEqual(News.objects.get(pk=3).category.pk, 1)
#         self.assertEqual(News.objects.get(pk=4).category.pk, 1)
#
#
#     def test_delete_news(self):
#         print(News.objects.all())
#         for token, code in self.TOKENS_DELETE.items():
#             with self.subTest(f'{token}:{code}'):
#                 news_client = self.client.delete(self.url + "1/",
#                                                  headers={"Authorization": token})
#                 self.assertEqual(news_client.status_code, code)
#         self.assertFalse(News.objects.filter(pk=1).exists())
#         self.assertEqual(News.objects.all().count(), 1)
#
#     def test_patch_news(self):
#         data = json.dumps({"title": "mynewtitle"})
#         print(News.objects.all())
#         for token, code in self.TOKENS_PATCH.items():
#             with self.subTest(f'{token}:{code}'):
#                 news_client = self.client.patch(self.url + "1/",
#                                                 data, content_type='application/json',
#                                                 headers={"Authorization": token})
#                 self.assertEqual(news_client.status_code, code)
#         new_news = News.objects.get(pk=1)
#         self.assertEqual(new_news.title, "mynewtitle")
#
#
#     def test_put_news(self):
#         data = json.dumps({"title": "mynew_title",
#                            "content": "mynewcontent",
#                            "category": self.category1.pk
#                            # "category": self.category1
#                            })
#         for token, code in self.TOKENS_PUT.items():
#             with self.subTest(f'{token}:{code}'):
#                 news_client = self.client.put(self.url + "1/",
#                                               data, content_type="application/json",
#                                               headers={"Authorization": token})
#                 self.assertEqual(news_client.status_code, code)
#         new_news = News.objects.get(pk=1)
#         self.assertEqual(new_news.title, "mynew_title")
#         self.assertEqual(new_news.content, "mynewcontent")
#         self.assertEqual(new_news.category.pk, 1)
#
