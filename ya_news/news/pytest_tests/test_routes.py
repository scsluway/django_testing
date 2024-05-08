from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture as lf

pytestmark = pytest.mark.django_db

STATUS_OK = HTTPStatus.OK

STATUS_NOT_FOUND = HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    'reverse_url, parametrized_client, status',
    (
        (lf('edit_url'), lf('not_author_client'), STATUS_NOT_FOUND),
        (lf('delete_url'), lf('not_author_client'), STATUS_NOT_FOUND),

        (lf('edit_url'), lf('author_client'), STATUS_OK),
        (lf('delete_url'), lf('author_client'), STATUS_OK),

        (lf('home_url'), lf('client'), STATUS_OK),
        (lf('login_url'), lf('client'), STATUS_OK),
        (lf('logout_url'), lf('client'), STATUS_OK),
        (lf('signup_url'), lf('client'), STATUS_OK),
        (lf('detail_url'), lf('client'), STATUS_OK),
    ),
)
def test_pages_availability(
        parametrized_client, reverse_url, status
):
    response = parametrized_client.get(reverse_url)
    assert response.status_code == status


@pytest.mark.parametrize(
    'url',
    (lf('edit_url'), lf('delete_url')),
)
def test_redirect_for_anonymous_client(url, client):
    login_url = reverse('users:login')
    redirect_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, redirect_url)
