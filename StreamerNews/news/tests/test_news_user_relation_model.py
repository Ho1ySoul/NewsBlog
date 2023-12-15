# from django.contrib.auth.models import User
# from django.test import TestCase
#
# from news.models import Category, News, UserNewsRelation
#
#
# class NewsUserRelationModelTestCase(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#
#         cls.category1 = Category.objects.create(pk=1, title="category1")
#
#         cls.user1 = User.objects.create(pk=1, username='user1')
#         cls.user1.set_password('12itcom12')
#         cls.user1.save()
#
#         cls.admin_user = User.objects.create(pk=2, username='admin',
#                                              is_staff=True)
#         cls.admin_user.set_password('12itcom12')
#         cls.admin_user.save()
#
#     def setUp(self):
#         self.news1 = News.objects.create(pk=1, title="news1",
#                                          author=self.user1,
#                                          category=self.category1)
#         self.news2 = News.objects.create(pk=2, title="news2",
#                                          author=self.user1,
#                                          category=self.category1)
#         self.user_news_relation1 = (
#             UserNewsRelation.objects.create(pk=1,
#                                             user=self.user1,
#                                             news=self.news1,
#                                             like=True)
#         )
#
#     def test_have_like(self):
#         self.assertEqual(News.objects.get(pk=1).readers.count(), 1)
#         self.assertEqual(News.objects.get(pk=2).readers.count(), 0)
