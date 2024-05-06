from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):
    AUTH_NAMESPACE = 'notes:'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='author')
        cls.reader = User.objects.create(username='Reader')
        cls.note = Note.objects.create(title='1', text='2', author=cls.author)
        cls.auth_urls = (
            ('detail', (cls.note.id,)),
            ('edit', (cls.note.id,)),
            ('delete', (cls.note.id,)),
            ('list', None),
            ('add', None),
            ('success', None)
        )

    def test_pages_availability_for_everyone(self):
        urls = {
            self.AUTH_NAMESPACE: ('home',),
            'users:': ('login', 'logout', 'signup')
        }
        for spacename, names in urls.items():
            for name in names:
                with self.subTest(name=name):
                    url = reverse(spacename + name)
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_auth_users(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND)
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name, args in self.auth_urls:
                with self.subTest(user=user, name=name):
                    url = reverse(self.AUTH_NAMESPACE + name, args=args)
                    response = self.client.get(url)
                    if args is not None:
                        self.assertEqual(response.status_code, status)
                    else:
                        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirects(self):
        login_url = reverse('users:login')
        for name, args in self.auth_urls:
            with self.subTest(name=name):
                url = reverse(self.AUTH_NAMESPACE + name, args=args)
                expected_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, expected_url)
