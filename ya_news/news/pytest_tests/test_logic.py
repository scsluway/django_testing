from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(detail_url, client, form_data):
    client.post(detail_url, form_data)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(
        comment_text, author_client, one_news, author, form_data, detail_url
):
    response = author_client.post(detail_url, form_data)
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == comment_text
    assert comment.news == one_news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, detail_url):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(detail_url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == 0


@pytest.mark.usefixtures('comment')
def test_author_can_delete_comment(url_to_comments, author_client, delete_url):
    response = author_client.delete(delete_url)
    assertRedirects(response, url_to_comments)
    comments_count = Comment.objects.count()
    assert comments_count == 0


@pytest.mark.usefixtures('comment')
def test_user_cant_delete_comment_of_another_user(
        delete_url, not_author_client
):
    response = not_author_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1


def test_author_can_edit_comment(
        comment,
        edit_url,
        url_to_comments,
        new_comment_text,
        author_client
):
    response = author_client.post(edit_url, data=new_comment_text)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == new_comment_text['text']


def test_user_cant_edit_comment_of_another_user(
        edit_url, not_author_client, new_comment_text, comment, comment_text
):
    response = not_author_client.post(edit_url, data=new_comment_text)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == comment_text
