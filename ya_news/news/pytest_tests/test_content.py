from django.conf import settings
from django.urls import reverse

import pytest
from pytest_django.asserts import assertRedirects
from http import HTTPStatus

HOME_URL = reverse('news:home')


@pytest.mark.django_db
@pytest.mark.usefixtures('news')
def test_news_count(client):
    response = client.get(HOME_URL)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
@pytest.mark.usefixtures('news')
def test_news_order(client):
    response = client.get(HOME_URL)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates
