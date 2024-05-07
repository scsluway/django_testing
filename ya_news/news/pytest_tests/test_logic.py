from http import HTTPStatus
from random import choice

import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db

FORM_DATA = {'text': 'Текст комментария'}

FORM_NEW_DATA = {'text': 'Обновлённый комментарий'}


def test_anonymous_user_cant_create_comment(detail_url, client):
    comments_count = Comment.objects.count()
    client.post(detail_url, FORM_DATA)
    assert comments_count == Comment.objects.count()


def test_user_can_create_comment(
        author_client, one_news, author, detail_url
):
    Comment.objects.all().delete()
    response = author_client.post(detail_url, FORM_DATA)
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == FORM_DATA['text']
    assert comment.news == one_news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, detail_url):
    bad_words_data = {
        'text': f'Какой-то текст, {choice(BAD_WORDS)}, еще текст'}
    comments_count = Comment.objects.count()
    response = author_client.post(detail_url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == comments_count


@pytest.mark.usefixtures('comment')
def test_author_can_delete_comment(url_to_comments, author_client, delete_url):
    comments_count = Comment.objects.count()
    response = author_client.delete(delete_url)
    assertRedirects(response, url_to_comments)
    assert comments_count - 1 == Comment.objects.count()


@pytest.mark.usefixtures('comment')
def test_user_cant_delete_comment_of_another_user(
        delete_url, not_author_client
):
    comments_count = Comment.objects.count()
    response = not_author_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == comments_count


def test_author_can_edit_comment(
        comment,
        edit_url,
        url_to_comments,
        author_client,
        author,
        one_news
):
    response = author_client.post(edit_url, data=FORM_NEW_DATA)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == FORM_NEW_DATA['text']
    assert comment.author == author
    assert comment.news == one_news


def test_user_cant_edit_comment_of_another_user(
        edit_url, not_author_client, comment
):
    comment_from_db = Comment.objects.get(pk=comment.pk)
    response = not_author_client.post(edit_url, data=FORM_NEW_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comment.text == comment_from_db.text
    assert comment.author == comment_from_db.author
