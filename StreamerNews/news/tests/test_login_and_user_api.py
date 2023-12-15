from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework.authtoken.models import Token


class LoginTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        user1 = User.objects.create(pk=1, username='user1')
        user1.set_password('12itcom12')
        user1.save()
        cls.user1_token = Token.objects.create(user=user1)

        admin_user = User.objects.create(pk=2, username='admin', is_staff=True)
        admin_user.set_password('12itcom12')
        admin_user.save()
        cls.admin_token = Token.objects.create(user=admin_user)

    def test_correctly_user_login(self):
        client_me = self.client.get('/auth/users/me/', headers={
            'Authorization': 'Token ' + self.user1_token.key})
        self.assertEqual(client_me.status_code, 200)
        self.assertEqual(client_me.json()['username'], 'user1')

    def test_uncorrectly_login(self):
        client_post = self.client.post('/auth/token/login/',
                                       {'username': 'usedas2',
                                        'password': '12itcom12'}
                                       )
        self.assertEqual(client_post.status_code, 400)

    def test_logout(self):
        self.client.login(username='user1',
                          password='12itcom12')
        client_post = self.client.post('/auth/token/logout/')
        self.assertEqual(client_post.status_code, 204)
