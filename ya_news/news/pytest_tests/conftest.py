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
def comment(author, one_news, comment_text):
    comment = Comment.objects.create(
        news=one_news,
        author=author,
        text=comment_text
    )
    return comment


@pytest.fixture
def id_news(one_news):
    return (one_news.id,)


@pytest.fixture
def id_comment(comment):
    return (comment.id,)


@pytest.fixture
def detail_url(id_news):
    return reverse('news:detail', args=id_news)


@pytest.fixture
def url_to_comments(detail_url):
    return detail_url + '#comments'


@pytest.fixture
def edit_url(id_comment):
    return reverse('news:edit', args=id_comment)


@pytest.fixture
def delete_url(id_comment):
    return reverse('news:delete', args=id_comment)


@pytest.fixture
def create_comments(author, one_news):
    for index in range(10):
        comment = Comment.objects.create(
            news=one_news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()


@pytest.fixture
def comment_text():
    return 'Текст комментария'


@pytest.fixture
def form_data(comment_text):
    return {'text': comment_text}


@pytest.fixture
def new_comment_text(form_data):
    form_data['text'] = 'Обновлённый комментарий'
    return form_data
