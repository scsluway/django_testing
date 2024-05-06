from datetime import datetime, timedelta

from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

import pytest

from news.models import News, Comment

now = timezone.now()


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def many_news():
    return News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=datetime.today() - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def one_news():
    return News.objects.create(
        title='Тестовая новость', text='Просто текст.'
    )


@pytest.fixture
def comment(author, one_news):
    comment = Comment.objects.create(
        news=one_news,
        author=author,
        text='Текст комментария'
    )
    return comment


@pytest.fixture
def id_for_args(one_news):
    return (one_news.id,)


@pytest.fixture
def detail_url(one_news):
    return reverse('news:detail', args=(one_news.id,))


@pytest.fixture
def create_comments(author, one_news):
    for index in range(10):
        comment = Comment.objects.create(
            news=one_news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()


@pytest.fixture
def form_data():
    return {
        'title': 'Новый заголовок',
        'text': 'Новый текст',
        'slug': 'new-slug'
    }
