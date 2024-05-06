from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note
from notes.forms import WARNING

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='author')
        cls.reader = User.objects.create(username='Reader')
        cls.note = Note.objects.create(title='1', text='2', author=cls.author)
        cls.anonymous = Client()
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)
        cls.form_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'new-slug'
        }
        cls.add_url = reverse('notes:add')

    def test_user_can_create_note_and_test_anonymous_user_cant(self):
        clients = (self.auth_client, self.anonymous)
        login_url = reverse('users:login')
        for client in clients:
            Note.objects.get().delete()
            with self.subTest(client=client):
                response = client.post(self.add_url, data=self.form_data)
                note_count = Note.objects.count()
                if note_count:
                    self.assertRedirects(response, reverse('notes:success'))
                    self.assertEqual(note_count, 1)
                    new_note = Note.objects.get()
                    self.assertEqual(new_note.title, self.form_data['title'])
                    self.assertEqual(new_note.text, self.form_data['text'])
                    self.assertEqual(new_note.slug, self.form_data['slug'])
                    self.assertEqual(new_note.author, self.author)
                else:
                    expected_url = f'{login_url}?next={self.add_url}'
                    self.assertRedirects(response, expected_url)
                    self.assertEqual(note_count, 0)

    def test_not_unique_slug(self):
        self.form_data['slug'] = self.note.slug
        response = self.auth_client.post(self.add_url, data=self.form_data)
        self.assertFormError(
            response,
            'form',
            'slug',
            errors=(self.note.slug + WARNING)
        )
        self.assertEqual(Note.objects.count(), 1)
