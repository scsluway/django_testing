from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
        ('news:detail', pytest.lazy_fixture('one_news')),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
    )
)
def test_pages_availability(client, name, args):
    if args is None:
        url = reverse(name, args=args)
    else:
        url = reverse(name, args=(args.pk,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'reverse_url',
    (pytest.lazy_fixture('edit_url'), pytest.lazy_fixture('delete_url')),
)
def test_availability_for_comment_edit_and_delete(
        parametrized_client, reverse_url, expected_status
):
    response = parametrized_client.get(reverse_url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url',
    (pytest.lazy_fixture('edit_url'), pytest.lazy_fixture('delete_url')),
)
def test_redirect_for_anonymous_client(url, client):
    login_url = reverse('users:login')
    redirect_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, redirect_url)
