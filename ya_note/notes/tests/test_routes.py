from django.contrib.auth import get_user

from .fixtures import TestFixtures


class TestRoutes(TestFixtures):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.auth_urls = (
            (cls.detail_url, cls.auth_client, cls.STATUS_OK),
            (cls.edit_url, cls.auth_client, cls.STATUS_OK),
            (cls.delete_url, cls.auth_client, cls.STATUS_OK),

            (cls.detail_url, cls.reader_client, cls.STATUS_NOT_FOUND),
            (cls.edit_url, cls.reader_client, cls.STATUS_NOT_FOUND),
            (cls.delete_url, cls.reader_client, cls.STATUS_NOT_FOUND),
        )
        cls.url_for_redirects = (
            cls.detail_url,
            cls.edit_url,
            cls.delete_url,
        )
        cls.reader_urls = (
            cls.list_url,
            cls.add_url,
            cls.success_url,
        )
        cls.anonymous_urls = (
            cls.home_url,
            cls.login_url,
            cls.logout_url,
            cls.signup_url
        )

    def test_pages_availability_for_everyone(self):
        for url in self.anonymous_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, self.STATUS_OK)

    def test_pages_availability_for_auth_user(self):
        for url in self.reader_urls:
            with self.subTest(url=url):
                response = self.reader_client.get(url)
                assert response.status_code == self.STATUS_OK

    def test_pages_availability_for_different_users(self):
        for url, client, status in self.auth_urls:
            with self.subTest(client=get_user(client), status=status):
                response = client.get(url)
                self.assertEqual(response.status_code, status)

    def test_redirects(self):
        for url in self.url_for_redirects:
            with self.subTest(url=url):
                expected_url = f'{self.login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, expected_url)
