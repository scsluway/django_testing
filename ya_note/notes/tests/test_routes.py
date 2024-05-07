from http import HTTPStatus

from django.urls import reverse

from .fixtures import TestFixtures


class TestRoutes(TestFixtures):
    AUTH_NAMESPACE = 'notes:'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.auth_urls = (
            (cls.detail_url, True),
            (cls.edit_url, True),
            (cls.delete_url, True),
            (cls.list_url, False),
            (cls.add_url, False),
            (cls.success_url, False),
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
            (self.auth_client, HTTPStatus.OK),
            (self.not_auth_client, HTTPStatus.NOT_FOUND)
        )
        for client, status in users_statuses:
            for url in self.auth_urls:
                with self.subTest(client=client):
                    response = client.get(url[0])
                    if url[1]:
                        self.assertEqual(response.status_code, status)
                    else:
                        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirects(self):
        for url in self.auth_urls:
            url = url[0]
            with self.subTest(url=url):
                expected_url = f'{self.login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, expected_url)
